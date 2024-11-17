from module_dates import generate_module_dates
from datetime import datetime
import os

# Definimos la ruta del folder y el nombre del archivo
folder = "D:/FOREX/MT5_1/MQL5/Experts/Python/DadProject/GetDates" 
name = "resultado_generado.txt"

# Creamos la ruta completa del archivo
ruta_completa = os.path.join(folder, name)

# Escribimos la cadena de texto en el archivo, asegurándonos de que se cree en la ruta especificada
# Asegúrate de usar el modo 'w' para abrir el archivo en modo escritura
with open(ruta_completa, "w") as archivo:
    archivo.write("aaaaaaaaaaaaaaaaaaaaa123")




"""
fecha = datetime(2024, 3, 4)
generador = generate_module_dates(fecha, 3)

print(generador)

# Convertimos la salida del generador a una cadena de texto
# Asumiendo que el generador devuelve un diccionario como en tu ejemplo
resultado_str = str(generador)

"""

