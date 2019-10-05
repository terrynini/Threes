#!/usr/bin/env python3

"""
Basic framework for developing 2048 programs in Python

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NCTU, Taiwan
        http://www.aigames.nctu.edu.tw
"""

class board:
    """ simple implementation of 2048 puzzle """
    score = [0, 1, 2, 3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072, 6144]
    op = None
    def __init__(self, state = None):
        self.state = state[:] if state is not None else [0] * 16
        return
    
    def __getitem__(self, pos):
        return self.state[pos]
    
    def __setitem__(self, pos, tile):
        self.state[pos] = tile
        return
    
    def place(self, pos, tile):
        """
        place a tile (index value) to the specific position (1-d form index)
        return 0 if the action is valid, or -1 if not
        """
        if pos >= 16 or pos < 0:
            return -1
        self.state[pos] = tile
        return 0
    
    def slide(self, opcode):
        """
        apply an action to the board
        return the reward of the action, or -1 if the action is illegal
        """
        self.op = opcode
        if opcode == 0:
            return self.slide_up()
        if opcode == 1:
            return self.slide_right()
        if opcode == 2:
            return self.slide_down()
        if opcode == 3:
            return self.slide_left()
        return -1
    
    def slide_left(self):
        move, score = [], 0
        for row in [self.state[r:r + 4] for r in range(0, 16, 4)]:
            for i in range(len(row)-1):
                if row[i] == 0 :
                    if row[i+1] != 0:
                        t = row[i+1]
                        row[i+1] = row[i]
                        row[i] = t
                elif row[i] in [1,2]:
                    if row[i+1] != row[i] and row[i+1] in [1,2]:
                        row[i] = 3
                        row[i+1] = 0
                        score += self.score[row[i]]
                elif row[i] == row[i+1]:
                    row[i] += 1
                    row[i+1] = 0
                    score += self.score[row[0]]
                move += [row[i]]
            move += [row[-1]]
        if move != self.state:
            self.state = move
            return score
        return -1
    
    def slide_right(self):
        self.reflect_horizontal()
        score = self.slide_left()
        self.reflect_horizontal()
        return score
    
    def slide_up(self):
        self.transpose()
        score = self.slide_left()
        self.transpose()
        return score
    
    def slide_down(self):
        self.transpose()
        score = self.slide_right()
        self.transpose()
        return score
    
    def reflect_horizontal(self):
        self.state = [self.state[r + i] for r in range(0, 16, 4) for i in reversed(range(4))]
        return
    
    def reflect_vertical(self):
        self.state = [self.state[c + i] for c in reversed(range(0, 16, 4)) for i in range(4)]
        return
    
    def transpose(self):
        self.state = [self.state[r + i] for i in range(4) for r in range(0, 16, 4)]
        return
    
    def rotate(self, rot = 1):
        rot = ((rot % 4) + 4) % 4
        if rot == 1:
            self.rotate_right()
            return
        if rot == 2:
            self.reverse()
            return
        if rot == 3:
            self.rotate_left()
            return
        return
    
    def rotate_right(self):
        """ clockwise rotate the board """
        self.transpose()
        self.reflect_horizontal()
        return
    
    def rotate_left(self):
        """ counterclockwise rotate the board """
        self.transpose()
        self.reflect_vertical()
        return
    
    def reverse(self):
        self.reflect_horizontal()
        self.reflect_vertical()
        return
        
    def __str__(self):
        state = '+' + '-' * 24 + '+\n'
        for row in [self.state[r:r + 4] for r in range(0, 16, 4)]:
            state += ('|' + ''.join('{0:6d}'.format(self.score[t]) for t in row) + '|\n')
        state += '+' + '-' * 24 + '+'
        return state
    
    
if __name__ == '__main__':
    print('2048 Demo: board.py\n')
    
    state = board()
    state[10] = 10
    print(state)
    