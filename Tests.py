import pandas as pd

# Define the lot sizes
lot_sizes = [0.01, 0.02, 0.03, 0.04, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
             0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.50, 2.00, 2.50, 3.00,
             3.50, 4.00, 4.50, 5.00]

# Base values for gains and risk
base_gains = 1200  # Base gain for 0.01 lots in cents
base_risk = 30000  # Base risk for 0.01 lots in cents

# Create the DataFrame
data = {
    "Tamaño del Lote": lot_sizes,
    "Ganancias Mensuales (centavos)": [x * base_gains for x in lot_sizes],
    "Ganancias Mensuales (USD)": [x * base_gains / 100 for x in lot_sizes],
    "Riesgo Máximo (centavos)": [x * base_risk for x in lot_sizes],
    "Riesgo Máximo (USD)": [x * base_risk / 100 for x in lot_sizes]
}

df = pd.DataFrame(data)

# Save the DataFrame to an Excel file on the desktop
file_path = "C:\\Users\\Arthur G\\Desktop\\Ganancias_y_Riesgo_Trading.xlsx"
df.to_excel(file_path, index=False)

print(f"Archivo guardado en {file_path}")
