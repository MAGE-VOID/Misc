# ejercicio_1.py
import os
import pandas as pd

# 1) Datos del Estado de Situación Financiera (15 filas)
left = [
    ("Activos corrientes", ""),
    ("Efectivo", 32000),
    ("Cuentas por cobrar clientes", 15000),
    ("Anticipos a proveedores", 1000),
    ("Inventario", 30200),
    ("", ""),
    ("Total activos corrientes", 78200),
    ("", ""),
    ("Activos no corrientes", ""),
    ("Propiedad, planta y equipo", 100000),
    ("Depreciación acumulada", 8000),
    ("Total activos no corrientes", 92000),
    ("Total Activos", 170200),
    ("", ""),
    ("", "")
]
right = [
    ("Pasivo corriente", ""),
    ("Proveedores por pagar", 50000),
    ("Impuestos por pagar", 10000),
    ("Otros cuentas por pagar", 1000),
    ("Total pasivos corrientes", 61000),
    ("", ""),
    ("Pasivo no corrientes", 97000),
    ("Total pasivos", 158000),
    ("", ""),
    ("Capital contable", ""),
    ("Capital pagado", 10000),
    ("Utilidades retenidas", 2200),
    ("Total capital contable", 12200),
    ("", ""),
    ("Total pasivo y capital", 170200)
]

df_left  = pd.DataFrame(left,  columns=["Activo", "Monto"])
df_right = pd.DataFrame(right, columns=["Pasivo", "Monto"])
df_estados = pd.concat([df_left, df_right], axis=1)

# 2) Filas RESOLUCIÓN con fórmulas de Excel para Análisis Vertical
#    Excel interpretará como fórmula las cadenas que empiecen por "=" al abrir el CSV.
res = [
    ("RESOLUCIÓN:",      "",           "",        ""),
    ("",                 "",           "",        ""),
    ("1) Análisis Vertical del Balance", "",      "",        ""),
    # Base Activos
    ("Base Activos",     "=$B$14",     "",        ""),
    # Vertical Activo
    ("Efectivo",         "=$B$3/$B$14", "",       ""),
    ("Cuentas por cobrar clientes", "=$B$4/$B$14", "", ""),
    ("Anticipos a proveedores",     "=$B$5/$B$14", "", ""),
    ("Inventario",       "=$B$6/$B$14", "",       ""),
    ("Total activos corrientes", "=$B$8/$B$14", "",   ""),
    ("Propiedad, planta y equipo", "=$B$11/$B$14", "", ""),
    ("Depreciación acumulada", "=$B$12/$B$14", "",      ""),
    ("Total activos no corrientes", "=$B$13/$B$14", "", ""),
    ("",                 "",           "",        ""),
    # Vertical Pasivo & Capital
    ("2) Análisis Vertical de Pasivo y Capital", "", "", ""),
    ("Base Pasivo y Capital", "=$D$16",    "",        ""),
    ("Proveedores por pagar", "=$D$3/$D$16", "",      ""),
    ("Impuestos por pagar",   "=$D$4/$D$16", "",      ""),
    ("Otros cuentas por pagar","=$D$5/$D$16", "",     ""),
    ("Total pasivos corrientes","=$D$6/$D$16", "",    ""),
    ("Pasivo no corrientes",   "=$D$8/$D$16", "",     ""),
    ("Total pasivos",          "=$D$9/$D$16", "",     ""),
    ("Capital pagado",         "=$D$12/$D$16", "",    ""),
    ("Utilidades retenidas",   "=$D$13/$D$16", "",    ""),
    ("Total capital contable", "=$D$14/$D$16", "",    ""),
    ("",                 "",           "",        ""),
    # Guía Análisis Horizontal
    ("3) Análisis Horizontal del Balance", "",    "",        ""),
    ("* Requiere saldos ejercicio anterior", "",  "",        "")
]
df_res = pd.DataFrame(res, columns=df_estados.columns)

# 3) Concatenar y exportar todo en un único CSV
df_final = pd.concat([df_estados, df_res], ignore_index=True)

script_dir  = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "TA2_Ejercicio_Nro_04.csv")

df_final.to_csv(
    output_path,
    sep=";",             # punto y coma para que Excel ES/LA separe en celdas
    decimal=",",         # separador decimal
    index=False,
    encoding="utf-8-sig" # BOM para acentos
)

print(f"✅ CSV con fórmulas generado en: {output_path}")
