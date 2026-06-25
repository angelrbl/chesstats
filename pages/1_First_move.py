import streamlit as st
import graphs
import general as general
from Player import Player

if "player" not in st.session_state:
    st.session_state["player"] = Player("TensiKReyDama", general.pgn_file)
player = st.session_state["player"]
st.title("First move.")
st.write("###### This page shows stats about the first moves played.")
st.space("small")

option_map = {0: "Player", 1: "General"}
selection = st.segmented_control("", options=option_map.keys(), format_func=lambda option: option_map[option], selection_mode="single", required=True, default=0)

try:
    st.write(f"Showing the first move stats of **{player.get_username() if player.get_username() else "User"}**" if option_map[selection] == "Player" else f"Showing general first move stats")
    player_selected = True
except:
    st.error("Error: No player selected.")
    player_selected = False

if player_selected:
    tab1, tab2 = st.tabs(["Graph", "Heatmap"])

    with tab1:
        st.write("#### First moves")

        try:
            st.pyplot(graphs.first_move_graph(player, selection=option_map[selection]), transparent="True")
        except:
            st.warning("Not enough data to show first moves graph.")
        
        st.markdown("---")
        st.write("#### Win rate")
        
        try:
            st.pyplot(graphs.opening_stats_graph(player, selection=option_map[selection]), transparent="True")
        except:
            st.warning("Not enough data to show first move leading win rates.")

        with st.expander("See explanation"):
            st.write('''
                The chart above shows the loss-rate, draw-rate and win-rate of
                the specified games as white/black in order from left to right.
            ''')

    with tab2:
        st.pyplot(graphs.first_moves_heatmap(player, selection=option_map[selection]))

st.bottom.link_button("Project", url="https://github.com/angelrbl/chesstats", type="secondary", icon=":material/deployed_code:")
graphs.text_color = graphs.check_text_color()
