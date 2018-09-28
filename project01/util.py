#-*- coding: UTF-8 -*-

def check_finish(arr):  # check whether a player win， put it in Game class

    def isSame(state):
        arr.sort()
        if arr[0] == arr[-1]:
            return True
        else:
            return False

    diag = []

    for i in range(self.len):
        row = self.state[1][:]
        col = self.state[:][1]
        diag.append(self.state[i][i])

        if ('P' not in row) and isSame(row):
            return True
        if ('P' not in col) and isSame(col):
            return True

    if ('P' not in diag) and isSame(diag):
        return True