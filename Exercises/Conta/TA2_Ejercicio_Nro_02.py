# ejercicio_4.py
import os
import pandas as pd

# 1) Datos del Estado de Resultados comparativo 2020 vs 2019
rows = [
    ("Ventas netas",                    42018964, 31668969),
    ("(-) Costo de ventas",            21935576, 16970746),
    ("UTILIDAD BRUTA",                 20083388, 14698223),
    ("(-) Gasto de ventas",             3904772,  3561789),
    ("(-) Gasto de administración",     4545854,  3549029),
    ("UTILIDAD OPERATIVA",             11632762,  7587405),
    ("",                                     "",         ""),
    ("OTROS INGRESOS Y/O EGRESOS",     "",         ""),
    ("Ingresos financieros",             175207,     97132),
    ("(-) Gastos financieros",           765665,    493666),
    ("Ingresos diversos",                355231,    277234),
    ("(-) Gastos diversos",              205343,    542540),
    ("UTILIDAD ANTES IMPTO. RENTA",    11192192,  6925565),
    ("Impuesto a la renta",             3301697,   2043042),
    ("UTILIDAD NETA",                   7890495,   4882523)
]
df_states = pd.DataFrame(rows, columns=["Cuenta", "2020", "2019"])

# 2) RESOLUCIÓN: fórmulas de Excel para análisis vertical y guía horizontal
res = [
    ("RESOLUCIÓN:",                                        "",     ""),
    ("",                                                   "",     ""),
    # Vertical 2020
    ("1) Análisis Vertical 2020",                          "",     ""),
    ("Base Ventas Netas",                                 "=$B$2", ""),
    ("(-) Costo de ventas",                              "=$B$3/$B$2", ""),
    ("UTILIDAD BRUTA",                                   "=$B$4/$B$2", ""),
    ("(-) Gasto de ventas",                              "=$B$5/$B$2", ""),
    ("(-) Gasto de administración",                      "=$B$6/$B$2", ""),
    ("UTILIDAD OPERATIVA",                               "=$B$7/$B$2", ""),
    ("",                                                   "",     ""),
    ("Ingresos financieros",                             "=$B$10/$B$2", ""),
    ("(-) Gastos financieros",                           "=$B$11/$B$2", ""),
    ("Ingresos diversos",                                "=$B$12/$B$2", ""),
    ("(-) Gastos diversos",                              "=$B$13/$B$2", ""),
    ("UTILIDAD ANTES IMPTO. RENTA",                      "=$B$14/$B$2", ""),
    ("Impuesto a la renta",                              "=$B$15/$B$2", ""),
    ("UTILIDAD NETA",                                    "=$B$16/$B$2", ""),
    ("",                                                   "",     ""),
    # Vertical 2019
    ("2) Análisis Vertical 2019",                          "",     ""),
    ("Base Ventas Netas",                                 "=$C$2", ""),
    ("(-) Costo de ventas",                              "=$C$3/$C$2", ""),
    ("UTILIDAD BRUTA",                                   "=$C$4/$C$2", ""),
    ("(-) Gasto de ventas",                              "=$C$5/$C$2", ""),
    ("(-) Gasto de administración",                      "=$C$6/$C$2", ""),
    ("UTILIDAD OPERATIVA",                               "=$C$7/$C$2", ""),
    ("",                                                   "",     ""),
    ("Ingresos financieros",                             "=$C$10/$C$2", ""),
    ("(-) Gastos financieros",                           "=$C$11/$C$2", ""),
    ("Ingresos diversos",                                "=$C$12/$C$2", ""),
    ("(-) Gastos diversos",                              "=$C$13/$C$2", ""),
    ("UTILIDAD ANTES IMPTO. RENTA",                      "=$C$14/$C$2", ""),
    ("Impuesto a la renta",                              "=$C$15/$C$2", ""),
    ("UTILIDAD NETA",                                    "=$C$16/$C$2", ""),
    ("",                                                   "",     ""),
    # Guía Análisis Horizontal
    ("3) Análisis Horizontal del ER",                     "",     ""),
    ("* Variación absoluta: =B2-C2",                       "",     ""),
    ("* Variación %: =(B2-C2)/C2",                        "",     "")
]

df_res = pd.DataFrame(res, columns=df_states.columns)

# 3) Concatenar y exportar todo en un único CSV
df_final = pd.concat([df_states, df_res], ignore_index=True)

script_dir  = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "TA2_Ejercicio_Nro_02.csv")

df_final.to_csv(
    output_path,
    sep=";",             # usa punto y coma para que Excel ES/LA importe en celdas
    decimal=",",         # coma como separador decimal
    index=False,
    encoding="utf-8-sig" # BOM para acentos
)

print(f"✅ CSV generado en: {output_path}")
