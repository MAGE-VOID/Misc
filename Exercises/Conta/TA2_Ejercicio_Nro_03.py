# ejercicio_2.py
import os
import pandas as pd

# 1) Datos del Estado de Resultados (12 filas)
rows = [
    ("Ingresos operacionales",       81000000),
    ("Costo de ventas",              45000000),
    ("UTILIDAD BRUTA",               36000000),
    ("Gastos operacionales",             40000),
    ("UTILIDAD OPERACIONAL",         35960000),
    ("Gastos financieros",               30000),
    ("Ingresos no operacionales",        6000),
    ("UTILIDAD ANTES DE IMPUESTOS",  35936000),
    ("Provisión para impuestos",     12577600),
    ("UTILIDAD NETA",                23358400),
    ("Reserva legal",                 2335840),
    ("UTILIDAD DISPONIBLE PARA SOCIOS", 21022560)
]

df_states = pd.DataFrame(rows, columns=["Cuenta", "Monto"])

# 2) Filas RESOLUCIÓN con fórmulas de Excel para Análisis Vertical y guía de Horizontal
#    Las cadenas que empiezan por "=" se importan como fórmulas en Excel.
res = [
    ("RESOLUCIÓN:",                                  ""),
    ("",                                             ""),
    ("1) Análisis Vertical del Estado de Resultados", ""),
    ("Base Ventas Netas",                           "=$B$2"),
    ("Costo de ventas",                             "=$B$3/$B$2"),
    ("UTILIDAD BRUTA",                              "=$B$4/$B$2"),
    ("Gastos operacionales",                        "=$B$5/$B$2"),
    ("UTILIDAD OPERACIONAL",                        "=$B$6/$B$2"),
    ("Gastos financieros",                          "=$B$7/$B$2"),
    ("Ingresos no operacionales",                   "=$B$8/$B$2"),
    ("UTILIDAD ANTES DE IMPUESTOS",                 "=$B$9/$B$2"),
    ("Provisión para impuestos",                    "=$B$10/$B$2"),
    ("UTILIDAD NETA",                               "=$B$11/$B$2"),
    ("Reserva legal",                               "=$B$12/$B$2"),
    ("UTILIDAD DISPONIBLE PARA SOCIOS",             "=$B$13/$B$2"),
    ("",                                             ""),
    ("2) Análisis Horizontal del Estado de Resultados",""),
    ("* Requiere saldos comparativos del ejercicio anterior","")
]

df_res = pd.DataFrame(res, columns=df_states.columns)

# 3) Concatenar y exportar todo en un único CSV
df_final = pd.concat([df_states, df_res], ignore_index=True)

script_dir  = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "TA2_Ejercicio_Nro_03.csv")

df_final.to_csv(
    output_path,
    sep=";",             # punto y coma para Excel ES/LA
    decimal=",",         # coma como separador decimal
    index=False,
    encoding="utf-8-sig" # BOM para acentos
)

print(f"✅ CSV con Análisis Vertical y guía Horizontal generado en: {output_path}")
