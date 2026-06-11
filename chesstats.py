import chess
import chess.pgn

pgn = open("chess_games.pgn", encoding="utf-8")

chess_games = []
chess_game = chess.pgn.read_game(pgn) 
while chess_game is not None:
    chess_games.append(chess_game)
    chess_game = chess.pgn.read_game(pgn) 

wins = 0
user = "TensiKReyDama"

for cg in chess_games:
    hd = cg.headers
    print(f"{hd.get("White")} vs. {hd.get("Black")}:  {hd.get("Result")}")
    if (user in hd.get("White", "?") and hd.get("Result") == "1-0") or (user in hd.get("Black", "?") and hd.get("Result") == "0-1"):
        print(user + " won.")
        wins += 1
    else:
        print(user + " did not win.")

    print()

print(f"{user} won {wins} games out of {len(chess_games)}, making a win % of: {(wins / len(chess_games)) * 100} %")