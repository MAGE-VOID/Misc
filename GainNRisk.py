import os
import pandas as pd
from openpyxl import load_workbook

# FACTORES DE CONVERSIÓN
# En una cuenta cent: 10 USD normal = 1000 cent, es decir, 1 USD normal = 100 cent.
currency_conversion_factor = 100
# En la cuenta cent se opera con lotes 10 veces mayores para tener el mismo riesgo/exposición que en una cuenta normal.
lot_conversion_factor = 10

# PARÁMETROS BASE
# Aunque el mínimo lote permitido en una cuenta cent es 0.01,
# para obtener la misma exposición que en una cuenta normal (0.01 lote) se utiliza 0.1 lote en cuenta cent.
base_lot_cent = 0.1  # Lote base en cuenta cent equivalente a 0.01 lote en cuenta normal.
base_gain_normal_usd = 2000   # Ganancia de 2000 USD por operar 0.01 lote en cuenta normal.
base_risk_normal_usd = 55000   # Drawdown máximo de 55000 USD por operar 0.01 lote en cuenta normal.

# Convertir las magnitudes a unidades de cuenta cent (centavos)
base_gain_cent = base_gain_normal_usd * currency_conversion_factor     # 2000 USD * 100 = 200000 cent
base_risk_cent = base_risk_normal_usd * currency_conversion_factor     # 55000 USD * 100 = 5500000 cent

# DEPÓSITO
# Definir el depósito inicial en USD normales y su equivalente en centavos.
deposit_normal_usd = 6000  # Puedes modificar este valor según sea necesario.
deposit_cent = deposit_normal_usd * currency_conversion_factor

# LISTA DE TAMAÑOS DE LOTE (en cuenta cent)
lot_sizes = [0.01, 0.02, 0.03, 0.04, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
             0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.50, 2.00, 2.50, 3.00,
             3.50, 4.00, 4.50, 5.00]

# CÁLCULO DE MÉTRICAS
# Los cálculos se hacen sobre la base de que:
#   Ganancia (centavos) = (lote / base_lot_cent) * base_gain_cent
#   Riesgo (centavos)  = (lote / base_lot_cent) * base_risk_cent
# Además, se añade la equivalencia en lotes de cuenta normal: lote_equiv_normal = lote / lot_conversion_factor
# Se calcula además el balance restante y el balance relativo (%), restando el riesgo del depósito.
data = {
    "Depósito (USD Normal)": [deposit_normal_usd] * len(lot_sizes),
    "Depósito (USD Centavos)": [deposit_cent] * len(lot_sizes),
    "Lote (Cuenta Cent)": lot_sizes,
    "Lote Equivalente (Cuenta Normal)": [round(x / lot_conversion_factor, 4) for x in lot_sizes],
    "Ganancias Mensuales (centavos)": [round((x / base_lot_cent) * base_gain_cent, 2) for x in lot_sizes],
    "Ganancias Mensuales (USD)": [round(((x / base_lot_cent) * base_gain_cent) / currency_conversion_factor, 2) for x in lot_sizes],
    "Riesgo Máximo (centavos)": [round((x / base_lot_cent) * base_risk_cent, 2) for x in lot_sizes],
    "Riesgo Máximo (USD)": [round(((x / base_lot_cent) * base_risk_cent) / currency_conversion_factor, 2) for x in lot_sizes],
    "Balance Restante (centavos)": [round(deposit_cent - ((x / base_lot_cent) * base_risk_cent), 2) for x in lot_sizes],
    "Balance Restante (USD)": [round(deposit_normal_usd - (((x / base_lot_cent) * base_risk_cent) / currency_conversion_factor), 2) for x in lot_sizes],
    "Balance Relativo (%)": [round(((deposit_cent - ((x / base_lot_cent) * base_risk_cent)) / deposit_cent * 100), 2) for x in lot_sizes]
}

df = pd.DataFrame(data)

# ESPECIFICA LA RUTA PARA GUARDAR EL ARCHIVO
directorio = r"G:\Desktop"
if not os.path.exists(directorio):
    os.makedirs(directorio)

file_path = os.path.join(directorio, "Ganancias_y_Riesgo_Trading.xlsx")

# Guarda el DataFrame en un archivo Excel
df.to_excel(file_path, index=False)

# AJUSTE DE ANCHO DE COLUMNAS USANDO openpyxl
wb = load_workbook(file_path)
ws = wb.active

for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter
    for cell in col:
        if cell.value is not None:
            max_length = max(max_length, len(str(cell.value)))
    adjusted_width = max_length + 2
    ws.column_dimensions[col_letter].width = adjusted_width

wb.save(file_path)

print(f"Archivo guardado en {file_path}")
