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
    nd = TTT_Node()
    nd.state = state

    if nd.check_finish():
        return nd.check_finish()
    another_token = 'O' if token == 'X' else 'X'
    diff = len(state[token]) - len(state[another_token])
    s = (diff)/3

    my_s4 = score4(token,state)
    en_s4 = score4(another_token,state)
    if my_s4==0 and en_s4 ==0:
        factor = 0
    else:
        factor = (my_s4-en_s4)/(my_s4+en_s4)
    #print(factor)
    return factor*0.5

def score4(token, state): # compute the factor
    token = 'X'
    another_token = 'O' if token == 'X' else 'X'
    my_states = state[token]
    enemy_states = state[another_token]
    # check lines
    my_lines = [x[0] for x in my_states]
    enemy_lines = [x[0] for x in enemy_states]
    available_lines = []
    for l in my_lines:
        if l not in enemy_lines:
            available_lines.append(l)
    line_score = len(available_lines)
    # check cols
    my_cols = [x[1] for x in my_states]
    enemy_cols = [x[1] for x in enemy_states]
    available_cols = []
    for l in my_cols:
        if l not in enemy_cols:
            available_cols.append(l)
    col_score = len(available_cols)

    # check diags
    d1_score = 0
    diag1 = [(0,0),(1,1),(2,2)]
    for d1 in diag1:
        if d1 in my_states:
            d1_score += 1
        elif d1 in enemy_states:
            d1_score = 0
            break

    d2_score = 0
    diag2 = [(0, 2), (1, 1), (2, 0)]
    for d2 in diag2:
        if d2 in my_states:
            d2_score += 1
        elif d2 in enemy_states:
            d2_score = 0
            break

    tt_score = line_score+col_score+d1_score+d2_score

    return tt_score


def fullbd_score(scr_lis): # scores will not change if the token taken by computer if not changed
    lines = [sum(i) for i in scr_lis]

    cols = []
    for j in range(3):
        cols.append(sum([x[j] for x in scr_lis]))

    diag = []
    diag.append(scr_lis[0][0]+scr_lis[1][1]+scr_lis[2][2])
    diag.append(scr_lis[0][2] + scr_lis[1][1] + scr_lis[2][0])

    all = lines+cols+diag

    return max(all)-abs(min(all))


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
    s = {'X': [(2, 1)], 'O': [(1, 1)], 'P': [(2, 0),(0, 2),(0, 0), (0, 1),  (1, 0), (1, 2), (2, 1)]}
    s2 = {'X': [(1, 2)], 'O': [(0, 0)], 'P': [(2, 2), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1)]}
    alpha =float('-inf')
    beta = float('inf')
    #print(score3('O', s2))  # score2 only can score for cpu = 'X' case
    print(score2(s2,'X',float('-inf'), float('inf')))