
class TTT_Board:

    def __init__(self, n):

        self.len = n
        self.board = [['P' for i in range(self.len)] for j in range(self.len)]
        self.next_player = []
        # self.state = {'X': [], 'O': [], 'P': []}

    def show(self):
        print("the current board is: \n")
        for i in range(self.len):
            print(self.board[i], '\n')

    def state2board(self, state):

        for pos in state['X']:
            self.board[pos[0]][pos[1]] = 'X'
        for pos in state['O']:
            self.board[pos[0]][pos[1]] = 'O'

    def board2state(self):
        state = {'X': [], 'O': [], 'P': []}
        for i in range(self.len):
            for j in range(self.len):
                current = self.board[i][j]
                if current == 'X':
                    state['X'].append((i, j))
                elif current == 'O':
                    state['O'].append((i, j))
                elif current == 'P':
                    state['P'].append((i, j))
                else:
                    return 'error'
        return state

    def check_finish(self): #test
        # check horizontal and verticle
        for i in range(self.len):
            row = sorted(self.board[i][:])
            col = sorted([a[i] for a in self.board])
            if row[0] == row[-1] and (row[0] != 'P'):
                return row[0]
            if col[0] == col[-1] and (col[0] != 'P'):
                return col[0]
        # check diag line
        diag1 = sorted([self.board[i][i] for i in range(self.len)])
        if diag1[0] == diag1[-1] and (diag1[0] != 'P'):
            return diag1[0]

        diag2 = sorted([self.board[i][self.len-i-1] for i in range(self.len)])
        if diag2[0] == diag2[-1] and (diag2[0] != 'P'):
            return diag2[0]
        return False


if __name__ == '__main__':

    s = {'X': [(0,0),  (2, 0)], 'O': [(1, 2)], 'P': [(1, 0),(2, 1), (0, 1), (1, 1), (0, 2),(2, 2)]}
    bd = TTT_Board(3)
    bd.state2board(s)
    bd.show()
    print(bd.check_finish())
