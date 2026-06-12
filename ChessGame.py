import chess
import chess.pgn

class ChessGame:
    def __init__(self, cg):
        self.game = cg
        self.hd = cg.headers
        self.board = cg.board
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
            return None
        
    