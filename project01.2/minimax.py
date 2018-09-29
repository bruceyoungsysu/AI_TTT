# -*- coding: UTF-8 -*-
import copy
from board import TTT_Board
from util import score2,score3
from util import copy_dict, copy_state
import random


class TTT3_Node:

    def __init__(self):
        state = {'X': [(2, 0), (2, 2)], 'O': [(0, 0), (0, 2), (1, 1), (1, 2)], 'P': [(0, 1), (2, 1), (1, 0)]}

        self.state = [[copy_dict(state) for i in range(3)] for j in range(3)]

        self.children = []
        self.depth = 0
        self.token = 'X'

        self.len = 3
        self.index = [[i,j] for i in range(3) for j in range(3)]

    def state2board(self):  # b is a board object, converting a state to a board object? but there should be only one board object per game

        bd = TTT_Board(self.len)
        bd.board = [['P' for i in range(self.len)] for j in range(self.len)]

        bd.len = self.len
        for pos in self.state['X']:

            bd.board[pos[0]][pos[1]] = 'X'

        for pos in self.state['O']:
            bd.board[pos[0]][pos[1]] = 'O'
        return bd

    def find_chdrn(self, token, ind):  # find children of the next move of token
        ind = list(ind)
        def find_chdrn2(token, state):  # find children of the next move of token

            children = []
            for pos in state['P']:
                new_state= copy_dict(state)  # copy the original dict
                new_state['P'].remove(pos)
                new_state[token].append(pos)
                children.append(new_state)
            return children

        children = []
        children_mv_pos = []
        state = self.state[ind[0]][ind[1]]

        bd = TTT_Board(3)
        bd.state2board(state)

        while bd.check_finish():
            ind[0] = random.randint(0,2)
            ind[1] = random.randint(0,2)
            state = self.state[ind[0]][ind[1]]
            bd = TTT_Board(3)
            bd.state2board(state)

        sub_ch = find_chdrn2(token, state)
        for ch in sub_ch:
            new_mv = list(set(ch[token])-set(state[token]))

            state_cp = copy_state(self.state)
            state_cp[ind[0]][ind[1]] = ch
            new_nd = TTT3_Node()
            new_nd.state = state_cp
            children.append(new_nd)
            children_mv_pos.append(new_mv[0])
        self.children = children
        return children, children_mv_pos

    def score(self, depth, token, cor, alpha, beta):
        depth += 1
        #print(depth)
        another_token = 'O' if token == 'X' else 'X'
        if (self.check_finish() != 0) and depth <= 3:
            min_score = float('inf')
            max_score = float('-inf')
            substates = self.find_chdrn(token,cor)
            chs = substates[0]  # level 1 children
            chs_pos = substates[1]
            for n in range(len(chs_pos)): # check the score of each children
                ch = chs[n]  #level 1 child
                ch_pos = chs_pos[0]  # level 1 child play position
                s = ch.score(depth, another_token, ch_pos, alpha, beta)
                if token == self.token:
                    if s > max_score:
                        max_score = s
                        alpha = max_score
                    if alpha >= beta:
                        #print('works!')
                        break
                if another_token == self.token:
                    if s < min_score:
                        min_score = s
                        beta = min_score
                    if beta <= alpha:
                        #print('works!')
                        break
            if token == self.token:
                return max_score
            else:
                return min_score
        else:
            aa = float('-inf')
            bb = float('inf')
            total_score = 0
            for inde in self.index:  # check whether it is the board playing
                if inde[0] == cor[0] and inde[1] == cor[1]:
                    s = score2(self.state[inde[0]][inde[1]], token, aa, bb)
                else:
                    s = score3(token, self.state[inde[0]][inde[1]])
                #print(s)
                total_score += s
            return total_score

    def check_finish2(self):  # check to win as many as possible
        finish_score = 0
        for inde in self.index:
            s = self.state[inde[0]][inde[1]]
            bd = TTT_Board(self.len)
            bd.state2board(s)
            another_token = 'X' if self.token == 'O' else 'O'
            if not bd.check_finish():
                return 0
            else:
                if bd.check_finish() == self.token:
                    finish_score += 1
                elif bd.check_finish() == another_token:
                    finish_score -= 1
                elif s['P'] == []:
                    finish_score += 0.0000001
        return finish_score

    def check_finish(self):  # check to win single
        for inde in self.index:
            s = self.state[inde[0]][inde[1]]
            bd = TTT_Board(self.len)
            bd.state2board(s)
            another_token = 'X' if self.token == 'O' else 'O'
            if bd.check_finish() == self.token:
                return 1
            elif bd.check_finish() == another_token:
                return -1
            if s['P'] == []:
                return 0.001
        return 0


    def move(self, cor):
        print('Thinking...')
        max_score = -float('inf')
        other_token = 'X' if self.token == 'O' else 'O'
        move = []
        self.children, children_pos = self.find_chdrn(self.token,cor)
        for ch_num in range(len(self.children)):
            ch = self.children[ch_num]
            ch_pos = children_pos[ch_num]
            s = ch.score(self.depth, other_token, ch_pos, float('-inf'), float('inf'))
            if s >= max_score:
                max_score = s
                move = [ch]
            elif s == max_score:
                move.append(ch)
        mv = move[-1].state
        for ind in self.index:
            if self.state[ind[0]][ind[1]] != mv[ind[0]][ind[1]]:
                pre = self.state[ind[0]][ind[1]]
                aft = mv[ind[0]][ind[1]]
                mv_pos = set(aft[self.token]) - set(pre[self.token])
                self.state[ind[0]][ind[1]] = mv[ind[0]][ind[1]]
                #print(pre)
                #print(aft)
                return mv, mv_pos


