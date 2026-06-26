import streamlit as st
from Player import Player
import general as general
import graphs

graphs.text_color = graphs.check_text_color()

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
    st.error("Error: No player selected.")
    player_to_compare = None

if player_to_compare:
    with st.spinner("Comparing games, this may take a few seconds:"):
        opponent = Player(player_to_compare, pgn_file)
        player_username = player.get_username()
        opponent_username = opponent.get_username()
        matches = player.get_matches(opponent)

    option_map = {0: "Matches", 1: "General"}
    selection = st.segmented_control("", options=option_map.keys(), format_func=lambda option: option_map[option], selection_mode="single", required=True, default=0)
    st.write(f"Comparing {"games" if option_map[selection] == "General" else "matches"} between **{player.get_username()}** and **{opponent_username}**:")
    st.space("xsmall")
    st.write("#### Performace comparison:")
    st.write(f"##### {option_map[selection]} win-rate: ")
    col1, col2 = st.columns(2)
    winning_rates = [{"Matches": player.get_winning_rate(games=matches), "General": player.get_winning_rate()}, {"Matches": opponent.get_winning_rate(games=matches), "General": opponent.get_winning_rate()}]
    col1.metric(label=player_username, value=winning_rates[0][option_map[selection]])
    col2.metric(label=opponent_username, value=winning_rates[1][option_map[selection]])
    tab1, tab2, tab3 = st.tabs(["General", "White", "Black"])

    with tab1:
        st.pyplot(graphs.compare_results_graphs(player, color="", opponent=opponent, selection=option_map[selection]), transparent="True")
    with tab2:
        st.pyplot(graphs.compare_results_graphs(player, color="white", opponent=opponent, selection=option_map[selection]), transparent="True")
    with tab3:
        st.pyplot(graphs.compare_results_graphs(player, color="black", opponent=opponent, selection=option_map[selection]), transparent="True")

    with st.expander("See explanation"):
            st.write(f'''
                The chart above shows results of the {"direct matches between" if option_map[selection] == "Matches" else "general games played by"} 
                *{player_username}* and *{opponent_username}*. On the graph, the left bars correspond to *{player_username}*, while the 
                right one corresponds to *{opponent_username}*.
            ''')

st.bottom.link_button("Project", url="https://github.com/angelrbl/chesstats", type="secondary", icon=":material/deployed_code:")

#IDEA: DESCARGAR EL MISMO NUMERO DE MESES DE JUEGO DEL OTRO JUGADOR PARA COMPARAR LAS GENERAL STATS DE UNA FORMA MAS JUSTA:
# estudiar si el pgn proviene de chess.com con una variable de estado,
# si es así, generar un pgn mediante seekchesscomgames del mismo numero de meses