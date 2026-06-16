import streamlit as st
import heatmap

player = st.session_state["player"]

st.title("First move heatmap")
st.write("This heatmap shows the first moves played by a specific player.")

st.pyplot(heatmap.build_heatmap(player))

