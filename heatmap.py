import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from Player import Player

def build_heatmap(player):
    matriz_np = np.array(player.get_first_moves_matrix())
    matriz_np = np.flipud(matriz_np)

    cols = ["a", "b", "c", "d", "e", "f", "g", "h"]
    files = ["8", "7", "6", "5", "4", "3", "2", "1"]

    fig, ax = plt.subplots(figsize=(7, 7))
    sns.heatmap(matriz_np, annot=True, fmt="d", cmap="YlOrRd", square=True, cbar=False, xticklabels=cols, yticklabels=files, ax=ax)
    fig.patch.set_alpha(0.0)
    ax.tick_params(colors='white')

    return fig

if __name__ == "__main__":
    pgn_file = open("chess_games.pgn", encoding="utf-8")
    user = "TensiKReyDama"

    usr = Player(user, pgn_file)
    build_heatmap(usr)
    plt.show()