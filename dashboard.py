import streamlit as st
import chesstats as cs
from Player import Player

#Título
st.write("# Chesstats")
st.write("The best data analysis engine to improve at chess")

#Usuario
if "username" not in st.session_state:
    st.session_state["username"] = "TensiKReyDama"
st.session_state["username"] = st.text_input(label="User", value=st.session_state["username"], placeholder="Type a username")

player = Player(st.session_state["username"], cs.pgn_file)
if "player" not in st.session_state:
    st.session_state["player"] = player
else:
    st.session_state["player"] = player

st.bottom.link_button("Proyecto", url="https://github.com/angelrbl/chesstats", type="secondary", icon="🐈")
