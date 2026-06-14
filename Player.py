import chess
import chess.pgn
from ChessGame import ChessGame

class Player:
    def __init__(self, usr, pgn):
        self.username = usr
        self.games = self.filter_games(pgn)
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

    def get_first_move(self, game, notation):
        board = game.get_board()
        board.reset()
        moves = iter(game.get_moves())
        white_move = next(moves)
        if game.is_white(self.username):
            first_move = white_move
        else:
            board.push(white_move)
            first_move = next(moves)
        if notation == 1:
            return board.san(first_move)
        else:
            return first_move

    def get_first_moves(self):
        first_moves = [{},{}]
        for game in self.games:
            first_move = self.get_first_move(game, notation=1)
            if game.is_white(self.username):
                if first_move in first_moves[0].keys():
                   first_moves[0][first_move] = first_moves[0].get(first_move, 0) + 1
                else:
                    first_moves[0][first_move] = 1
            else:
                if first_move in first_moves[1].keys():
                    first_moves[1][first_move] = first_moves[0].get(first_move, 0) + 1
                else:
                    first_moves[1][first_move] = 1
        return first_moves

    def get_first_moves_matrix(self):
        first_moves = [[0]*8 for _ in range(8)]
        for game in self.games:
            first_move = self.get_first_move(game, notation=0)
            go_square = first_move.to_square
            f = chess.square_rank(go_square)
            c = chess.square_file(go_square)
            first_moves[f][c] += 1
        return first_moves 

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
            return False
        else:
            return True
    
    