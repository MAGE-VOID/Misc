import os
import requests
import pandas as pd

BASE_DIR = r"D:\FOREX\MT5_1\MQL5\Experts\Projects\Sharing-Projects\Misc\Dota2"

target_accounts = {
    455391001: "Ozo",
    41242412:  "Fer",
    387939600: "Lofo",
    149597815: "Tot",
    46415099: "Limon",
}

def obtener_ultimos_matches(account_id, limit=100):
    url = f"https://api.opendota.com/api/players/{account_id}/matches?limit={limit}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else []

def obtener_detalles_match(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def analizar_partidas(account_id, limit=100):
    partidas = obtener_ultimos_matches(account_id, limit)
    if not partidas:
        print(f"No se recibieron partidas para {account_id}.")
        return None

    df = pd.DataFrame(partidas)

    # 1) Win/Loss
    df['win'] = df.apply(
        lambda r: (r['player_slot'] < 128 and r['radiant_win'])
                  or (r['player_slot'] >= 128 and not r['radiant_win']),
        axis=1
    )

    # 2) Convertir o crear columnas numéricas sin generar FutureWarning
    numeric_cols = ['version','leaver_status','party_size','hero_variant','average_rank']
    for col in numeric_cols:
        if col in df.columns:
            # convierto a numérico, relleno NA con 0 y paso a int
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        else:
            df[col] = 0

    # 3) Extraer stats avanzadas
    stats = {
        'gold_per_min':   [],
        'xp_per_min':     [],
        'last_hits':      [],
        'denies':         [],
        'hero_damage':    [],
        'tower_damage':   [],
        'hero_healing':   [],
        'level':          [],
        'net_worth':      [],
        'obs_placed':     [],
        'sen_placed':     [],
    }

    for match_id, slot in zip(df['match_id'], df['player_slot']):
        detalle = obtener_detalles_match(match_id)
        pj = None
        if detalle and 'players' in detalle:
            pj = next((p for p in detalle['players'] if p.get('player_slot') == slot), None)
        for stat in stats:
            stats[stat].append(pj.get(stat, 0) if pj else 0)

    for stat, values in stats.items():
        df[stat] = values

    # 4) Métricas derivadas
    df['kda_ratio']      = (df['kills'] + df['assists']) / df['deaths'].replace(0, 1)
    df['cs_per_min']     = df['last_hits'] / (df['duration'] / 60)
    df['denies_per_min'] = df['denies']    / (df['duration'] / 60)

    # 5) Convertir booleanos y fechas
    df['radiant_win'] = df['radiant_win'].astype(int)
    df['win']         = df['win'].astype(int)
    df['start_time']  = pd.to_datetime(df['start_time'], unit='s')

    # 6) Reordenar columnas
    cols = [
        'match_id','player_slot','radiant_win','win',
        'duration','game_mode','lobby_type','hero_id','start_time',
        'kills','deaths','assists',
        'gold_per_min','xp_per_min',
        'last_hits','denies','hero_damage','tower_damage','hero_healing',
        'level','net_worth','obs_placed','sen_placed',
        'kda_ratio','cs_per_min','denies_per_min',
        'average_rank','leaver_status','party_size','hero_variant'
    ]
    return df.loc[:, cols]

if __name__ == "__main__":
    os.makedirs(BASE_DIR, exist_ok=True)

    for account_id, alias in target_accounts.items():
        df = analizar_partidas(account_id, limit=100)
        if df is not None:
            path = os.path.join(BASE_DIR, f"{alias}.csv")
            df.to_csv(path, index=False)
            print(f"→ Guardado CSV de {alias}: {path}")
