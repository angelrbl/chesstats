import chess
import chess.pgn

class ChessGame:
    def __init__(self, cg):
        self.game = cg
        self.hd = cg.headers
        self.board = cg.board()
        self.white = cg.headers.get("White")
        self.black = cg.headers.get("Black")
        self.result =cg.headers.get('Result')

    def get_color_winner(self): # color winner
        if self.result == '1-0':
            return 'white'
        elif self.result == '0-1':
            return 'black'
        elif self.result in ('1/2-1/2', '½-½'):
            return 'draw'
        return None
    
    def get_winner(self):  # user winner
        winner = self.get_cwinner()
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
        moves = iter(self.game.mainline_moves())
        first_move = next(moves)
        if notation == 1:
            return self.board.san(first_move)
        else:
            return first_move

    def get_first_move_user(self, user, notation):
        moves = iter(self.game.mainline_moves())
        white_move = next(moves)
        if self.is_white(user):
            first_move = white_move
        else:
            self.board.push(white_move)
            first_move = next(moves)

        if notation == 1:
            return self.board.san(first_move)
        else:
            return first_move