import streamlit as st
import random
import matplotlib.pyplot as plt

# Configuración inicial
st.set_page_config(page_title="Bot Mines Realista", layout="centered")

# Función para generar una cuadrícula con minas aleatorias
def generar_tablero(filas=5, columnas=5, minas=4):
    tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
    posiciones = [(i, j) for i in range(filas) for j in range(columnas)]
    minas_colocadas = random.sample(posiciones, minas)
    for i, j in minas_colocadas:
        tablero[i][j] = -1
    return tablero, minas_colocadas

# Función para simular clics aleatorios y mostrar la partida
def simular_partida():
    tablero, minas = generar_tablero()
    posiciones_disponibles = [(i, j) for i in range(5) for j in range(5)]
    random.shuffle(posiciones_disponibles)

    aciertos = 0
    fallos = 0
    clics = []

    for pos in posiciones_disponibles:
        i, j = pos
        if tablero[i][j] == -1:
            fallos += 1
            clics.append((i, j, "❌"))
            break
        else:
            aciertos += 1
            clics.append((i, j, "✔️"))
            if aciertos in [4, 5]:
                break

    return tablero, clics, aciertos, fallos

# Función para mostrar el tablero con matplotlib
def mostrar_tablero(clics):
    fig, ax = plt.subplots()
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)

    for i in range(5):
        for j in range(5):
            ax.text(j, 4 - i, "", va='center', ha='center', fontsize=20)

    for i, j, simbolo in clics:
        ax.text(j, 4 - i, simbolo, va='center', ha='center', fontsize=20)

    st.pyplot(fig)

# Interfaz de usuario
st.title("🎯 Simulador de Bot Mines Realista")
st.markdown("Haz clic en el botón para simular una partida. Se detiene al llegar a 4 o 5 aciertos, o si cae en una mina.")

if st.button("🔁 Simular partida"):
    tablero, clics, aciertos, fallos = simular_partida()
    st.subheader("🧠 Última partida simulada:")
    mostrar_tablero(clics)
    st.markdown(f"**Aciertos:** {aciertos}  \n**Fallos:** {fallos}  \n**Total de clics:** {aciertos + fallos}")
