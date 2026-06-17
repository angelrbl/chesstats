import streamlit as st
import heatmap

player = st.session_state["player"]

st.title("First move heatmap.")
st.write("###### This heatmap shows the first moves played by a specific player.")
st.space("small")

st.pyplot(heatmap.build_heatmap(player))

st.bottom.link_button("Proyecto", url="https://github.com/angelrbl/chesstats", type="secondary", icon="🐈")
