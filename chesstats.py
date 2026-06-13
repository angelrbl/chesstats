import chess
import chess.pgn
from ChessGame import ChessGame

pgn = open("chess_games.pgn", encoding="utf-8")
user = "TensiKReyDama"

chess_games = []
cg = chess.pgn.read_game(pgn) 
while cg is not None:
    chess_games.append(ChessGame(cg))
    cg = chess.pgn.read_game(pgn) 

def get_winning_rate(usr):
    wins = 0
    for cg in chess_games:
        print(f"{cg.white} vs. {cg.black}:  {cg.result}")
        if (cg.get_winner() == usr):
            print(usr + " won.")
            wins += 1
        else:
            print(usr + " did not win.")

        print()

    print(f"{usr} won {wins} games out of {len(chess_games)}, making a win % of: {(wins / len(chess_games)) * 100} %")

def get_first_moves():
    first_moves = {}
    for cg in chess_games:
        first_move = cg.get_first_move()
        if first_move in first_moves.keys():
            first_moves.update({first_move: first_moves.get(first_move) + 1})
        else:
            first_moves.update({first_move: 1})
    return first_moves

def get_first_moves_user(usr):
    first_moves = {}
    for cg in chess_games:
        first_move = cg.get_first_move_user(usr)
        usr_color = cg.get_color(usr)
        if first_move in first_moves.keys():
            first_moves.update({(first_move, usr_color): first_moves.get(first_move)})
        else:
            first_moves.update({(first_move, usr_color): 1})
    return first_moves

print(get_first_moves_user(user))