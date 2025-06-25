import csv
import os

# Directorio donde está este script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta completa para crear encuesta.csv en la misma carpeta
ruta_csv = os.path.join(script_dir, "encuesta.csv")

# Lista de preguntas (encabezados) de la encuesta
preguntas = [
    "¿Eres fan de los triples?",
    "¿Cuántos años tienes?",
    "Género",
    "¿En qué distrito de Lima Metropolitana resides o pasas la mayor parte de tu tiempo?",
    "¿Con qué frecuencia consumes triples durante la semana?",
    "¿En qué momento disfrutas más de este tipo de snack? (Selecciona todas las que apliquen)",
    "¿Dónde compras tus triples actualmente?",
    "¿Qué valoras más al elegir un triple?",
    "¿Cuál de estas presentaciones de Triple X te parece más atractiva y deliciosa?",
    "¿Qué tipo de cremas o salsas te gustaría que acompañen nuestros triples? (Selecciona todas las que apliquen)",
    "¿Tienes en mente alguna crema especial que no viste en la lista anterior y te encantaría que acompañe nuestros triples?",
    "Si tuvieras la oportunidad de probar un nuevo triple fácil de llevar, con rellenos sabrosos y diferentes, ¿qué tanto te interesaría?",
    "¿Qué tan dispuesto(a) estás a probar sabores nuevos en productos como los triples?",
    "¿Con qué te gustaría acompañar tu triple al momento de comerlo? (Selecciona todas las que apliquen)",
    "Considerando un triple de buena calidad y tamaño, ¿Cuánto te parecería justo pagar?",
    "¿Dónde te gustaría poder comprar este Triple X? (Selecciona todas las que apliquen)",
    "¿Con qué frecuencia utilizarías un servicio de delivery para pedir estos triples?",
    "Si el producto cumple con tus expectativas, ¿qué tan probable sería que lo recomiendes a un amigo o familiar?",
    "¿Tienes algún comentario, sugerencia o idea adicional que quieras compartir con nosotros sobre este nuevo producto?"
]

# Crear el CSV con BOM UTF-8 y punto y coma como separador
with open(ruta_csv, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(preguntas)

print(f"Archivo creado en: {ruta_csv}")
