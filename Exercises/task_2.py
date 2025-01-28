import matplotlib.pyplot as plt

# ========= 1. DEFINICIÓN DE EVENTOS Y DATOS =========
# A = "Participar en una conferencia sobre IA"
# B = "Encontrarse con un docente de la UTP"

# Dado en el enunciado:
# P(A ∩ B) = 0.15   (15%)
# P(B)     = 0.90   (90%)

pA_and_B = 0.15
pB       = 0.90

# ========= 2. CÁLCULO DE LA PROBABILIDAD SOLICITADA =========
# Queremos: P(A | B) = P(A ∩ B) / P(B)
pA_given_B = pA_and_B / pB  # 0.15 / 0.90 = 0.1667 (16.67%)

# ========= 3. MOSTRAR RESULTADOS EN CONSOLA =========
print("Resultados:")
print(f"P(A ∩ B) = {pA_and_B:.2f}  (15%)")
print(f"P(B)      = {pB:.2f}      (90%)")
print(f"P(A | B)  = {pA_given_B:.4f}  (≈ {pA_given_B * 100:.2f}%)")

# ========= 4. GRAFICACIÓN CON MATPLOTLIB =========
# Para ilustrar las probabilidades, creamos un diagrama de barras sencillo.

labels = ["P(A ∩ B)", "P(B)", "P(A | B)"]
values = [pA_and_B, pB, pA_given_B]

# Aumentamos el tamaño de la figura para que haya suficiente espacio a la derecha
plt.figure(figsize=(9, 5))

bars = plt.bar(labels, values, color=["#2ca02c", "#1f77b4", "#ff7f0e"])

# Ajuste del eje Y para mostrar de 0 a 1
plt.ylim(0, 1.05)
plt.ylabel("Valor de la Probabilidad", fontsize=11)
plt.title("Probabilidades relacionadas con la Conferencia IA y Docente UTP",
          fontsize=13, fontweight='bold')

# Etiquetas de texto encima de cada barra (porcentajes)
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.02,
        f"{height * 100:.1f}%",
        ha='center', va='bottom', fontsize=10
    )

# Texto explicativo adicional:
explicacion = (
    "P(A ∩ B): Probabilidad de participar en\n"
    "          conferencia IA y encontrarse con\n"
    "          un docente de la UTP (15%).\n\n"
    "P(B):     Probabilidad de encontrarse con\n"
    "          un docente de la UTP en un día\n"
    "          cualquiera (90%).\n\n"
    "P(A | B): Probabilidad de haber participado\n"
    "          en la conferencia IA DADO que\n"
    "          se encontró con un docente UTP.\n"
    "          (Se calcula con P(A ∩ B) / P(B))"
)

# Ubicamos el texto en la parte derecha del gráfico (x>1)
plt.text(
    1.05, 0.5,
    explicacion,
    transform=plt.gca().transAxes,
    fontsize=9,
    va='center',  # Para que el cuadro se centre verticalmente en Y=0.5
    bbox=dict(boxstyle="round,pad=0.6", fc="lightyellow", ec="black", alpha=0.8)
)

# Ajustamos la distribución para que no se corte nada
plt.tight_layout(rect=[0, 0, 0.85, 1])  
# rect=[left, bottom, right, top] deja espacio a la derecha (0.85)

plt.show()
