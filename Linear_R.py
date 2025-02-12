import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# 1. Generar Serie con autocorrelación en los retornos
# Elimina o comenta la siguiente línea para que la simulación cambie cada vez:
# np.random.seed(42)  # reproducibilidad

n = 300
retornos = np.zeros(n)

# Retorno inicial
retornos[0] = 0.002

for t in range(1, n):
    retornos[t] = 0.4 * retornos[t-1] + np.random.normal(0, 0.001)

precios = 100 + np.cumsum(retornos)
df = pd.DataFrame({'precio': precios})

# 2. Calcular Retorno (% cambio)
df['retorno'] = df['precio'].pct_change()
df.dropna(inplace=True)

# 3. Crear Features (lags)
def crear_lags(serie, n_lags=3):
    df_lags = pd.DataFrame({'target': serie})
    for i in range(1, n_lags+1):
        df_lags[f'lag_{i}'] = df_lags['target'].shift(i)
    return df_lags

df_lags = crear_lags(df['retorno'], n_lags=3)
df_lags.dropna(inplace=True)

# 4. Separar en train/test
X = df_lags[['lag_1', 'lag_2', 'lag_3']].values
y = df_lags['target'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# 5. Entrenar el modelo de Ridge
model = Ridge(alpha=1.0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 6. Métrica: R² en test
r2 = r2_score(y_test, y_pred)
print(f'R² en el set de prueba: {r2:.4f}')

# 7. Graficar
plt.figure(figsize=(10, 5))
plt.plot(y_test, label='Retorno Real', marker='o')
plt.plot(y_pred, label='Retorno Predicho (Ridge)', marker='x')
plt.title('Comparación Retorno Real vs. Retorno Predicho (con autocorrelación)')
plt.xlabel('Índice de Tiempo (Test)')
plt.ylabel('Retorno')
plt.legend()
plt.tight_layout()
plt.show()
