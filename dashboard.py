import streamlit as st
import chesstats as cs
from Player import Player
import matplotlib.pyplot as plt
import seaborn as sns

#Título
st.write("# **Chesstats.**")
st.write("###### The best data analysis engine to improve at chess")
st.space("small")

#Usuario
if "username" not in st.session_state:
    st.session_state["username"] = "TensiKReyDama"
st.session_state["username"] = st.text_input(label="User", value=st.session_state["username"], placeholder="Type a username")

player = Player(st.session_state["username"], cs.pgn_file)
if "player" not in st.session_state:
    st.session_state["player"] = player
else:
    st.session_state["player"] = player

st.space("medium")

#ESTADISTÍCAS PARTIDAS
st.write(f"## ***{st.session_state["username"] if st.session_state["username"] else "User"}***, welcome.  \n##### These are some of your chess stats:")
col1, col2, col3 = st.columns(3)
col1.metric(label="Games", value=player.GAME_NUM)
col2.metric(label="Wins", value=player.get_win_count())
col3.metric(label="Winning %", value=player.get_winning_rate())

st.write(f"##### Performance")
wins = player.get_win_count()
draws = player.get_draw_count()
losses = player.GAME_NUM - wins - draws
chess_results_data = {
    "Results": ["Wins", "Losses", "Draws"],
    "Games": [wins, losses, draws]
}

fig, ax = plt.subplots()
color_palette = ['#2ecc71', '#e74c3c', '#95a5a6']
sns.set_theme(style="dark", rc={"axes.facecolor": "none", "figure.facecolor": "none"})
sns.barplot(x='Games',y='Results', data=chess_results_data, palette=color_palette, ax=ax)
sns.despine(left=True, bottom=True)
ax.tick_params(colors='white', labelsize=12) # Letras en blanco
ax.set_xlabel('Número de Partidas', color='white', fontsize=12)
ax.set_ylabel('', color='white')
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)
st.pyplot(fig, transparent="True")

st.bottom.link_button("Proyecto", url="https://github.com/angelrbl/chesstats", type="secondary", icon="🐈", )
