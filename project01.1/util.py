#-*- coding: UTF-8 -*-

from minimax2 import TTT_Node
import copy


def score2(state, token, alpha, beta):  # token == token of the next move; alpha, beta are father's
    nd = TTT_Node()
    nd.state = state
    if nd.check_finish() == 0:
        min_score = float('inf')
        max_score = float('-inf')
        next_token = 'X' if token == 'O' else 'O'
        for ch in nd.find_chdrn(token):
            ch_score = score2(ch.state, next_token, alpha, beta)  # score of X's child

            if token == nd.token:  # choose max
                if ch_score > max_score:  # update the min/alpha value
                    max_score = ch_score
                    alpha = ch_score
                if alpha >= beta:
                    break

            if next_token == nd.token:  # choose min
                if ch_score < min_score:  # update the max/beta value
                    min_score = ch_score
                    beta = ch_score

                if beta <= alpha:
                    break

        if token == nd.token:
            return max_score
        else:

            return min_score
    else:
        f = nd.check_finish()
        return f


def score3(token, state):
    another_token = 'O' if token=='X' else 'X'
    diff = len(state[token]) - len(state[another_token])
    #if diff<=-6:
    #    return 1
    s = (diff)/3
    return s

def score4(token, state):
    another_token = 'O' if token == 'X' else 'X'


def copy_dict(src): # cpoy from a src dict to a dst dict
    dst = {}
    for k in src.keys():
        dst[k] = src[k][:]
    return dst


def copy_state(state): # copy a source state to a dst dict
    dst = []
    for line in state:
        c = []
        for col in line:
            c.append(copy_dict(col))
        dst.append(c)
    return dst


if __name__ == '__main__':
    s = {'X': [(1, 0), (1, 2)], 'O': [(0, 2),(0, 0)], 'P': [(0, 1),(1,1)]}
    alpha =float('-inf')
    beta = float('inf')
    print(score3('X', s))  # score2 only can score for cpu = 'X' case