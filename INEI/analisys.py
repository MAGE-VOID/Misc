import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

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

# Convertir las columnas relevantes a formato numérico
df["Ingreso Total Mensual"] = pd.to_numeric(
    df["Ingreso Total Mensual"], errors="coerce"
)
df["Ingreso principal mensual"] = pd.to_numeric(
    df["Ingreso principal mensual"], errors="coerce"
)
df["TOTAL, DE HORAS TRABAJADAS"] = pd.to_numeric(
    df["TOTAL, DE HORAS TRABAJADAS"], errors="coerce"
)

# ===============================
# Medidas Estadísticas
# ===============================

# Medidas para 'Ingreso Total Mensual'
print("\nMedidas Estadísticas para 'Ingreso Total Mensual':")
ingreso_total = df["Ingreso Total Mensual"].dropna()
print("Media:", ingreso_total.mean())
print("Mediana:", ingreso_total.median())
print(
    "Moda:",
    ingreso_total.mode().iloc[0] if not ingreso_total.mode().empty else "Sin moda",
)
print("Desviación Estándar:", ingreso_total.std())
print("Mínimo:", ingreso_total.min())
print("Máximo:", ingreso_total.max())

# Medidas para 'Ingreso principal mensual'
print("\nMedidas Estadísticas para 'Ingreso principal mensual':")
ingreso_principal = df["Ingreso principal mensual"].dropna()
print("Media:", ingreso_principal.mean())
print("Mediana:", ingreso_principal.median())
print(
    "Moda:",
    (
        ingreso_principal.mode().iloc[0]
        if not ingreso_principal.mode().empty
        else "Sin moda"
    ),
)
print("Desviación Estándar:", ingreso_principal.std())
print("Mínimo:", ingreso_principal.min())
print("Máximo:", ingreso_principal.max())

# Medidas para 'TOTAL, DE HORAS TRABAJADAS'
print("\nMedidas Estadísticas para 'TOTAL, DE HORAS TRABAJADAS':")
horas_trabajadas = df["TOTAL, DE HORAS TRABAJADAS"].dropna()
print("Media:", horas_trabajadas.mean())
print("Mediana:", horas_trabajadas.median())
print(
    "Moda:",
    (
        horas_trabajadas.mode().iloc[0]
        if not horas_trabajadas.mode().empty
        else "Sin moda"
    ),
)
print("Desviación Estándar:", horas_trabajadas.std())
print("Mínimo:", horas_trabajadas.min())
print("Máximo:", horas_trabajadas.max())

# ===============================
# Tablas de Frecuencia
# ===============================

# Tabla de frecuencia para la variable de género (asumiendo que '207. SEXO' es la columna correspondiente)
print("\nTabla de Frecuencia para '207. SEXO':")
print(df["207. SEXO"].value_counts())

# Si existe, tabla de frecuencia para 'Mes de la encuesta'
if "Mes de la encuesta" in df.columns:
    print("\nTabla de Frecuencia para 'Mes de la encuesta':")
    print(df["Mes de la encuesta"].value_counts())

# ===============================
# Detección de Outliers
# ===============================


# Función para detectar outliers utilizando el método IQR
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]


# Detectar y mostrar outliers para las columnas numéricas
numerical_cols = [
    "Ingreso Total Mensual",
    "Ingreso principal mensual",
    "TOTAL, DE HORAS TRABAJADAS",
]
for col in numerical_cols:
    outliers = detect_outliers(df, col)
    print(f"\nOutliers en la columna {col}:")
    print(outliers[[col]])

# ===============================
# Gráficos Estadísticos
# ===============================

# Gráfico de la distribución de 'Ingreso Total Mensual'
plt.figure(figsize=(10, 6))
sns.histplot(ingreso_total, kde=True, color="blue")
plt.title("Distribución de Ingreso Total Mensual")
plt.xlabel("Ingreso Total Mensual")
plt.ylabel("Frecuencia")
plt.xticks(rotation=45)
plt.show()

