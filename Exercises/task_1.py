import matplotlib.pyplot as plt

# === 1. DATOS DE LA TABLA ===
total_estudiantes = 80

# Representación de la tabla original en forma de lista de listas
table_data = [
    ["", "Python", "Java", "C++", "TOTAL"],
    ["Ing. Sist. e Inform.", 15, 19, 2, 36],
    ["Ing. Software", 22, 16, 6, 44],
    ["TOTAL", 37, 35, 8, 80]
]

# === 2. CÁLCULOS DE PROBABILIDADES ===

# a) P(Ing. de Software y Java)
ing_software_java = 16
p_software_java = ing_software_java / total_estudiantes  # 16/80

# b) P(Python o Ing. de Sistemas e Informática)
python_total = 15 + 22        # 37
ing_sist_total = 15 + 19 + 2  # 36
interseccion = 15             # Ing. Sist. e Inform. que usan Python
p_python_ing_sist = (python_total + ing_sist_total - interseccion) / total_estudiantes
# (37 + 36 - 15) / 80 => 58/80

# c) P(No utiliza C++)
cpp_total = 2 + 6   # 8
p_no_cpp = 1 - (cpp_total / total_estudiantes  )  # 1 - 8/80 = 72/80

# === 3. IMPRESIÓN DE RESULTADOS EN CONSOLA ===
print("Resultados:")
print(f"a) P(Ing. Software y Java)           = {p_software_java:.3f} (≈ {p_software_java*100:.1f}%)")
print(f"b) P(Python o Ing. Sistemas)         = {p_python_ing_sist:.3f} (≈ {p_python_ing_sist*100:.1f}%)")
print(f"c) P(No usa C++)                     = {p_no_cpp:.3f} (≈ {p_no_cpp*100:.1f}%)")

# === 4. GRAFICACIÓN CON MATPLOTLIB ===
# Se utilizan subplots: en la parte superior (ax_bar) un gráfico de barras,
# y en la parte inferior (ax_table) la tabla con los datos originales.

fig, (ax_bar, ax_table) = plt.subplots(
    nrows=2,
    figsize=(9, 8),  # Ajusta el tamaño total de la figura
    gridspec_kw={"height_ratios": [2, 1.2]}  # Dar algo más de espacio a la tabla
)

# Título principal de la figura
fig.suptitle("Probabilidades y Distribución de 80 Estudiantes (UTP)",
             fontsize=14, fontweight='bold', y=0.98)

# =============== PARTE 1: GRÁFICO DE BARRAS =============== #
# 4.1. Preparar datos y dibujar barras
labels = ["a)", "b)", "c)"]
probabilidades = [p_software_java, p_python_ing_sist, p_no_cpp]
colors = ["#4CAF50", "#2196F3", "#FF9800"]

barras = ax_bar.bar(labels, probabilidades, color=colors)

# 4.2. Ajustes del gráfico
ax_bar.set_ylim(0, 1.05)         # Para que el eje Y llegue hasta un poco más del 100%
ax_bar.set_ylabel("Probabilidad", fontsize=11)
ax_bar.set_title("a), b), c) - Probabilidades de Eventos", fontsize=12, pad=10)

# 4.3. Colocar el porcentaje encima de cada barra
for bar in barras:
    altura = bar.get_height()
    ax_bar.text(
        bar.get_x() + bar.get_width() / 2,
        altura + 0.01,
        f"{altura*100:.1f}%",
        ha='center', va='bottom', fontsize=10
    )

# 4.4. Recuadro: Interpretación detallada
interpretacion_text = (
    "Interpretación:\n"
    "a) (Ing. Software & Java): De los 80 estudiantes,\n"
    "   16 pertenecen a Ing. Software y usan Java.\n"
    "b) (Python O Ing. Sist.): Combina quienes usan Python (37)\n"
    "   o pertenecen a Ing. de Sistemas (36), restando la intersección (15).\n"
    "c) (No usa C++): Excluye a los 8 estudiantes que usan C++,\n"
    "   quedando 72 que no lo utilizan."
)
ax_bar.text(
    1.03, 0.94,
    interpretacion_text,
    transform=ax_bar.transAxes,
    fontsize=9,
    bbox=dict(boxstyle="round,pad=0.4", fc="lightyellow", ec="black", alpha=0.9)
)

# 4.5. Recuadro: Procedimiento matemático
procedimiento_text = (
    "Procedimientos:\n"
    "a) 16/80 = 0.20\n"
    "b) (37 + 36 - 15)/80 = 58/80 = 0.725\n"
    "c) 1 - 8/80 = 72/80 = 0.90"
)
ax_bar.text(
    1.03, 0.52,
    procedimiento_text,
    transform=ax_bar.transAxes,
    fontsize=9,
    bbox=dict(boxstyle="round,pad=0.4", fc="lightcyan", ec="black", alpha=0.9)
)

# =============== PARTE 2: TABLA COMPLETA =============== #
# 4.6. Crear la tabla en ax_table
ax_table.set_axis_off()  # Ocultamos ejes para que solo se vea la tabla
the_table = ax_table.table(
    cellText=table_data,
    loc="center",
    cellLoc="center",
    colLabels=None  # La primera fila de table_data ya contiene los encabezados
)

# Ajustar el tamaño del texto en la tabla y las columnas
the_table.auto_set_font_size(False)
the_table.set_fontsize(10)
the_table.auto_set_column_width(col=list(range(len(table_data[0]))))

# Título de la tabla
ax_table.set_title(
    "Distribución de estudiantes por carrera y lenguaje de programación",
    fontsize=12, pad=10
)

# Ajuste final del layout para evitar que se superpongan elementos
plt.tight_layout(h_pad=2)
plt.show()
