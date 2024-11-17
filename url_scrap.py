import requests
from bs4 import BeautifulSoup

def obtener_texto_de_url(url):
    try:
        # Realiza una solicitud GET para obtener el contenido de la página
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa (código 200)
        
        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrae el texto visible (sin las etiquetas HTML)
        texto = soup.get_text(separator=' ', strip=True)
        return texto
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
        return ""

def guardar_texto_en_archivo(urls, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for url in urls:
            # Escribe el encabezado de la URL en el archivo
            f.write(f"=== Texto extraído de: {url} ===\n\n")
            
            # Obtiene el texto de la URL
            texto = obtener_texto_de_url(url)
            
            # Escribe el texto en el archivo
            f.write(texto + "\n\n")
            
            # Escribe una línea de separación entre diferentes URLs
            f.write("="*50 + "\n\n")

if __name__ == "__main__":
    # Lista de URLs que deseas procesar
    urls = [
        'https://www.mql5.com/es/docs/onnx/onnx_intro',
        'https://www.mql5.com/es/docs/onnx/onnx_conversion',
        'https://www.mql5.com/es/docs/onnx/onnx_types_autoconversion',
        'https://www.mql5.com/es/docs/onnx/onnx_prepare',
        'https://www.mql5.com/es/docs/onnx/onnx_mql5',
        'https://www.mql5.com/es/docs/onnx/onnx_test',
        'https://www.mql5.com/es/docs/onnx/onnxcreate',
        'https://www.mql5.com/es/docs/onnx/onnxcreatefrombuffer',
        'https://www.mql5.com/es/docs/onnx/onnxrelease',
        'https://www.mql5.com/es/docs/onnx/onnxrun',
        'https://www.mql5.com/es/docs/onnx/onnxgetinputcount',
        'https://www.mql5.com/es/docs/onnx/onnxgetoutputcount',
        'https://www.mql5.com/es/docs/onnx/onnxgetinputname',
        'https://www.mql5.com/es/docs/onnx/onnxgetoutputname',
        'https://www.mql5.com/es/docs/onnx/onnxgetinputtypeinfo',
        'https://www.mql5.com/es/docs/onnx/onnxgetoutputtypeinfo',
        'https://www.mql5.com/es/docs/onnx/onnxsetinputshape',
        'https://www.mql5.com/es/docs/onnx/onnxsetoutputshape',
        'https://www.mql5.com/es/docs/onnx/onnx_structures',

        # Agrega más URLs aquí
    ]
    
    # Archivo de salida donde se guardará el texto extraído
    archivo_salida = 'resultado_texto_urls.txt'
    
    # Llamada a la función para procesar las URLs y guardar el texto
    guardar_texto_en_archivo(urls, archivo_salida)

    print(f"El texto ha sido guardado en {archivo_salida}")