# Gráfico de barras de la distribución por género
plt.figure(figsize=(6, 6))
sns.countplot(x="207. SEXO", data=df, palette="Set2")
plt.title("Distribución por Género")
plt.xlabel("Sexo")
plt.ylabel("Frecuencia")
plt.xticks(rotation=45)
plt.show()

# Gráfico de dispersión entre 'Ingreso Total Mensual' y 'TOTAL, DE HORAS TRABAJADAS'
plt.figure(figsize=(10, 6))
sns.scatterplot(x="TOTAL, DE HORAS TRABAJADAS", y="Ingreso Total Mensual", data=df)
plt.title("Relación entre Ingreso Total Mensual y Horas Trabajadas")
plt.xlabel("Horas Trabajadas")
plt.ylabel("Ingreso Total Mensual")
plt.xticks(rotation=45)
plt.show()

# Gráfico de caja para analizar la distribución de ingresos por género
plt.figure(figsize=(8, 6))
sns.boxplot(x="207. SEXO", y="Ingreso Total Mensual", data=df)
plt.title("Ingreso Total Mensual por Género")
plt.xlabel("Sexo")
plt.ylabel("Ingreso Total Mensual")
plt.xticks(rotation=45)
plt.show()

# Análisis de tendencias temporales: evolución del 'Ingreso Total Mensual' a lo largo del tiempo
if "Año de la encuesta" in df.columns and "Mes de la encuesta" in df.columns:
    df["Fecha"] = pd.to_datetime(
        df["Año de la encuesta"].astype(str)
        + "-"
        + df["Mes de la encuesta"].astype(str),
        format="%Y-%m",
    )
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="Fecha", y="Ingreso Total Mensual")
    plt.title("Tendencia de Ingreso Total Mensual a lo largo del Tiempo")
    plt.xlabel("Fecha")
    plt.ylabel("Ingreso Total Mensual")
    plt.xticks(rotation=45)
    plt.show()


# Definir la matriz de operacionalización
data_matrix = {
    "Variable Teórica": [
        "Ingreso Total Mensual", 
        "Ingreso Principal Mensual", 
        "Horas Trabajadas", 
        "Género"
    ],
    "Definición Conceptual": [
        "Total de ingresos percibidos mensualmente por el trabajador",
        "Ingreso predominante del trabajador",
        "Número total de horas trabajadas en el periodo evaluado",
        "Sexo del trabajador"
    ],
    "Variable Operacional": [
        "Ingreso Total Mensual",
        "Ingreso principal mensual",
        "TOTAL, DE HORAS TRABAJADAS",
        "207. SEXO"
    ],
    "Indicador": [
        "Monto monetario", 
        "Monto monetario", 
        "Número de horas", 
        "Categórico"
    ],
    "Unidad de Medición": [
        "Soles", 
        "Soles", 
        "Horas", 
        "-"
    ],
    "Fuente": [
        "Encuesta Nacional de Hogares (INEI)",
        "Encuesta Nacional de Hogares (INEI)",
        "Encuesta Nacional de Hogares (INEI)",
        "Encuesta Nacional de Hogares (INEI)"
    ]
}
matrix_df = pd.DataFrame(data_matrix)

# Función para envolver el texto de una celda
def wrap_cell(text, width=40):
    return textwrap.fill(text, width=width)

# Aplicar envoltura a las columnas con textos largos (por ejemplo, "Definición Conceptual")
matrix_df["Definición Conceptual"] = matrix_df["Definición Conceptual"].apply(lambda x: wrap_cell(x, width=40))

# Crear el plot para la tabla
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')
ax.axis('tight')

# Establecer ancho de columna (se ajusta según la cantidad de columnas)
col_widths = [0.18] * len(matrix_df.columns)

# Crear la tabla en el plot
table = ax.table(cellText=matrix_df.values,
                 colLabels=matrix_df.columns,
                 cellLoc='center',
                 colWidths=col_widths,
                 loc='center')

# Ajustar la fuente y escala para mejorar la visibilidad
table.auto_set_font_size(False)
table.set_fontsize(7)
table.scale(1.2, 1.5)

ax.set_title("Matriz de Operacionalización", pad=20, fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()