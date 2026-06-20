import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from Player import Player
import general as general
from matplotlib.ticker import MaxNLocator
import streamlit as st

text_color = "white" if st.context.theme.type == "dark" else "black"
if "pgn_file" not in st.session_state:
        st.session_state["pgn_file"] = general.pgn_file
pgn_file = st.session_state["pgn_file"]
if "games" not in st.session_state:
        st.session_state["games"] = general.build_games_list(pgn_file)

def check_text_color():
    text_color = "white" if st.context.theme.type == "dark" else "black"

def first_moves_heatmap(player, selection):
    matriz_np = np.array(player.get_first_moves_matrix() if selection == "Player" else general.get_first_moves_matrix(st.session_state["games"]))
    matriz_np = np.flipud(matriz_np)

    cols = ["a", "b", "c", "d", "e", "f", "g", "h"]
    files = ["8", "7", "6", "5", "4", "3", "2", "1"]

    fig, ax = plt.subplots(figsize=(7, 7))
    sns.heatmap(matriz_np, annot=True, fmt="d", cmap="YlOrRd", square=True, cbar=False, xticklabels=cols, yticklabels=files, ax=ax)
    fig.patch.set_alpha(0.0)
    ax.tick_params(colors=text_color)

    return fig

def results_graph(player, color):
    if color == "white":
        wins = player.get_win_count(color="white")
        draws = player.get_draw_count(color="white")
        losses = player.get_loss_count(color="white")
        color="#dfd3c3"
    elif color == "black":
        wins = player.get_win_count(color="black")
        draws = player.get_draw_count(color="black")
        losses = player.get_loss_count(color="black")
        color = "#373737"
    else:
        wins = player.get_win_count(color="")
        draws = player.get_draw_count(color="")
        losses = player.get_loss_count(color="")
        color = "#dfd3c3"
    
    
    chess_results_data = {
        "Results": ["Wins", "Losses", "Draws"],
        "Games": [wins, losses, draws]
    }

    fig, ax = plt.subplots(figsize=(8,6))
    sns.barplot(x='Results',y='Games', data=chess_results_data, color=color, ax=ax)
    sns.despine(left=True, bottom=True)
    ax.tick_params(colors=text_color, labelsize=12)
    ax.set_xlabel('', color=text_color)
    ax.set_ylabel('Num of games', color=text_color, fontsize=12)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    fig.patch.set_alpha(0.0)
    return fig

def first_move_graph(player, selection):
    if selection == "Player":
        first_move_dict = player.get_first_moves()
        if not first_move_dict:
            raise Exception("Not enough data to show")
        first_move_white_data = {
            "Move": list(first_move_dict[0].keys()),
            "Times": list(first_move_dict[0].values())
        }
        first_move_black_data = {
            "Move": list(first_move_dict[1].keys()),
            "Times": list(first_move_dict[1].values())
        }
        games_num = len(first_move_dict[0]) + len(first_move_dict[1])
    else:
        first_move_dict = general.get_first_moves(st.session_state["games"])
        if not first_move_dict:
            raise Exception("Not enough data to show")
        first_move_white_data = {
            "Move": list(first_move_dict.keys()),
            "Times": list(first_move_dict.values())
        }
        games_num = len(first_move_dict.keys())

    height = max(3, games_num * 0.5) 

    fig, ax = plt.subplots(figsize=(8, height))
    sns.barplot(x='Times', y='Move', data=first_move_white_data, color="#dfd3c3", ax=ax)
    if selection == "Player":
        sns.barplot(x='Times', y='Move', data=first_move_black_data, color="#373737", ax=ax)
        ax.bar_label(ax.containers[1], padding=8, color=text_color, fontweight='bold', fontsize=11)
    ax.tick_params(colors=text_color, labelsize=12)
    ax.bar_label(ax.containers[0], padding=8, color=text_color, fontweight='bold', fontsize=11)
    ax.set_ylabel('', color=text_color)
    ax.get_xaxis().set_visible(False)
    sns.despine(left=True, bottom=True)
    fig.patch.set_alpha(0.0)
    return fig


