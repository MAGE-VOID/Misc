import torch
import time
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)
from langchain_huggingface import HuggingFacePipeline

# --------------------------------------------------------------------------
# CONFIGURACIÓN DEL MODELO
# --------------------------------------------------------------------------
model_path = r"G:\deepseek-llm-7b-chat"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",
    quantization_config=quant_config,
    torch_dtype=torch.float16,
)

# Configurar el pipeline de generación con hiperparámetros adecuados
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.2,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id,
    truncation=True,
)

llm = HuggingFacePipeline(pipeline=pipe)

# --------------------------------------------------------------------------
# PROCESO DE PENSAMIENTO (DINÁMICO, HASTA UN MÁXIMO DE 30 ITERACIONES)
# --------------------------------------------------------------------------
def proceso_pensamiento_dinamico(llm, question, max_iteraciones=30):
    """
    Simula el diálogo interno del sistema. Decide cuándo detenerse,
    con un máximo de 30 iteraciones.
    """
    # Inicializamos el razonamiento interno
    texto_dialogo = (
        "Eres un sistema de pensamiento crítico que razona consigo mismo para "
        "encontrar la mejor respuesta.\n\n"
        f"Pregunta a resolver: {question}\n\n"
        "Inicia tu razonamiento interno y continúa preguntándote y respondiéndote hasta llegar a una conclusión clara. "
        "Indica cuándo consideras que tienes una respuesta definitiva usando la frase: 'He llegado a una conclusión'.\n"
        "Sistema (pensando):"
    )
    
    for i in range(max_iteraciones):
        # Llamada al modelo con el texto acumulado
        salida = llm(texto_dialogo)
        
        if isinstance(salida, list) and len(salida) > 0 and 'generated_text' in salida[0]:
            new_segment = salida[0]['generated_text']
        else:
            new_segment = salida if isinstance(salida, str) else str(salida)
        
        # Identificamos lo nuevo generado por el modelo
        new_segment_stripped = new_segment.replace(texto_dialogo, "").strip()
        
        # Agregamos el nuevo segmento al diálogo acumulado
        texto_dialogo += new_segment_stripped

        # Imprimir la iteración actual
        print(f"\n\033[1;34m[ITERACIÓN {i+1} PENSAMIENTO]\033[0m\n")
        print(new_segment_stripped.strip())
        time.sleep(1)

        # Detener el bucle si el modelo indica que ha llegado a una conclusión
        if "He llegado a una conclusión" in new_segment_stripped:
            print("\n\033[1;32m[CONCLUSIÓN DETECTADA]\033[0m El modelo ha decidido que ha finalizado su razonamiento.\n")
            break

    # Retornamos el razonamiento completo generado
    return texto_dialogo

# --------------------------------------------------------------------------
# PROCESO DE RESPUESTA (CONCLUSIÓN FINAL)
# --------------------------------------------------------------------------
def proceso_respuesta(llm, razonamiento):
    """
    Toma el razonamiento interno final y pide al modelo que brinde una
    respuesta concisa y clara para el usuario.
    """
    prompt_final = (
        f"{razonamiento}\n\n"
        "Ahora, por favor, elabora tu respuesta final de manera clara y directa, "
        "dirigida al usuario, sin mostrar tu razonamiento interno paso a paso:\n"
        "Respuesta:"
    )
    
    salida = llm(prompt_final)
    if isinstance(salida, list) and len(salida) > 0 and 'generated_text' in salida[0]:
        final_answer = salida[0]['generated_text']
    else:
        final_answer = salida if isinstance(salida, str) else str(salida)
    
    final_answer_stripped = final_answer.replace(prompt_final, "").strip()
    return final_answer_stripped

# --------------------------------------------------------------------------
# EJECUCIÓN: EJEMPLO PRÁCTICO
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # Pregunta de ejemplo
    question = "Que hay dentro del agujero negro?"

    print(f"\n\033[1;32m[PREGUNTA]\033[0m {question}\n")
    
    # Proceso de pensamiento dinámico
    texto_razonamiento = proceso_pensamiento_dinamico(llm, question, max_iteraciones=30)

    # Proceso de respuesta final
    print("\n\033[1;33m[RESPUESTA FINAL]\033[0m\n")
    respuesta_final = proceso_respuesta(llm, texto_razonamiento)
    print(respuesta_final)
