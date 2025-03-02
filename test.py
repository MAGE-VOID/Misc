import matplotlib.pyplot as plt

# Configurar la figura y el eje
fig, ax = plt.subplots(figsize=(8, 2))

# Dibujar la línea de la recta numérica
ax.hlines(1, 20, 40, colors='black')  # línea horizontal desde 20 hasta 40

# Marcar el 25 con un punto sólido
ax.plot(25, 1, 'ko', markersize=8)

# Dibujar una flecha que indica que el intervalo se extiende a la derecha
ax.annotate('', xy=(40, 1), xytext=(25, 1), arrowprops={'arrowstyle':'->', 'color':'black'})

# Añadir etiquetas y ajustar límites
ax.text(25, 1.1, '25', horizontalalignment='center')
ax.set_xlim(20, 42)
ax.set_ylim(0.8, 1.2)
ax.axis('off')  # Ocultar ejes para mostrar solo la recta numérica

plt.title('Representación del intervalo [25, ∞)')
plt.show()
