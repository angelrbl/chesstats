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
        first_move = cg.get_first_move(1)
        if first_move in first_moves.keys():
            first_moves.update({first_move: first_moves.get(first_move) + 1})
        else:
            first_moves.update({first_move: 1})
    return first_moves

def get_first_moves_user(usr):
    first_moves = {}
    for cg in chess_games:
        first_move = cg.get_first_move_user(usr, 1)
        usr_color = cg.get_color(usr)
        if (first_move, usr_color) in first_moves.keys():
            first_moves.update({(first_move, usr_color): first_moves.get((first_move, usr_color)) + 1})
        else:
            first_moves.update({(first_move, usr_color): 1})
    return first_moves

def get_first_moves_matrix():
    first_moves = [[0]*8 for _ in range(8)]
    for cg in chess_games:
        first_move = cg.get_first_move(0)
        go_square = first_move.to_square
        f = chess.square_rank(go_square)
        c = chess.square_file(go_square)
        first_moves[f][c] += 1
    return first_moves

def get_first_moves_user_matrix(usr):
    first_moves = [[0]*8 for _ in range(8)]
    for cg in chess_games:
        first_move = cg.get_first_move_user(usr, 0)
        go_square = first_move.to_square
        f = chess.square_rank(go_square)
        c = chess.square_file(go_square)
        first_moves[f][c] += 1
    return first_moves

move_matrix = get_first_moves_user_matrix(user)

for f in range(len(move_matrix)):
    print(move_matrix[-(f+1)])

#print(get_first_moves_user(user))