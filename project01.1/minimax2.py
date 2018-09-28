# -*- coding: UTF-8 -*-
import copy

from board import TTT_Board

def copy_dict(src): # cpoy from a src dict to a dst dict
    dst = {}
    for k in src.keys():
        dst[k] = src[k][:]
    return dst


class TTT_Node:

    def __init__(self):

        self.state = {}

        self.children = []

        self.token = 'X'

        self.len = 3
        self.alpha = float('-inf')
        self.beta = float('inf')

    def state2board(self):  # b is a board object, converting a state to a board object? but there should be only one board object per game

        bd = TTT_Board(self.len)
        bd.board = [['P' for i in range(self.len)] for j in range(self.len)]

        bd.len = self.len
        for pos in self.state['X']:

            bd.board[pos[0]][pos[1]] = 'X'

        for pos in self.state['O']:
            bd.board[pos[0]][pos[1]] = 'O'
        return bd

    def find_chdrn(self, token):  # find children of the next move of token
        children = []
        for pos in self.state['P']:
            #
            new_state = TTT_Node()
            new_state.state = copy_dict(self.state)  # copy the original dict
            new_state.state['P'].remove(pos)
            new_state.state[token].append(pos)
            children.append(new_state)
        return children

    def score(self, token, alpha, beta):  # token == token of the next move; alpha, beta are father's
        if self.check_finish() == 0:
            scores = []

            next_token = 'X' if token == 'O' else 'O'
            for ch in self.find_chdrn(token):
                ch_score = ch.score(next_token, alpha, beta)  # score of X's child
                if token == self.token:   # choose max
                    scores.append(ch_score)
                    if ch_score > alpha:  # update the min/alpha value
                        alpha = ch_score

                    if alpha >= beta:
                        break

                if next_token == self.token:   # choose min
                    scores.append(ch_score)
                    if ch_score < beta:   # update the max/beta value
                        beta = ch_score

                    if beta <= alpha:
                        break

            if token == self.token:   #alpha beta  purning here
                return max(scores)
            else:

                return min(scores)
        else:
            f = self.check_finish()
            return f

    def check_finish(self):

        bd = TTT_Board(self.len)
        bd.state2board(self.state)
        another_token = 'X' if self.token == 'O' else 'O'
        if bd.check_finish() == self.token:
            return 1
        elif bd.check_finish() == another_token:
            return -1
        if self.state['P'] == []:
            return 0.001
        return 0
    """
    def check_finish2(self, token):

        n = 3

        X_pos = []
        factor = 1 if token == self.token else -1
        for i in zip(*self.state[token]):
            X_pos.append(sorted(i))
        print(X_pos)
        if len(X_pos[0]) == len(X_pos[1]) == n:
            if X_pos[0][0] == X_pos[0][-1] and X_pos[1][0] == 0 and X_pos[1][-1] == n-1:
                return 2*factor
            if X_pos[1][0] == X_pos[1][-1] and X_pos[0][0] == 0 and X_pos[0][-1] == n-1:
                return 2*factor

        if self.state['P'] == []:
            return 1
        return 0
    """

    def move(self):
        max_score = -float('inf')
        other_token = 'X' if self.token == 'O' else 'O'
        move = []
        for ch in self.children:
            al = float('-inf')
            be = float('inf')
            s = ch.score(other_token,al,be)
            if s >= max_score:
                max_score = s
                move = [ch]
            elif s == max_score:
                move.append(ch)
            self.state = move[-1].state

        return move[-1].state


if __name__ == '__main__':
    ttt = TTT_Node()
    ttt.state = {'X': [(0, 0),(0, 1)], 'O': [(1, 0), (1, 1)], 'P': [(0, 2), (1, 2)]}
    ttt.children = ttt.find_chdrn('X')
    #alph = float('-inf')
    #bet = float('inf')
    #print(ttt.score('X', alph, bet))

    #ch = ttt.find_chdrn('X')

    #print(ttt.move())
    #ttt.state2board().show()