if __name__ == '__main__':
    ttt = TTT3_Node()

    ttt.state = [[{'X': [(1, 2)], 'O': [(0, 0)], 'P': [(2, 2), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1)]},
                  {'X': [], 'O': [(1, 2)], 'P': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2)]},
                  {'X': [(1, 0), (1, 1)], 'O': [(0, 2), (1, 2)], 'P': [(0, 0), (0, 1), (2, 0), (2, 1), (2, 2)]}],
                 [{'X': [(2, 0)], 'O': [(2, 2)], 'P': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)]},
                  {'X': [(2, 1), (2, 2)], 'O': [(1, 1), (2, 0)], 'P': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]},
                  {'X': [(0, 1), (1, 2), (0, 0)], 'O': [(0, 2), (2, 1)], 'P': [(1, 0), (1, 1), (2, 0), (2, 2)]}],
                 [{'X': [(2, 0), (0, 2)], 'O': [(0, 0), (1, 0)], 'P': [(0, 1), (1, 1), (1, 2), (2, 1), (2, 2)]},
                  {'X': [(0, 2)], 'O': [(2, 0)], 'P': [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2)]},
                  {'X': [(2, 2)], 'O': [(1, 1), (1, 2)], 'P': [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1)]}]]

    """
    ttt.state = [[{'X': [], 'O': [], 'P': [(1, 1), (2, 1),(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]},
                  {'X': [], 'O': [], 'P': [(1, 1), (2, 1),(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]},
                  {'X': [], 'O': [], 'P': [(2, 2), (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]}],
                 [{'X': [], 'O': [], 'P': [(1, 1), (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]},
                  {'X': [], 'O': [(1, 1)], 'P': [(2, 1),(0, 0),(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]},
                  {'X': [], 'O': [], 'P': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]}],
                 [{'X': [], 'O': [], 'P': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]},
                  {'X': [], 'O': [], 'P': [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]},
                  {'X': [], 'O': [], 'P': [(0, 1), (0, 2), (0, 0), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]}]]
    """

    a = float('-inf')
    b = float('inf')
    print('sss'+str(ttt.score(0,'X',(0,0), a, b)))

    print(ttt.move((0,0)))
    #print(ttt.check_finish())
    #print(ttt.check_finish())
    #ttt.children = ttt.find_chdrn('X')
    #ch = ttt.find_chdrn('X')
    #print(ttt.score('X'))

    #print(ttt.move())
    #ttt.state2board().show()