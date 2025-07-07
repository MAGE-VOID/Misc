#!/usr/bin/env python3
import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Ruta absoluta por defecto al CSV
DEFAULT_CSV = r"D:\FOREX\MT5_1\MQL5\Experts\Projects\Sharing-Projects\Misc\Dota2\Fer.csv"

def analyze_player(csv_path):
    # 1) Leer y preparar datos
    df = pd.read_csv(csv_path, parse_dates=['start_time'])
    df.sort_values('start_time', inplace=True)
    alias = os.path.splitext(os.path.basename(csv_path))[0]

    # 2) Estadísticas generales
    total_games = len(df)
    win_rate    = df['win'].mean()
    avg_gpm     = df['gold_per_min'].mean()
    avg_xpm     = df['xp_per_min'].mean()
    avg_kda     = df['kda_ratio'].mean()

    print(f"\n=== Resumen para {alias} ===")
    print(f"Partidas analizadas : {total_games}")
    print(f"Tasa de victorias    : {win_rate:.2%}")
    print(f"GPM promedio         : {avg_gpm:.1f}")
    print(f"XPM promedio         : {avg_xpm:.1f}")
    print(f"KDA promedio         : {avg_kda:.2f}")

    # 3) Definir métricas temporales
    time_metrics = [
        'gold_per_min',
        'xp_per_min',
        'kda_ratio',
        'cs_per_min',
        'denies_per_min',
        'net_worth'
    ]

    # 4) Crear figura con GridSpec: 3 filas para métricas, 1 fila para KDA por partida
    fig = plt.figure(figsize=(14, 20))
    gs = gridspec.GridSpec(4, 2, height_ratios=[1,1,1,1.5], hspace=0.4, wspace=0.3)

    # 5) Graficar evolución de cada métrica
    for idx, metric in enumerate(time_metrics):
        row, col = divmod(idx, 2)
        ax = fig.add_subplot(gs[row, col])
        ax.plot(df['start_time'], df[metric], marker='o', linestyle='-')
        ax.set_title(f"{alias} — Evolución de {metric.replace('_',' ').title()}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel(metric.replace('_',' ').title())
        ax.grid(True)

    # 6) Gráfico de K/D/A por partida, ocupando toda la fila inferior
    ax_kda = fig.add_subplot(gs[3, :])
    x = np.arange(total_games)
    width = 0.25
    ax_kda.bar(x - width, df['kills'],   width, label='Kills')
    ax_kda.bar(x,         df['deaths'],  width, label='Deaths')
    ax_kda.bar(x + width, df['assists'], width, label='Assists')
    ax_kda.set_title(f"{alias} — K/D/A por partida")
    ax_kda.set_xlabel("Partida (orden cronológico)")
    ax_kda.set_ylabel("Cantidad")
    ax_kda.set_xticks(x)
    ax_kda.set_xticklabels(df['match_id'].astype(str), rotation=90, fontsize=6)
    ax_kda.legend()
    ax_kda.grid(True)

    # 7) Ajustar layout y mostrar todo en una sola ventana
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(
        description="Análisis interactivo de CSV de Dota2 por jugador"
    )
    parser.add_argument(
        "-i", "--input",
        default=DEFAULT_CSV,
        help=f"Ruta al CSV del jugador (por defecto: {DEFAULT_CSV})"
    )
    args = parser.parse_args()
    analyze_player(args.input)

if __name__ == "__main__":
    main()
