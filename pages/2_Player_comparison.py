import streamlit as st
from Player import Player
import general as general
import graphs

if "player" not in st.session_state:
    st.session_state["player"] = Player("TensiKReyDama", general.pgn_file)
player = st.session_state["player"]
if "pgn_file" not in st.session_state:
        st.session_state["pgn_file"] = general.pgn_file
pgn_file = st.session_state["pgn_file"]

st.write("# Player comparison")
st.write("###### Compare different stats between players.")
st.space("small")

try:
    player_to_compare = st.selectbox(label="Player", placeholder="Select a player to compare with", options=player.get_rivals(), index=None)
except:
    raise Exception("Error: No player selected.")

if player_to_compare:
    option_map = {0: "Matches", 1: "General"}
    selection = st.segmented_control("", options=option_map.keys(), format_func=lambda option: option_map[option], selection_mode="single", required=True, default=0)
    opponent = Player(player_to_compare, pgn_file)
    st.write(f"Comparing {"games" if option_map[selection] == "General" else "matches"} between **{player.get_username()}** and **{opponent.get_username()}**")
    tab1, tab2, tab3 = st.tabs(["General", "White", "Black"])

    with tab1:
        st.pyplot(graphs.compare_results_graphs(player, color="", opponent=opponent, selection=option_map[selection]), transparent="True")
    with tab2:
        st.pyplot(graphs.compare_results_graphs(player, color="white", opponent=opponent, selection=option_map[selection]), transparent="True")
    with tab3:
        st.pyplot(graphs.compare_results_graphs(player, color="black", opponent=opponent, selection=option_map[selection]), transparent="True")

st.bottom.link_button("Project", url="https://github.com/angelrbl/chesstats", type="secondary", icon=":material/deployed_code:")
graphs.text_color = graphs.check_text_color()