#-*- coding: UTF-8 -*-

from board import TTT_Board
from minimax import TTT_Node

class Game:

    def __init__(self):

        self.bd = []
        #self.player = player
        self.role = ['O']

    def start_game(self, n):
        self.bd = TTT_Board(n)  # build the board
        self.bd.show()
        print(self.bd.check_finish())

        # setup AI
        AI = TTT_Node()
        while not self.bd.check_finish():
            pos = input("What position do you want to play?:\n")  # parse the players play
            self.bd.board[int(pos[1])][int(pos[3])] = 'O'  # need someway to alowe change role
            self.bd.show()
            # ai's move
            current_state = self.bd.board2state()
            AI.state = current_state
            AI.children = AI.find_chdrn('X')
            update_state = AI.move()
            print(update_state)
            self.bd.state2board(update_state)
            self.bd.show()


if __name__ == '__main__':
    g = Game()
    g.start_game(3)