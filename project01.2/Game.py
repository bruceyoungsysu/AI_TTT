#-*- coding: UTF-8 -*-

from board import TTT_Board,TTT3_board
from minimax import TTT3_Node

class Game:

    def __init__(self):

        self.bd = []
        #self.player = player
        self.role = ['O']

    def start_game(self, n=3):
        self.bd = TTT3_board()  # build the board
        self.bd.show()
        AI = TTT3_Node()
        while True:
            pos1 = input("Which board do you want to play?:\n")  # parse the players play
            pos2 = input("Which position do you want to play?:\n")
            self.bd.big_board[int(pos1[1])][int(pos1[3])].board[int(pos2[1])][int(pos2[3])] = 'O'
            # update the board state
            current_state = self.bd.big_board[int(pos1[1])][int(pos1[3])].board2state()
            self.bd.state[int(pos1[1])][int(pos1[3])] = current_state
            self.bd.show()
            self.bd.next_bd_cor = (int(pos2[1]),int(pos2[3])) # the board AI will play on

            AI.state = self.bd.state
            AI.childen = AI.find_chdrn('X',self.bd.next_bd_cor)
            AI_mv, AI_cor = AI.move(self.bd.next_bd_cor)
            print(AI_mv)
            self.bd.state = AI.state
            self.bd.big_board = self.bd.state2board(self.bd.next_bd_cor, AI_mv[self.bd.next_bd_cor[0]][self.bd.next_bd_cor[1]])
            self.bd.show()
            print('You should play on board at ' + str(AI_cor))

if __name__ == '__main__':
    g = Game()
    g.start_game(3)