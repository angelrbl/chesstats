import streamlit as st
import graphs

player = st.session_state["player"]

st.title("First move.")
st.write("###### This page shows stats about the first moves played.")
st.space("small")

option_map = {0: "Player", 1: "General"}
selection = st.segmented_control("", options=option_map.keys(), format_func=lambda option: option_map[option], selection_mode="single", required=True, default=0)

st.write(f"Showing the first move stats of **{player.get_username()}**" if option_map[selection] is "Player" else f"Showing general first move stats")

tab1, tab2 = st.tabs(["Graph", "Heatmap"])

with tab1:
    try:
        st.pyplot(graphs.first_move_graph(player, selection=option_map[selection]), transparent="True")
    except:
        st.warning("Not enough data to show first moves graph.")
with tab2:
    st.pyplot(graphs.first_moves_heatmap(player, selection=option_map[selection]))


st.bottom.link_button("Proyecto", url="https://github.com/angelrbl/chesstats", type="secondary", icon="🐈")
