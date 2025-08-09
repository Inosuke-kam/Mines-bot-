
import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

# Configuración inicial
rows, cols = 5, 5
total_cells = rows * cols
csv_file = "stats.csv"

def simular_partida(num_minas=3, max_aciertos=4):
    minas = set(random.sample(range(total_cells), num_minas))
    clics_realizados = set()
    aciertos = 0
    fallos = 0

    while aciertos < max_aciertos:
        opciones_disponibles = list(set(range(total_cells)) - clics_realizados)
        if not opciones_disponibles:
            break

        # Estrategia predictiva simple: evitar repetir, evita bordes consecutivos si es posible
        centro = [6, 7, 8, 11, 12, 13, 16, 17, 18]
        opciones_seguras = [c for c in opciones_disponibles if c in centro]
        if opciones_seguras:
            casilla = random.choice(opciones_seguras)
        else:
            casilla = random.choice(opciones_disponibles)

        clics_realizados.add(casilla)

        if casilla in minas:
            fallos += 1
            break
        else:
            aciertos += 1

    resultado = "Gana" if aciertos >= 4 and fallos == 0 else "Pierde"
    guardar_resultado(aciertos, fallos, clics_realizados, resultado)
    return minas, clics_realizados, aciertos, fallos

def guardar_resultado(aciertos, fallos, clics, resultado):
    partida = {
        "fecha": datetime.now().isoformat(),
        "aciertos": aciertos,
        "fallos": fallos,
        "clicks": len(clics),
        "coordenadas": list(clics),
        "resultado": resultado
    }

    df = pd.DataFrame([partida])

    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, index=False)

def dibujar_cuadricula(minas, clics, aciertos, fallos):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xticks(range(cols + 1))
    ax.set_yticks(range(rows + 1))
    ax.grid(True)
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.invert_yaxis()

    for idx in range(total_cells):
        row = idx // cols
        col = idx % cols
        if idx in clics:
            if idx in minas:
                ax.text(col + 0.5, row + 0.5, '✖️', ha='center', va='center', fontsize=20)
            else:
                ax.text(col + 0.5, row + 0.5, '✔️', ha='center', va='center', fontsize=20)

    plt.title(f"Aciertos: {aciertos} | Fallos: {fallos} | Total clics: {len(clics)}")
    st.pyplot(fig)

# Interfaz de usuario
st.title("🤖 Bot Mines Realista con Estrategia Predictiva")
st.markdown("Cuadrícula 5x5 - Se detiene al lograr 4 o 5 aciertos o al fallar.")

if st.button("🎮 Simular Partida"):
    minas, clics, aciertos, fallos = simular_partida()
    dibujar_cuadricula(minas, clics, aciertos, fallos)
