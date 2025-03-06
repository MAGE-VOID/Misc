import requests
import os
import re
import base64
import json
from dotenv import load_dotenv
import concurrent.futures
from rich.progress import Progress

load_dotenv()
api_key = os.environ.get("token")
token = api_key
headers = {"Authorization": f"token {token}"}


def get_default_branch(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("default_branch", "master")
    return None


def get_repo_tree(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("tree", [])
    else:
        print(f"Error obteniendo el árbol para {repo}: {response.status_code}")
        return []


def fetch_file_content(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("encoding") == "base64":
            try:
                content = base64.b64decode(data["content"]).decode(
                    "utf-8", errors="ignore"
                )
                return content
            except Exception as e:
                # Se omite la impresión para agilizar el proceso
                return None
    return None


def analyze_file_content(filename, content):
    libraries = set()
    ext = os.path.splitext(filename)[1].lower()

    if filename == "Dockerfile":
        libraries.add("Docker")
    elif ext == ".py":
        py_imports = re.findall(
            r"^\s*(?:import|from)\s+([\w\.]+)", content, re.MULTILINE
        )
        libraries.update(py_imports)
    elif ext in {".cpp", ".c", ".h", ".hpp", ".mq5", ".mql5"}:
        cpp_includes = re.findall(r'#include\s*[<"]([\w\./]+)[">]', content)
        libraries.update(cpp_includes)
        if ext in {".mq5", ".mql5"}:
            libraries.add("MQL5")
    elif ext == ".cs":
        cs_usings = re.findall(r"^\s*using\s+([\w\.]+);", content, re.MULTILINE)
        libraries.update(cs_usings)
        libraries.add("C#")
    elif ext == ".go":
        go_imports = re.findall(r'import\s+\(?\s*"([^"]+)"', content)
        libraries.update(go_imports)
        libraries.add("Go")
    elif ext in {".js", ".jsx", ".ts", ".tsx"}:
        js_requires = re.findall(r'require\(\s*[\'"]([\w\-/]+)[\'"]\s*\)', content)
        js_imports = re.findall(
            r'import\s+(?:.*\s+from\s+)?[\'"]([\w\-/]+)[\'"]', content
        )
        libraries.update(js_requires)
        libraries.update(js_imports)
    elif ext == ".php":
        php_includes = re.findall(
            r'(?:include|require|use)\s+[\'"]([\w\\\/]+)[\'"]', content
        )
        libraries.update(php_includes)
    elif ext == ".sql":
        sql_matches = re.findall(r"--\s*LIB:\s*(\w+)", content)
        libraries.update(sql_matches)
    elif ext == ".css":
        css_imports = re.findall(r'@import\s+[\'"]([\w\-/\.]+)[\'"]', content)
        libraries.update(css_imports)
        libraries.add("CSS")
    elif ext in {".html", ".htm"}:
        scripts = re.findall(
            r'<script\s+[^>]*src=["\']([^"\']+)["\']', content, re.IGNORECASE
        )
        links = re.findall(
            r'<link\s+[^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE
        )
        libraries.update(scripts)
        libraries.update(links)
        libraries.add("HTML")
    elif ext == ".ipynb":
        try:
            notebook = json.loads(content)
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "code":
                    cell_code = "\n".join(cell.get("source", []))
                    py_imports = re.findall(
                        r"^\s*(?:import|from)\s+([\w\.]+)", cell_code, re.MULTILINE
                    )
                    libraries.update(py_imports)
            libraries.add("Jupyter Notebook")
        except Exception:
            libraries.add("Jupyter Notebook")
    return libraries


allowed_extensions = {
    ".py",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".php",
    ".sql",
    ".cs",
    ".mq5",
    ".mql5",
    ".go",
    ".css",
    ".html",
    ".htm",
    ".ipynb",
}

repos = []
page = 1
while True:
    url = f"https://api.github.com/user/repos?per_page=100&page={page}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error al obtener repositorios:", response.status_code)
        break
    data = response.json()
    if not data:
        break
    repos.extend(data)
    page += 1

global_summary = {}  # Contador global de tecnologías/librerías
global_file_summary = {}  # Contador global de tipos de archivo

# Configuramos la barra de progreso global con Rich
with Progress() as progress:
    overall_task = progress.add_task(
        "[cyan]Procesando repositorios...", total=len(repos)
    )

    for repo in repos:
        owner = repo["owner"]["login"]
        repo_name = repo["name"]
        default_branch = get_default_branch(owner, repo_name)
        if not default_branch:
            progress.advance(overall_task)
            continue

        tree = get_repo_tree(owner, repo_name, default_branch)
        repo_libraries = {}
        future_to_path = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for item in tree:
                if item["type"] == "blob":
                    path = item["path"]
                    if repo_name == "MQL5" and not (
                        path.startswith("Experts/") or path.startswith("Include/")
                    ):
                        continue
                    ext = os.path.splitext(path)[1].lower()
                    file_type = "Dockerfile" if path == "Dockerfile" else ext
                    global_file_summary[file_type] = (
                        global_file_summary.get(file_type, 0) + 1
                    )

                    if path == "Dockerfile" or ext in allowed_extensions:
                        future = executor.submit(
                            fetch_file_content, owner, repo_name, path
                        )
                        future_to_path[future] = path

            total_files = len(future_to_path)
            if total_files:
                file_task = progress.add_task(
                    f"[green]Procesando archivos de {repo_name}", total=total_files
                )
                for future in concurrent.futures.as_completed(future_to_path):
                    path = future_to_path[future]
                    content = future.result()
                    if content:
                        libs = analyze_file_content(path, content)
                        if libs:
                            for lib in libs:
                                repo_libraries[lib] = repo_libraries.get(lib, 0) + 1
                                global_summary[lib] = global_summary.get(lib, 0) + 1
                    progress.advance(file_task)
        progress.advance(overall_task)

# Imprimir resúmenes globales al finalizar
print("\nResumen global de tecnologías utilizadas:")
for lib, count in sorted(global_summary.items(), key=lambda x: x[1], reverse=True):
    print(f"  {lib}: {count} ocurrencia(s)")

print("\nResumen global de tipos de archivo analizados:")
for file_type, count in sorted(
    global_file_summary.items(), key=lambda x: x[1], reverse=True
):
    print(f"  {file_type}: {count} archivo(s)")
