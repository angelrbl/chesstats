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
        pgn.seek(0)
        file_game = chess.pgn.read_game(pgn) 
        while file_game is not None:
            game = ChessGame(file_game)
            if(game.get_white() == self.username or game.get_black() == self.username):
                chess_games.append(game)
            file_game = chess.pgn.read_game(pgn) 
        pgn.seek(0)
        return chess_games
    
    def get_winning_rate(self):
        if self.GAME_NUM == 0:
            return 0
        return f"{(self.get_win_count() / self.GAME_NUM) * 100:.1f} %"

    def get_first_move(self, game, notation):
        board = game.get_board()
        board.reset()
        moves = iter(game.get_moves())
        white_move = next(moves)
        if self.is_white(game):
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
            if self.is_white(game):
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

    def took(self, game, move_index):
        move = game.find_move(move_index, notation=0)
        if game.get_board().turn == self.is_white(game) and game.is_a_capture(move):
            return True
        else:
            return False
        
    def get_first_capture(self, game_index):
        game = self.games[game_index]
        for i in range(game.MOVE_COUNT):
            if self.took(game, i):
                return (game.find_move(i, notation=1), i//2 ,i)
        return False

    def is_white(self, game):
        if game.is_white(self.username):
            return True
        else:
            return False

    def get_win_count(self):
        wins = 0
        for game in self.games:
            if self.won(game):
                wins += 1
        return wins
    
    def get_draw_count(self):
        draws = 0
        for game in self.games:
            if self.drew(game):
                draws += 1 
        return draws


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
    
    def get_games(self):
        return self.games
    def get_username(self):
        return self.username

#IDEA: COMPARAR PARTIDAS CON LAS DE UN POSIBLE RIVAL 
