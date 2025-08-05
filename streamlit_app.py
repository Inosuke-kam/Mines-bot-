
import streamlit as st
import random

st.set_page_config(page_title="Bot Mines Web", layout="centered")

st.title("💣 Bot Mines – Simulación Visual")

# Parámetros
minas = random.randint(3, 4)
cuadricula = 5
max_aciertos = 5

# Inicialización
if "mina_pos" not in st.session_state:
    st.session_state.tablero = [["" for _ in range(cuadricula)] for _ in range(cuadricula)]
    st.session_state.mina_pos = set()
    while len(st.session_state.mina_pos) < minas:
        st.session_state.mina_pos.add((random.randint(0, 4), random.randint(0, 4)))
    st.session_state.clics = []
    st.session_state.resultado = None

def procesar_clic(x, y):
    if (x, y) in st.session_state.clics or st.session_state.resultado:
        return
    st.session_state.clics.append((x, y))
    if (x, y) in st.session_state.mina_pos:
        st.session_state.tablero[x][y] = "❌"
        st.session_state.resultado = "💥 Fallaste. Fin de la partida."
    else:
        st.session_state.tablero[x][y] = "✔️"
        aciertos = sum(1 for c in st.session_state.clics if c not in st.session_state.mina_pos)
        if aciertos in [4, 5]:
            st.session_state.resultado = f"🎉 ¡Ganaste con {aciertos} aciertos!"
        else:
            st.session_state.resultado = f"Aciertos: {aciertos}"

# Mostrar cuadrícula
for i in range(cuadricula):
    cols = st.columns(cuadricula)
    for j in range(cuadricula):
        cell = st.session_state.tablero[i][j]
        if cell:
            cols[j].markdown(f"### {cell}")
        elif st.session_state.resultado:
            cols[j].button(" ", key=f"{i}-{j}", disabled=True)
        else:
            if cols[j].button(" ", key=f"{i}-{j}"):
                procesar_clic(i, j)
                st.experimental_rerun()

# Mostrar resultado
if st.session_state.resultado:
    aciertos = sum(1 for c in st.session_state.clics if c not in st.session_state.mina_pos)
    fallos = len(st.session_state.clics) - aciertos
    st.markdown(f"**{st.session_state.resultado}**")
    st.markdown(f"- Total de clics: {len(st.session_state.clics)}")
    st.markdown(f"- ✔️ Aciertos: {aciertos}")
    st.markdown(f"- ❌ Fallos: {fallos}")

# Reiniciar
if st.button("🔁 Reiniciar partida"):
    for key in ["tablero", "mina_pos", "clics", "resultado"]:
        st.session_state.pop(key, None)
    st.experimental_rerun()
