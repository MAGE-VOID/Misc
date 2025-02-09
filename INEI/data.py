import pandas as pd

# Leer el archivo de datos .csv con la ruta completa
file_path_data = r'D:\FOREX\MT5_1\MQL5\Experts\Projects\Sharing-Projects\Misc\INEI\Data_Renamed.csv'
df = pd.read_csv(file_path_data)

# Mostrar las primeras filas del dataframe
print("Vista de Datos:")
print(df.head())

# Mostrar los nombres de las columnas
print("\nNombres de las Columnas:")
print(df.columns.tolist())
