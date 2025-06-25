# ejercicio_3.py
import os
import pandas as pd

# 1) Datos del Estado de Situación Financiera de EL DORADO S.R.L.
left = [
    ("Activo corriente",               ""),
    ("Caja y Bancos (1)",           50000.00),
    ("Cuentas por cobrar (2)",      40000.00),
    ("Mercaderías (3)",             90000.00),
    ("Anticipo a proveedores (4)",   2000.00),
    ("Total activo corriente",     182000.00),
    ("",                                ""),
    ("Activo no corriente",            ""),
    ("Inmuebles, maq y equip. (5)", 10000.00),
    ("Depreciación acumulada (6)",  -1000.00),
    ("Total activo no corriente",    9000.00),
    ("",                                ""),
    ("Total activo",              191000.00)
]

right = [
    ("Pasivo corriente",               ""),
    ("Tributos por pagar (7)",       5000.00),
    ("Remuneraciones por pagar (8)",10000.00),
    ("Cuentas por pagar (9)",       30000.00),
    ("Anticipo de clientes (10)",    1000.00),
    ("Total pasivo corriente",      46000.00),
    ("",                                ""),
    ("Pasivo no corriente",            ""),
    ("Obligaciones financieras (11)",35000.00),
    ("Total pasivo no corriente",    35000.00),
    ("",                                ""),
    ("Total pasivo",               81000.00),
    ("",                                ""),
    ("Patrimonio neto",                ""),
    ("Capital social (12)",         30000.00),
    ("Utilidad del ejercicio (13)",80000.00),
    ("Total patrimonio neto",      110000.00),
    ("",                                ""),
    ("Total pasivo y patrimonio",  191000.00)
]

df_left  = pd.DataFrame(left,  columns=["Activo", "Monto"])
df_right = pd.DataFrame(right, columns=["Pasivo", "Monto"])
df_estados = pd.concat([df_left, df_right], axis=1)

# 2) RESOLUCIÓN: Análisis Vertical (con fórmulas de Excel) y guía Horizontal
res = [
    ("RESOLUCIÓN:",                             "",           "",        ""),
    ("",                                        "",           "",        ""),
    ("1) Análisis Vertical del Balance",        "",           "",        ""),
    # Base Activos = Total activo (celda B14 en Excel)
    ("Base Activos",                            "=$B$14",     "",        ""),
    ("Caja y Bancos (1)",                       "=$B$2/$B$14", "",       ""),
    ("Cuentas por cobrar (2)",                  "=$B$3/$B$14", "",       ""),
    ("Mercaderías (3)",                         "=$B$4/$B$14", "",       ""),
    ("Anticipo a proveedores (4)",              "=$B$5/$B$14", "",       ""),
    ("Total activo corriente",                  "=$B$6/$B$14", "",       ""),
    ("Inmuebles, maq y equip. (5)",             "=$B$9/$B$14", "",       ""),
    ("Depreciación acumulada (6)",              "=$B$10/$B$14","",       ""),
    ("Total activo no corriente",               "=$B$11/$B$14","",       ""),
    ("Total activo",                            "=$B$14/$B$14","",       ""),
    ("",                                        "",           "",        ""),
    ("2) Análisis Vertical de Pasivo y Patrimonio","",         "",        ""),
    # Base Pasivo y Patrimonio = Total pasivo y patrimonio (celda D20)
    ("Base Pasivo y Patrimonio",                "=$D$20",     "",        ""),
    ("Tributos por pagar (7)",                  "=$D$2/$D$20", "",      ""),
    ("Remuneraciones por pagar (8)",            "=$D$3/$D$20", "",      ""),
    ("Cuentas por pagar (9)",                   "=$D$4/$D$20", "",      ""),
    ("Anticipo de clientes (10)",               "=$D$5/$D$20", "",      ""),
    ("Total pasivo corriente",                  "=$D$6/$D$20", "",      ""),
    ("Obligaciones financieras (11)",           "=$D$9/$D$20", "",      ""),
    ("Total pasivo no corriente",               "=$D$10/$D$20","",      ""),
    ("Total pasivo",                            "=$D$12/$D$20","",      ""),
    ("Capital social (12)",                     "=$D$14/$D$20","",      ""),
    ("Utilidad del ejercicio (13)",             "=$D$15/$D$20","",      ""),
    ("Total patrimonio neto",                   "=$D$16/$D$20","",      ""),
    ("Total pasivo y patrimonio",               "=$D$20/$D$20","",      ""),
    ("",                                        "",           "",        ""),
    ("3) Análisis Horizontal del Balance",      "* Requiere saldos comparativos del ejercicio anterior", "", "")
]
df_res = pd.DataFrame(res, columns=df_estados.columns)

# 3) Concatenar y exportar todo en un único CSV
df_final = pd.concat([df_estados, df_res], ignore_index=True)

script_dir  = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "TA2_Ejercicio_Nro_01.csv")

df_final.to_csv(
    output_path,
    sep=";",             # punto y coma para Excel locales ES/LA
    decimal=",",         # coma como separador decimal
    index=False,
    encoding="utf-8-sig" # BOM para acentos
)

print(f"✅ CSV con el Estado de Situación y Análisis generado en: {output_path}")
