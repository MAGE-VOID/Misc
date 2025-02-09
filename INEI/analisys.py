import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el archivo CSV (actualiza la ruta si es necesario)
file_path_data = (
    r"D:\FOREX\MT5_1\MQL5\Experts\Projects\Sharing-Projects\Misc\INEI\Data_Renamed.csv"
)
df = pd.read_csv(file_path_data)

# Mostrar las primeras filas y las estadísticas descriptivas
print("Vista de Datos:")
print(df.head())

print("\nEstadísticas Descriptivas:")
print(df.describe(include="all"))

# Verificamos los tipos de datos
print("\nTipos de Datos:")
print(df.dtypes)

# Verificar la cantidad y porcentaje de datos faltantes
missing_data = df.isnull().sum()
missing_percentage = (missing_data / len(df)) * 100
print("\nDatos Faltantes:")
print(missing_data[missing_data > 0])

print("\nPorcentaje de Datos Faltantes:")
print(missing_percentage[missing_percentage > 0])

# Detectar y mostrar valores atípicos para las columnas de ingresos y horas trabajadas
numerical_cols = [
    "Ingreso Total Mensual",
    "Ingreso principal mensual",
    "TOTAL, DE HORAS TRABAJADAS",
]

# Función para detectar outliers con el método de IQR
def detect_outliers(df, column):
    # Convertir a tipo numérico si no lo está, y eliminar valores no numéricos
    df[column] = pd.to_numeric(df[column], errors="coerce")
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

# Mostrar los outliers para cada columna
for col in numerical_cols:
    outliers = detect_outliers(df, col)
    print(f"\nOutliers en la columna {col}:")
    print(outliers[[col]])

# Asegúrate de que las columnas de ingresos estén en el formato correcto
df["Ingreso Total Mensual"] = pd.to_numeric(
    df["Ingreso Total Mensual"], errors="coerce"
)
df["Ingreso principal mensual"] = pd.to_numeric(
    df["Ingreso principal mensual"], errors="coerce"
)

# Graficar la distribución de los ingresos (Ingreso Total Mensual)
plt.figure(figsize=(10, 6))
sns.histplot(df["Ingreso Total Mensual"].dropna(), kde=True, color="blue")
plt.title("Distribución de Ingreso Total Mensual")
plt.xlabel("Ingreso Total Mensual")
plt.ylabel("Frecuencia")
plt.xticks(rotation=45)  # Rotar las etiquetas del eje X
plt.show()

# Graficar la distribución por género
plt.figure(figsize=(6, 6))
sns.countplot(x="207. SEXO", data=df, palette="Set2")
plt.title("Distribución por Género")
plt.xlabel("Sexo")
plt.ylabel("Frecuencia")
plt.xticks(rotation=45)  # Rotar las etiquetas del eje X
plt.show()

# Asegurarse de que las columnas de horas trabajadas estén en el formato correcto
df["TOTAL, DE HORAS TRABAJADAS"] = pd.to_numeric(
    df["TOTAL, DE HORAS TRABAJADAS"], errors="coerce"
)

# Graficar la relación entre Ingreso Total Mensual y Horas Trabajadas
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df["TOTAL, DE HORAS TRABAJADAS"], y=df["Ingreso Total Mensual"])
plt.title("Relación entre Ingreso Total Mensual y Horas Trabajadas")
plt.xlabel("Horas Trabajadas")
plt.ylabel("Ingreso Total Mensual")
plt.xticks(rotation=45)  # Rotar las etiquetas del eje X
plt.show()

# Si hay una columna de "Año de la encuesta" o "Mes de la encuesta", podemos analizar las tendencias temporales.
if "Año de la encuesta" in df.columns and "Mes de la encuesta" in df.columns:
    df["Fecha"] = pd.to_datetime(
        df["Año de la encuesta"].astype(str)
        + "-"
        + df["Mes de la encuesta"].astype(str),
        format="%Y-%m",
    )

    # Graficar la evolución de los ingresos a lo largo del tiempo
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="Fecha", y="Ingreso Total Mensual")
    plt.title("Tendencia de Ingreso Total Mensual a lo largo del Tiempo")
    plt.xlabel("Fecha")
    plt.ylabel("Ingreso Total Mensual")
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje X
    plt.show()

# Análisis por género: Ingreso Total Mensual por Sexo
plt.figure(figsize=(8, 6))
sns.boxplot(x="207. SEXO", y="Ingreso Total Mensual", data=df)
plt.title("Ingreso Total Mensual por Género")
plt.xlabel("Sexo")
plt.ylabel("Ingreso Total Mensual")
plt.xticks(rotation=45)  # Rotar las etiquetas del eje X
plt.show()