def opening_stats_graph(player, selection):
    if selection == "Player":
        opening_stats = player.get_opening_stats()
        if not opening_stats:
            raise Exception("Not enough data to show")
        #WHITE
        white_moves = []
        white_results = []
        white_percentages = []
        for move, data in opening_stats[0].items():
            total = data["win"] + data["draw"] + data["loss"]
            if total > 0:
                #WIN
                if data["win"] > 0:
                    white_moves.append(move)
                    white_results.append("Win")
                    white_percentages.append((data["win"]/total) * 100)
                #DRAW
                if data["draw"] > 0:
                    white_moves.append(move)
                    white_results.append("Draw")
                    white_percentages.append((data["draw"]/total) * 100)
                #LOSS
                if data["loss"] > 0:
                    white_moves.append(move)
                    white_results.append("Loss")
                    white_percentages.append((data["loss"]/total) * 100)
        
        if not white_moves:
            raise Exception("No moves with total games > 0 found")

        white_data = {
            "Move": white_moves,
            "Result": white_results,
            "Percentage": white_percentages
        }

        #BLACK
        black_moves = []
        black_results = []
        black_percentages = []
        for move, data in opening_stats[1].items():
            total = data["win"] + data["draw"] + data["loss"]
            if total > 0:
                #WIN
                if data["win"] > 0:
                    black_moves.append(move)
                    black_results.append("Win")
                    black_percentages.append((data["win"]/total) * 100)
                #DRAW
                if data["draw"] > 0:
                    black_moves.append(move)
                    black_results.append("Draw")
                    black_percentages.append((data["draw"]/total) * 100)
                #LOSS
                if data["loss"] > 0:
                    black_moves.append(move)
                    black_results.append("Loss")
                    black_percentages.append((data["loss"]/total) * 100)
        
        if not black_moves:
            raise Exception("No moves with total games > 0 found")

        black_data = {
            "Move": black_moves,
            "Result": black_results,
            "Percentage": black_percentages
        }

        games_num = len(opening_stats[0]) + len(opening_stats[1])
    else:
        opening_stats = general.get_opening_stats(st.session_state["games"])
        if not opening_stats:
            raise Exception("Not enough data to show")
        #WHITE
        white_moves = []
        white_results = []
        white_percentages = []
        for move, data in opening_stats.items():
            total = data["win"] + data["draw"] + data["loss"]
            if total > 0:
                #WIN
                if data["win"] > 0:
                    white_moves.append(move)
                    white_results.append("Win")
                    white_percentages.append((data["win"]/total) * 100)
                #DRAW
                if data["draw"] > 0:
                    white_moves.append(move)
                    white_results.append("Draw")
                    white_percentages.append((data["draw"]/total) * 100)
                #LOSS
                if data["loss"] > 0:
                    white_moves.append(move)
                    white_results.append("Loss")
                    white_percentages.append((data["loss"]/total) * 100)
        
        if not white_moves:
            raise Exception("No moves with total games > 0 found")

        white_data = {
            "Move": white_moves,
            "Result": white_results,
            "Percentage": white_percentages
        }
        games_num = len(opening_stats)

    white_palette = {"Win": "#dfd3c3", "Draw": "#beb6aa", "Loss": "#888279"}
    black_palette = {"Win": "#333333", "Draw": "#242424", "Loss": "#1a1a1a"}
        
        
    fig, ax = plt.subplots(figsize=(8, max(3, games_num * 0.5)))
    sns.histplot(data=white_data, y="Move", weights="Percentage", hue="Result", multiple="stack", alpha=1, shrink=0.5, palette=white_palette, ax=ax)
    if selection == "Player":
        sns.histplot(data=black_data, y="Move", weights="Percentage", hue="Result", multiple="stack", alpha=1, shrink=0.5, palette=black_palette, ax=ax)
    ax.tick_params(colors=text_color, labelsize=12)
    ax.set_xlabel('Percentage (%)', color=text_color, fontsize=12)
    ax.set_ylabel('Move', color=text_color, fontsize=12)
    ax.set_xlim(0, 100)

    sns.despine(left=True, bottom=True)
    fig.patch.set_alpha(0.0)

    legend = ax.get_legend()
    if legend:
        legend.remove()
            
    return fig

if __name__ == "__main__":
    pgn_file = open("chess_games.pgn", encoding="utf-8")
    user = "TensiKReyDama"

    usr = Player(user, pgn_file)
    first_move_graph(usr, selection="General")
    plt.show()