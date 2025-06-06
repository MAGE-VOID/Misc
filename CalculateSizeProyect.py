"""

Calcula:
  1. El tamaño total de la carpeta de tu proyecto (por defecto, la carpeta donde está este script).
  2. El tamaño únicamente de las librerías (módulos) que se importan dentro de ese proyecto
     y que están instaladas en site-packages.

"""

import os
import sys
import ast
import argparse
import importlib.util
from typing import Optional, Set, List, Tuple


class ProjectSizeAnalyzer:
    """
    Clase que encapsula toda la lógica para:
      - Calcular el tamaño total de un proyecto.
      - Detectar los imports top-level y computar el tamaño de las librerías externas instaladas.
    """

    def __init__(self, project_dir: str) -> None:
        self.project_dir: str = os.path.abspath(project_dir)
        if not os.path.isdir(self.project_dir):
            raise NotADirectoryError(
                f"ERROR: '{self.project_dir}' no existe o no es un directorio."
            )

    @staticmethod
    def human_readable(bytesize: int) -> str:
        """
        Transforma un número de bytes en una cadena legible (KB, MB, GB…).
        """
        for unidad in ["B", "KB", "MB", "GB", "TB", "PB"]:
            if bytesize < 1024.0:
                return f"{bytesize:3.1f} {unidad}"
            bytesize /= 1024.0
        return f"{bytesize:.1f} PB"

    def get_dir_size(self, path: str) -> int:
        """
        Recorre 'path' recursivamente y suma el tamaño de todos los archivos (en bytes).
        Omite enlaces simbólicos y archivos inaccesibles.
        """
        total: int = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for fname in filenames:
                fp = os.path.join(dirpath, fname)
                try:
                    if not os.path.islink(fp):
                        total += os.path.getsize(fp)
                except (OSError, FileNotFoundError):
                    # Si un archivo está inaccesible, lo ignoramos
                    continue
        return total

    def collect_top_imports(self) -> Set[str]:
        """
        Recorre todos los archivos .py dentro de project_dir (recursivo),
        parsea sus imports con ast y devuelve un conjunto de nombres de
        módulo top-level (la primera parte antes del punto).
        """
        top_levels: Set[str] = set()

        for root, _, files in os.walk(self.project_dir):
            for fname in files:
                if not fname.endswith(".py"):
                    continue
                fullpath = os.path.join(root, fname)
                try:
                    with open(fullpath, "r", encoding="utf-8") as f:
                        source = f.read()
                except (OSError, UnicodeDecodeError):
                    continue

                try:
                    tree = ast.parse(source, filename=fullpath)
                except SyntaxError:
                    # Si el .py tiene sintaxis inválida, lo saltamos
                    continue

                for node in ast.walk(tree):
                    # import foo or import foo.bar
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            nombre = alias.name.split(".")[0]
                            top_levels.add(nombre)

                    # from foo import bar  OR  from foo.bar import baz
                    elif isinstance(node, ast.ImportFrom):
                        # Si es import relativo (level > 0), lo ignoramos
                        if node.level != 0 or node.module is None:
                            continue
                        nombre = node.module.split(".")[0]
                        top_levels.add(nombre)

        return top_levels

    def is_local_module(self, name: str) -> bool:
        """
        Comprueba si 'name' coincide con un módulo local del proyecto, esto es:
          - project_dir/<name>.py   O
          - project_dir/<name>/__init__.py
        En cuyo caso lo consideramos parte del proyecto y NO una librería externa.
        """
        posible_py = os.path.join(self.project_dir, f"{name}.py")
        if os.path.isfile(posible_py):
            return True

        posible_pkg = os.path.join(self.project_dir, name, "__init__.py")
        if os.path.isfile(posible_pkg):
            return True

        return False

    @staticmethod
    def find_module_root(name: str) -> Optional[str]:
        """
        Dado un nombre de módulo top-level (por ejemplo, 'cv2', 'ultralytics', 'google'),
        retorna la ruta absoluta a:
          - si es un paquete: la carpeta del paquete (donde está __init__.py)
          - si es un módulo simple: la ruta al archivo .py o .pyd/.so
        Si no se puede encontrar (o es built-in o stdlib), devuelve None.
        """
        try:
            spec = importlib.util.find_spec(name)
        except (ImportError, AttributeError):
            return None

        if spec is None:
            return None

        # Si es package, spec.submodule_search_locations contendrá la carpeta
        if spec.submodule_search_locations:
            return list(spec.submodule_search_locations)[0]

        # Si no tiene submodule_search_locations, es un módulo simple; origin indica el archivo
        origin = spec.origin
        if origin is None or origin == "built-in":
            return None

        return origin

    def run(self) -> None:
        """
        Método principal que orquesta todo el flujo:
          1) Calcula el tamaño total del proyecto.
          2) Recopila imports top-level y filtra los externos.
          3) Busca la ruta de cada paquete externo en site-packages.
          4) Calcula tamaños, muestra resultados.
        """
        # 1) Calcular tamaño total del proyecto
        print(f"Calculando tamaño del proyecto en: {self.project_dir}\n")
        tamaño_proyecto_bytes = self.get_dir_size(self.project_dir)
        print(
            f"→ Tamaño TOTAL de '{self.project_dir}': "
            f"{self.human_readable(tamaño_proyecto_bytes)} ({tamaño_proyecto_bytes} bytes)\n"
        )

        # 2) Extraer todos los imports top-level que aparecen en .py del proyecto
        imports_top = self.collect_top_imports()
        imports_externos = {m for m in imports_top if not self.is_local_module(m)}

        # 3) Para cada módulo externo, localizar su ruta
        paquetes_a_contar: Set[str] = set()  # rutas absolutas de carpeta o archivo
        paquetes_ignorados: Set[str] = (
            set()
        )  # nombres que no se encontraron / built-in / stdlib

        for nombre in sorted(imports_externos):
            root = self.find_module_root(nombre)
            if root is None:
                paquetes_ignorados.add(nombre)
                continue

            norm = os.path.normcase(root).lower()
            if "site-packages" in norm:
                paquetes_a_contar.add(root)
            else:
                # Si no contiene "site-packages" en la ruta, lo ignoramos (stdlib, built-in, etc.)
                paquetes_ignorados.add(nombre)

        # 4) Mostrar qué librerías se van a contar y cuáles se ignoraron
        print("=== MÓDULOS EXTERNOS DETECTADOS ===\n")
        if paquetes_a_contar:
            print("Se contarán (paquetes en site-packages usados por el proyecto):")
            for idx, ruta in enumerate(sorted(paquetes_a_contar), 1):
                print(f"  {idx}. {ruta}")
        else:
            print(
                "No se detectó ningún paquete externo instalado en site-packages que importe el proyecto."
            )

        if paquetes_ignorados:
            print("\nSe ignoraron (built-in, stdlib o no instalados):")
            for nombre in sorted(paquetes_ignorados):
                print(f"  - {nombre}")
        print("")

        # 5) Para cada ruta en paquetes_a_contar, sumar su tamaño
        tamaño_librerias_bytes = 0
        detalles_librerias: List[Tuple[str, int]] = (
            []
        )  # lista de tuplas (ruta, tamaño_bytes)
        for ruta in paquetes_a_contar:
            if os.path.isdir(ruta):
                size = self.get_dir_size(ruta)
            elif os.path.isfile(ruta):
                try:
                    size = os.path.getsize(ruta)
                except OSError:
                    size = 0
            else:
                size = 0
            detalles_librerias.append((ruta, size))
            tamaño_librerias_bytes += size

        # 6) Mostrar detalles y total de librerías
        if detalles_librerias:
            print("=== TAMAÑO POR PAQUETE CONSULTADO ===\n")
            for ruta, size in sorted(detalles_librerias, key=lambda x: x[0].lower()):
                print(f"{self.human_readable(size):>8}   ← {ruta}")
            print("")

        tamaño_librerias_str = self.human_readable(tamaño_librerias_bytes)
        print("=== RESULTADO FINAL ===\n")
        print(
            f"Tamaño de librerías usadas: {tamaño_librerias_str} "
            f"({tamaño_librerias_bytes} bytes)"
        )
        total_bytes = tamaño_proyecto_bytes + tamaño_librerias_bytes
        print(
            f"Tamaño COMBINADO:          {self.human_readable(total_bytes)} "
            f"({total_bytes} bytes)\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calcula el tamaño del proyecto y de las librerías externas usadas."
    )
    parser.add_argument(
        "-p",
        "--project-dir",
        default=os.path.dirname(__file__),
        help="Ruta al proyecto (por defecto, la carpeta donde está este script).",
    )
    args = parser.parse_args()

    try:
        analyzer = ProjectSizeAnalyzer(args.project_dir)
    except NotADirectoryError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR inesperado al iniciar: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        analyzer.run()
    except Exception as e:
        print(f"ERROR durante el análisis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
