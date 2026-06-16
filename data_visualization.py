import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import chesstats as cs
import chess
import chess.pgn
from ChessGame import ChessGame
from Player import Player

pgn_file = open("chess_games.pgn", encoding="utf-8")
user = "TensiKReyDama"

chess_games = cs.build_games_list(pgn_file)
player = Player(user, pgn_file)

matriz_np = np.array(player.get_first_moves_matrix())
matriz_np = np.flipud(matriz_np)

cols = ["a", "b", "c", "d", "e", "f", "g", "h"]
files = ["1", "2", "3", "4", "5", "6", "7", "8"]

plt.figure(figsize=(7, 7))
sns.heatmap(matriz_np, annot=True, fmt="d", cmap="YlOrRd", square=True, cbar=False, xticklabels=cols, yticklabels=files)

plt.show()