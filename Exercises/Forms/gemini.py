import os
import json
import csv
import random
import time
import ast
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

# 5 ejes de "personalidad" para cada encuesta
ROLES = [
    "joven universitario(a) entusiasta de la gastronomía",
    "profesional ocupado(a) que busca snacks rápidos",
    "amante de la comida saludable",
    "foodie curioso(a) que siempre busca sabores nuevos",
    "fanático(a) de las comidas tradicionales peruanas",
    "viajero(a) que prueba snacks locales en cada visita",
    "padre/madre de familia con poco tiempo para comer",
    "deportista que busca energía antes o después del entrenamiento",
    "influencer gastronómico(a)",
    "chef aficionado(a)",
]

MOODS = [
    "amable",
    "feliz",
    "curioso(a)",
    "estresado(a)",
    "relajado(a)",
    "emocionado(a)",
    "indeciso(a)",
    "ambicioso(a)",
    "creativo(a)",
    "práctico(a)",
]

AGE_GROUPS = [
    "Menos de 18 años",
    "18 - 24 años",
    "25 - 34 años",
    "35 - 44 años",
    "Más de 45 años",
]

TRAITS = [
    "ambicioso(a)",
    "trabajador(a)",
    "exitoso(a)",
    "tímido(a)",
    "extrovertido(a)",
    "optimista",
    "pesimista",
    "analítico(a)",
    "aventurero(a)",
    "soñador(a)",
]

HOBBIES = [
    "cocinar en casa",
    "hacer ejercicio",
    "ver series",
    "viajar",
    "leer novelas",
    "jardinería",
    "fotografía",
    "tocar música",
    "videojuegos",
    "meditar",
]


def safe_generate_content(client, model, contents, config):
    """Llama a Gemini y, en caso de 429, espera y reintenta indefinidamente."""
    while True:
        try:
            return client.models.generate_content(
                model=model, contents=contents, config=config
            )
        except errors.ClientError as e:
            txt = str(e)
            parsed = {}
            if "{" in txt:
                try:
                    parsed = ast.literal_eval(txt[txt.index("{") :])
                except Exception:
                    pass
            err = parsed.get("error", parsed) if isinstance(parsed, dict) else {}
            code = err.get("code")
            status = err.get("status", "")
            if code == 429 or "RESOURCE_EXHAUSTED" in status:
                retry = 35.0
                for d in err.get("details", []):
                    rd = d.get("retryDelay", "")
                    if isinstance(rd, str) and rd.endswith("s"):
                        try:
                            retry = float(rd[:-1])
                        except:
                            pass
                        break
                print(f"⚠️ Rate limit ({status}), esperando {retry}s...")
                time.sleep(retry)
                continue
            raise


def generate_with_content(client, model, contents, config):
    """Asegura que la respuesta tenga texto no vacío."""
    while True:
        resp = safe_generate_content(client, model, contents, config)
        text = getattr(resp, "text", "")
        if text and text.strip():
            return resp
        print("⚠️ Respuesta vacía, reintentando en 1s...")
        time.sleep(1)


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Falta API_KEY en .env")

    client = genai.Client(api_key=api_key)
    model = "gemma-3-27b-it"

    base = os.path.dirname(os.path.abspath(__file__))
    alt_path = os.path.join(base, "alternativas.json")
    csv_path = os.path.join(base, "encuesta.csv")

    with open(alt_path, encoding="utf-8") as f:
        alternativas = json.load(f)

    # Cuenta filas existentes (sin contar encabezado)
    if os.path.exists(csv_path):
        with open(csv_path, encoding="utf-8-sig") as fr:
            existing = list(csv.reader(fr, delimiter=";"))
        start = max(0, len(existing) - 1)
    else:
        start = 0

    if start >= 350:
        print("🎉 Ya hay 350 filas. Nada por hacer.")
        return

    with open(csv_path, "a", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")

        for idx in range(start, 350):
            # Construye contexto
            role = random.choice(ROLES)
            mood = random.choice(MOODS)
            age = random.choice(AGE_GROUPS)
            trait = random.choice(TRAITS)
            hobby = random.choice(HOBBIES)
            contexto = f"Eres {role}, tienes {age}, te sientes {mood}, eres {trait} y disfrutas de {hobby}."

            # Monta prompt único para toda la encuesta
            lines = [
                f"Contexto (usuario): {contexto}",
                'Responde devolviendo un JSON con campo "answers":',
                "un array de respuestas en orden de las preguntas.",
                "No incluyas texto adicional.\nEncuesta:",
            ]
            for i, (preg, opts) in enumerate(alternativas.items(), start=1):
                if opts:
                    opts_txt = "\n".join(
                        f"{j}. {o}" for j, o in enumerate(opts, start=1)
                    )
                    lines.append(f"{i}. {preg}\nOpciones:\n{opts_txt}")
                else:
                    # Pregunta abierta
                    lines.append(f"{i}. {preg}\n(Respuesta libre, máximo 10 palabras)")

            prompt = "\n\n".join(lines)
            contents = [
                types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
            ]
            config = types.GenerateContentConfig(response_mime_type="text/plain")

            resp = generate_with_content(client, model, contents, config)
            txt = resp.text.strip()

            # Extrae JSON
            try:
                data = json.loads(txt)
                fila = data["answers"]
                if not isinstance(fila, list) or len(fila) != len(alternativas):
                    raise
            except:
                # fallback aleatorio; para abiertas genera respuesta corta
                fila = [
                    (
                        random.choice(opts)
                        if opts
                        else "Me encantaría probar una salsa especial."
                    )
                    for opts in alternativas.values()
                ]

            # Si alguna abierta quedó vacía o genérica, rellena con segunda pasada
            for i, (preg, opts) in enumerate(alternativas.items()):
                if not opts and (
                    not fila[i].strip() or fila[i].startswith("Me encantaría")
                ):
                    prompt_abierta = (
                        f"Contexto: {contexto}\n\n"
                        f"Pregunta abierta:\n{preg}\n"
                        "Por favor, responde con sinceridad en máximo 10 palabras."
                    )
                    resp2 = generate_with_content(
                        client,
                        model,
                        [
                            types.Content(
                                role="user",
                                parts=[types.Part.from_text(text=prompt_abierta)],
                            )
                        ],
                        config,
                    )
                    fila[i] = resp2.text.strip()

            # Escribe CSV
            writer.writerow([r.replace(";", ",") for r in fila])
            csvfile.flush()
            os.fsync(csvfile.fileno())
            print(f"✅ Fila {idx+1} completada.")

    print(f"🎉 Se añadieron {350 - start} filas en {csv_path}")


if __name__ == "__main__":
    main()
