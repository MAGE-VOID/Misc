import pandas as pd


def calcular_ganancias(
    inversiones, ganancia_mensual, porcentaje_ganancia=0.25, inversion_base=30000
):
    """
    Calcula las ganancias para cada inversor basadas en su proporción de inversión con respecto a un capital base.

    :param inversiones: Lista de inversiones de los inversores.
    :param ganancia_mensual: Ganancia total mensual generada por el robot.
    :param porcentaje_ganancia: Porcentaje de la ganancia mensual que se distribuye a los inversores.
    :param inversion_base: Monto de inversión que se considera para el cálculo base.
    :return: Lista de ganancias para cada inversor.
    """
    if ganancia_mensual <= 0:
        raise ValueError(
            "La ganancia mensual debe ser un valor positivo mayor que cero."
        )

    if any(inv < 0 for inv in inversiones):
        raise ValueError("Las inversiones no pueden ser negativas.")

    if not inversiones:
        raise ValueError("La lista de inversiones no puede estar vacía.")

    total_participacion = sum(min(inv / inversion_base, 1) for inv in inversiones)
    if total_participacion == 0:
        raise ValueError("El total de participación no puede ser cero.")

    ganancias = [
        (ganancia_mensual * min(inv / inversion_base, 1) / total_participacion)
        * porcentaje_ganancia
        for inv in inversiones
    ]

    return ganancias


# Capital de los inversores en una lista
inversiones = [
    78700,
]

# Ganancia mensual generada por el robot en un mes
ganancia_mensual = 3000  # Asumiendo un promedio de ganancia mensual del robot

try:
    # Calcular las ganancias de los inversores
    ganancias = calcular_ganancias(inversiones, ganancia_mensual)

    # Crear DataFrame para los resultados
    data = {
        "Inversor": [f"Inversor {i+1}" for i in range(len(inversiones))] + ["Total"],
        "Monto": inversiones + [sum(inversiones)],
        "Ganancia": [round(g, 2) for g in ganancias] + [round(sum(ganancias), 2)],
        "Ganancia Mensual %": [(g / ganancia_mensual) * 100 for g in ganancias]
        + [round((sum(ganancias) / ganancia_mensual) * 100, 2)],
        "Monto Invertido %": [
            (g / i) * 100 if i != 0 else 0 for g, i in zip(ganancias, inversiones)
        ]
        + [sum(g / i * 100 for g, i in zip(ganancias, inversiones)) / len(inversiones)],
    }
    df = pd.DataFrame(data)
    print(
        df.to_string(
            index=False,
            formatters={
                "Ganancia": "${:,.2f}".format,
                "Ganancia Mensual %": "{:.2f}%".format,
                "Monto Invertido %": "{:.2f}%".format,
            },
        )
    )

    # Calcular y mostrar la ganancia del creador y su porcentaje
    ganancia_creador = ganancia_mensual - sum(ganancias)
    porcentaje_creador = (ganancia_creador / ganancia_mensual) * 100
    print(f"Ganancia del Creador: ${ganancia_creador:.2f} ({porcentaje_creador:.2f}%)")

except ValueError as e:
    print(e)
