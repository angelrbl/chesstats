import streamlit as st
import general as general
from Player import Player
import graphs

#Título
st.write("# **Chesstats.**")
st.write("###### The best data analysis engine to improve at chess")
st.space("small")

#Usuario
if "username" not in st.session_state:
    st.session_state["username"] = "TensiKReyDama"
st.session_state["username"] = st.text_input(label="User", value=st.session_state["username"], placeholder="Type a username")

player = Player(st.session_state["username"], general.pgn_file)
if "player" not in st.session_state:
    st.session_state["player"] = player
else:
    st.session_state["player"] = player

st.space("medium")

#ESTADISTÍCAS PARTIDAS
st.write(f"## ***{st.session_state["username"] if st.session_state["username"] else "User"}***, welcome.  \n##### These are some of your chess stats:")
col1, col2, col3 = st.columns(3)
col1.metric(label="Games", value=player.GAME_NUM)
col2.metric(label="Wins", value=player.get_win_count(color=""))
col3.metric(label="Winning %", value=player.get_winning_rate())

st.space("xsmall")
st.write(f"#### Performance")
st.space("xxsmall")
tab1, tab2, tab3 = st.tabs(["General", "White", "Black"])

with tab1:
    st.pyplot(graphs.results_graph(player, color=""), transparent="True")
with tab2:
    st.pyplot(graphs.results_graph(player, color="white"), transparent="True")
with tab3:
    st.pyplot(graphs.results_graph(player, color="black"), transparent="True")

st.bottom.link_button("Project", url="https://github.com/angelrbl/chesstats", type="secondary", icon="🐈", )
