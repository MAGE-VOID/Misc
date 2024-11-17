def calcular_planchas(
    kills_favor, kills_contra, victorias, planchas_min=1, planchas_max=10
):

    balance_muertes = kills_favor - kills_contra
    print(f"Diferencia de muertes: {balance_muertes}")

    if victorias == 0:
        if balance_muertes < -20:
            incremento = abs(balance_muertes) // 2
            planchas = min(planchas_max, planchas_min + incremento)
            print(f"Derrota abrumadora, penalización aplicada: {incremento} planchas")
        elif balance_muertes <= -10:
            incremento = abs(balance_muertes) // 4
            planchas = min(planchas_max, planchas_min + incremento)
            print(f"Derrota normal, penalización aplicada: {incremento} planchas")
        elif balance_muertes > 10:
            planchas = planchas_max - 1
            print(f"Perdiste con ventaja, eres un nub. Reducción aplicada: 1 plancha")
        elif balance_muertes > 0:
            reduccion = balance_muertes // 10
            planchas = max(planchas_min, planchas_max - reduccion)
            print(f"Reducción mínima por más kills en derrota: {reduccion} planchas")
        else:
            planchas = planchas_max - 2
            print("Partida reñida, aplicando penalización cercana al máximo")
    else:
        planchas = max(planchas_min, planchas_max - victorias)
        print(f"Planchas reducida por {victorias} victoria(s): {planchas} planchas")

    if victorias > 0:
        descuento_por_victorias = 0.17 * victorias
        planchas_final = max(planchas_min, planchas - descuento_por_victorias)
        print(f"Dscto por {victorias} win seguida: {descuento_por_victorias} planchas")
    else:
        planchas_final = planchas

    return planchas_final


# Inputs
victorias = 0  # Victorias consecutivas
kills_favor = 31
kills_contra = 55
planchas_a_realizar = calcular_planchas(kills_favor, kills_contra, victorias)
print(f"Planchas a realizar: {round(planchas_a_realizar, 2)}")
