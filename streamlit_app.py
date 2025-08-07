
import streamlit as st
import random
import matplotlib.pyplot as plt

# Configuración de la cuadrícula
rows, cols = 5, 5
total_cells = rows * cols

def simular_partida(num_minas=3, max_aciertos=4):
    minas = set(random.sample(range(total_cells), num_minas))
    clics_realizados = set()
    aciertos = 0
    fallos = 0

    while aciertos < max_aciertos:
        opciones_disponibles = list(set(range(total_cells)) - clics_realizados)
        if not opciones_disponibles:
            break
        casilla = random.choice(opciones_disponibles)
        clics_realizados.add(casilla)

        if casilla in minas:
            fallos += 1
            break
        else:
            aciertos += 1

    return minas, clics_realizados, aciertos, fallos

def dibujar_cuadricula_5x5(minas, clics, aciertos, fallos):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xticks([x for x in range(6)])
    ax.set_yticks([y for y in range(6)])
    ax.grid(True)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.invert_yaxis()

    for idx in range(25):
        row = idx // 5
        col = idx % 5
        if idx in clics:
            if idx in minas:
                ax.text(col + 0.5, row + 0.5, '✖️', ha='center', va='center', fontsize=20)
            else:
                ax.text(col + 0.5, row + 0.5, '✔️', ha='center', va='center', fontsize=20)

    plt.title(f"Aciertos: {aciertos} | Fallos: {fallos} | Total clics: {len(clics)}")
    st.pyplot(fig)

st.title("🔮 Simulador de Mines - Estilo Predictivo")
st.markdown("Cuadrícula 5x5 con 3 minas aleatorias. Se detiene al lograr 4 o 5 aciertos o al fallar.")

if st.button("🎮 Simular Partida"):
    minas, clics, aciertos, fallos = simular_partida()
    dibujar_cuadricula_5x5(minas, clics, aciertos, fallos)
