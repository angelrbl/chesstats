import chess
import chess.pgn
from ChessGame import ChessGame
from Player import Player

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
            first_moves[first_move] = first_moves.get(first_move, 0) + 1
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


pgn_file = open("chess_games.pgn", encoding="utf-8")
user = "TensiKReyDama"
games = build_games_list(pgn_file)

if __name__ == "__main__":
    player = Player(user, pgn_file)
    chess_games = build_games_list(pgn_file)

    #PLAYER

    player_move_matrix = player.get_first_moves_matrix()

    for f in range(len(player_move_matrix)):
        print(player_move_matrix[-(f+1)]) 
        
    player_first_moves = player.get_first_moves()
    print(player_first_moves)

    #GAMES

    games_move_matrix = get_first_moves_matrix(chess_games)

    for f in range(len(games_move_matrix)):
        print(games_move_matrix[-(f+1)])

    games_first_moves = get_first_moves(chess_games)
    print(games_first_moves)
 
    player = Player(user, pgn_file)
    print(player.get_first_capture(0))

    chess_games = build_games_list(pgn_file)
    print(chess_games[0].get_first_capture())

    print(player.took(player.get_games()[0], 17))