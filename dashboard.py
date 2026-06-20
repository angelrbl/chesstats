import streamlit as st
import general as general
from Player import Player
import graphs
from io import StringIO

#INICIALIZAMOS

if "username" not in st.session_state:
        st.session_state["username"] = "TensiKReyDama"
if "pgn_file" not in st.session_state:
        st.session_state["pgn_file"] = general.pgn_file
if "player" not in st.session_state:
    st.session_state["player"] = Player(st.session_state["username"], st.session_state["pgn_file"])

def data_from_pgn(username):
    st.session_state["username"] = username
    st.session_state["pgn_file"] = general.pgn_file
    st.session_state["player"] = Player(username, general.pgn_file)

def data_from_chesscom(username, months):
    with st.spinner(f"Downloading {username} last {months} games from Chess.com... (this may take a few seconds)"):
        try:
            st.session_state["username"] = username
            st.session_state["pgn_file"] = StringIO(general.seek_chessdotcom_games(st.session_state["username"], months=months))
            st.session_state["player"] = Player(username, st.session_state["pgn_file"])
        except Exception as e:
            st.error(f"Player's data not found on Chess.com: {e}")

#Título
st.write("# **Chesstats.**")
st.write("##### The best data analysis engine to improve at chess")
st.space("small")

st.write("Pick where do you want to get your data from: ")  
tab1, tab2 = st.tabs(["PGN File", "Chess.com"])
with tab1:
    #Usuario
    username = st.text_input(label="User", value=st.session_state["username"], placeholder="Type a username")
    st.button("Retrieve data from PGN file", on_click=data_from_pgn, kwargs={"username": username}, width="stretch", key="pgn_button")
    
with tab2:
    col1,col2 = st.columns(2) 
    username = col1.text_input(label="User", value=st.session_state["username"], placeholder="Type a Chess.com username")
    months = col2.number_input("Months", placeholder="Type the number of months back to retrieve data from", icon=":material/calendar_month:", min_value=1, value=3)
    st.button("Retrieve data from Chess.com", on_click=data_from_chesscom, kwargs={"username": username, "months": months}, width="stretch", key="chesscom_button")

player = st.session_state["player"]

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

st.bottom.link_button("Project", url="https://github.com/angelrbl/chesstats", type="secondary", icon=":material/deployed_code:")
graphs.check_text_color()