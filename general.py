import chess
import chess.pgn
from ChessGame import ChessGame
import chessdotcom
import streamlit as st

chessdotcom.Client.request_config["headers"]["User-Agent"] = ("ChesstatsApp"
    "Contact me at angelramibla@gmail.com")

def seek_chessdotcom_games(username, months):
    try:
        response = chessdotcom.get_player_game_archives(username.lower())
        archive = response.json.get("archives", [])
        pgn = ""
        last_month_url = archive[-1]
        last_month_url = last_month_url.split('/')

        for i in range(months):
            year = last_month_url[-2]
            month = str(int(last_month_url[-1]) - i)
            if int(month) <= 0:
                month = str(int(month) + 12)
                year = str(int(year) - 1)
            month_pgn = chessdotcom.get_player_games_by_month_pgn(username.lower(), year=year, month=month)
            if month_pgn.text:
                pgn += month_pgn.text + "\n\n"
        return pgn
    except Exception as e:
        raise Exception(f"Error while obtaining data from Chess.com: {e}")


def build_games_list(pgn):
    pgn.seek(0)
    games = []
    file_game = chess.pgn.read_game(pgn) 
    while file_game is not None:
        games.append(ChessGame(file_game))
        file_game = chess.pgn.read_game(pgn) 
    pgn.seek(0)
    return games

def get_first_moves(games):
    first_moves = {}
    for game in games:
        first_move = game.get_first_move(notation=1)
        if first_move in first_moves.keys():
            first_moves[first_move] += 1
        else:
            first_moves[first_move] = 1
    return first_moves

def get_first_moves_matrix(games):
    first_moves = [[0]*8 for _ in range(8)]
    for game in games:
        first_move = game.get_first_move(notation=0)
        go_square = first_move.to_square
        f = chess.square_rank(go_square)
        c = chess.square_file(go_square)
        first_moves[f][c] += 1
    return first_moves

def get_opening_stats(games):
    opening_stats = {}
    for game in games:
        first_move = game.get_first_move(notation=1)
        result = game.get_white_result()
        if first_move not in opening_stats:
            opening_stats[first_move] = {"win": 0, "draw": 0, "loss": 0}
        opening_stats[first_move][result] += 1
    return opening_stats

pgn_file = open("chess_games.pgn", encoding="utf-8")
user = "TensiKReyDama"
games = build_games_list(pgn_file)

if __name__ == "__main__":
    print(seek_chessdotcom_games("TensiKReyDama", months=3))