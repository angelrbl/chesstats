import streamlit as st
import general as general
from Player import Player
import graphs
from io import StringIO

st.set_page_config(page_title="Chesstats", page_icon=":material/chess_rook:")
graphs.text_color = graphs.check_text_color()

#INICIALIZAMOS

if "username" not in st.session_state:
        st.session_state["username"] = None
if "pgn_file" not in st.session_state:
        st.session_state["pgn_file"] = general.pgn_file
if "player" not in st.session_state:
    st.session_state["player"] = None
if "games" not in st.session_state:
    st.session_state["games"] = general.build_games_list(st.session_state["pgn_file"])

def data_from_pgn(username, pgn_file):
    st.session_state["username"] = username
    st.session_state["pgn_file"] = pgn_file
    st.session_state["player"] = Player(username, pgn_file)
    st.session_state["games"] = general.build_games_list(pgn_file)

def data_from_chesscom(username, months):
    with st.spinner(f"Downloading {username} last {months} months' games from Chess.com... (this may take a few seconds)"):
        try:
            st.session_state["username"] = username
            print(username, months)
            st.session_state["pgn_file"] = StringIO(general.seek_chessdotcom_games(username=username, months=months))
            st.session_state["player"] = Player(username, st.session_state["pgn_file"])
            st.session_state["games"] = general.build_games_list(st.session_state["pgn_file"])
        except Exception as e:
            st.error(f"Player's data not found on Chess.com: {e}")

def default_pgn_file():
    st.session_state["pgn_file"] = general.pgn_file

#Título
st.write("# **Chesstats.**")
st.write("##### The best data analysis engine to improve at chess")
st.space("small")

st.write("Pick where do you want to get your data from: ")  
tab1, tab2 = st.tabs(["PGN File", "Chess.com"])
with tab1:
    #Usuario
    pgn_file = general.pgn_file  
    uploaded_file = st.file_uploader(label="PGN file", type=".pgn", max_upload_size=10, accept_multiple_files=False, on_change=default_pgn_file)
    with st.spinner(f"Downloading games from uploaded PGN file... (this may take a few seconds)"):
        if uploaded_file:
            pgn_file = StringIO(uploaded_file.getvalue().decode("utf-8"))            
    player_list = general.get_player_list(pgn_file)
    pgn_user = st.selectbox(label="User", placeholder="Type a username", options=player_list, index=(None if not st.session_state["username"] in player_list else player_list.index(st.session_state["username"])))
    st.button("Retrieve data from PGN file", on_click=data_from_pgn, kwargs={"username": pgn_user, "pgn_file": pgn_file}, width="stretch", key="pgn_button")

with tab2:
    col1,col2 = st.columns(2) 
    chesscom_user = col1.text_input(label="User", value=st.session_state["username"], placeholder="Type a Chess.com username")
    months = col2.number_input("Months", placeholder="Type the number of months back to retrieve data from", icon=":material/calendar_month:", min_value=1, value=3)
    st.button("Retrieve data from Chess.com", on_click=data_from_chesscom, kwargs={"username": chesscom_user, "months": months}, width="stretch", key="chesscom_button")

player = st.session_state["player"]

st.space("medium")
if player:
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

st.bottom.link_button("Project", url="https://github.com/angelrbl/chesstats", type="secondary", icon=":material/deployed_code:")
