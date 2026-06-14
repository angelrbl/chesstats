import chess
import chess.pgn
from ChessGame import ChessGame

class Player:
    def __init__(self, usr, pgn):
        self.username = usr
        self.games = self.filter_games(pgn)
        self.board = chess.Board()
        self.GAME_NUM = len(self.games)

    def filter_games(self, pgn):
        chess_games = []
        file_game = chess.pgn.read_game(pgn) 
        while file_game is not None:
            game = ChessGame(file_game)
            if(game.get_white() == self.username or game.get_black() == self.username):
                chess_games.append(game)
            file_game = chess.pgn.read_game(pgn) 
        return chess_games
    
    def get_winning_rate(self):
        wins = 0
        for game in self.games:
            print(f"{game.get_white()} vs. {game.get_black()}:  {game.get_result()}")
            if (self.won(game)):
                print(self.username + " won.\n")
                wins += 1
            elif(self.drew(game)):
                print(self.username + " drew.\n")
            else:
                print(self.username + " lost.\n")

        return f"{self.username} won {wins} games out of {self.GAME_NUM}, making a win % of: {(wins / self.GAME_NUM) * 100} %"

    def won(self, game):
        if game.get_winner() == self.username:
            return True
        else:
            return False
    def drew(self, game):
        if game.get_winner() == "draw":
            return True
        else:
            return False
    def lost(self, game):
        if self.drew(game) or self.won(game):
            return True
        else:
            return False
    
    