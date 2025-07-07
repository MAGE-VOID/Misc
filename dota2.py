import requests


def obtener_detalles_match(match_id):
    """
    Consulta la API de OpenDota para obtener los detalles de un match.
    """
    url = f"https://api.opendota.com/api/matches/{match_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos del match {match_id}: {response.status_code}")
        return None


def obtener_detalles_jugador(account_id):
    """
    Consulta la API de OpenDota para obtener los datos de un jugador.
    """
    url = f"https://api.opendota.com/api/players/{account_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Error al obtener datos del jugador {account_id}: {response.status_code}"
        )
        return None


def obtener_ultimos_matches(account_id, limit=5):
    """
    Consulta la API de OpenDota para obtener las últimas 'limit' partidas jugadas por el jugador.
    Se utiliza el endpoint /players/{account_id}/matches, el cual permite especificar un límite.
    """
    url = f"https://api.opendota.com/api/players/{account_id}/matches?limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return (
            response.json()
        )  # Retorna una lista de diccionarios, cada uno representando un match
    else:
        print(
            f"Error al obtener las partidas para el jugador {account_id}: {response.status_code}"
        )
        return None


if __name__ == "__main__":
    # Reemplaza con un account_id válido
    my_account_id = 455391001

    # Lista de account IDs que queremos buscar en los matches (aparte del tuyo)
    target_accounts = [
        455391001,  # Ozo
        41242412,  # Fer
        387939600,  # Lofo
        149597815,  # Tot
    ]

    # (Opcional) Obtener y mostrar detalles del jugador
    datos_jugador = obtener_detalles_jugador(my_account_id)
    if datos_jugador:
        print("Detalles del jugador:")
        perfil = datos_jugador.get("profile", {})
        print("Nombre de usuario:", perfil.get("personaname"))
        print("Steam ID:", perfil.get("steamid"))

    # Obtener los últimos 100 match IDs del jugador
    print("\n=== Últimos 100 Match IDs ===")
    ultimos_matches = obtener_ultimos_matches(my_account_id, limit=100)
    if ultimos_matches:
        for match in ultimos_matches:
            print(match.get("match_id"))
    else:
        print("No se pudo obtener el historial de partidas.")
