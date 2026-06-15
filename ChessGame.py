import chess
import chess.pgn

class ChessGame:
    def __init__(self, game):
        self.game = game
        self.hd = game.headers
        self.board = game.board()
        self.white = game.headers.get("White")
        self.black = game.headers.get("Black")
        self.result = game.headers.get('Result')
        self.moves = game.mainline_moves()

    def get_color_winner(self): # color winner
        if self.result == '1-0':
            return 'white'
        elif self.result == '0-1':
            return 'black'
        elif self.result in ('1/2-1/2', '½-½'):
            return 'draw'
        return None
    
    def get_winner(self):  # user winner
        winner = self.get_color_winner()
        if winner == "white":
            return self.white
        elif winner == "black":
            return self.black
        else:
            return winner

    def is_white(self, user):
        if user == self.white:
            return True
        elif user == self.black:
            return False
        else:
            raise Exception("The user given did not play this game")

    def get_color(self, user):
        if self.is_white(user):
            return "white"
        else:
            return "black"

    def get_first_move(self, notation):
        moves = iter(self.moves)
        self.board.reset()
        first_move = next(moves)
        if notation == 1:
            return self.board.san(first_move)
        else:
            return first_move

    def is_piece_taken(self, move):
        move = self.board.san(move)
        return move[1] == 'x'
    
    def get_first_taken(self):
        i = 0
        j = 0
        self.board.reset()
        for move in self.moves:
            if self.is_piece_taken(move):
                return (self.board.san(move), j, i)
            self.board.push(move)
            i += 1
            if i % 2 == 0:
                j += 1


    def get_game(self):
        return self.game
    def get_white(self):
        return self.white
    def get_black(self):
        return self.black
    def get_result(self):
        return self.result
    def get_board(self):
        return self.board
    def get_moves(self):
        return self.moves