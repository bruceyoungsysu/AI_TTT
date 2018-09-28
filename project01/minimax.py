# -*- coding: UTF-8 -*-
import copy
from board import TTT_Board


class TTT_Node:

    def __init__(self):

        self.state = {}

        self.children = []

        self.token = 'X'

        self.len = 3

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

            new_state = TTT_Node()
            new_state.state = copy.deepcopy(self.state)  # copy the original dict
            new_state.state['P'].remove(pos)
            new_state.state[token].append(pos)
            children.append(new_state)

        return children

    def score(self, token):  # token == token of the next move

        if self.check_finish() == False:
            scores = []

            next_token = 'X' if token == 'O' else 'O'
            for ch in self.find_chdrn(token):
                scores.append(ch.score(next_token))
            if token == self.token:
                return max(scores)
            else:
                return min(scores)
        else:
            return self.check_finish()

    def check_finish(self):

        bd = TTT_Board(self.len)
        bd.state2board(self.state)
        another_token = 'X' if self.token == 'O' else 'O'
        if bd.check_finish() == self.token:
            return 2
        elif bd.check_finish() == another_token:
            return -2
        if self.state['P'] == []:
            return 1
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
            s = ch.score(other_token)
            print(s, ch.state)
            if s >= max_score:
                max_score = s
                move = [ch]
            elif s == max_score:
                move.append(ch)
            self.state = move[-1].state

        return move[-1].state


if __name__ == '__main__':
    ttt = TTT_Node()
    ttt.state = {'X': [(0, 1), (2, 0), (2, 2)], 'O': [(0, 0), (0, 2), (1, 1), (1, 2)], 'P': [(2, 1), (1, 0)]}
    print(ttt.check_finish())
    ttt.children = ttt.find_chdrn('X')
    ch = ttt.find_chdrn('X')
    print(ttt.score('X'))

    print(ttt.move())
    ttt.state2board().show()