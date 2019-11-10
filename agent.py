#!/usr/bin/env python3

"""
Basic framework for developing 2048 programs in Python

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NCTU, Taiwan
        http://www.aigames.nctu.edu.tw
"""

from board import board
from action import action
from operator import itemgetter
from weight import weight
from array import array
import random
import sys

class agent:
    """ base agent """
    
    def __init__(self, options = ""):
        self.info = {}
        options = "name=unknown role=unknown " + options
        for option in options.split():
            data = option.split("=", 1) + [True]
            self.info[data[0]] = data[1]
        return

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        return
    
    def open_episode(self, flag = ""):
        return
    
    def close_episode(self, flag = ""):
        return
    
    def take_action(self, state):
        return action()
    
    def check_for_win(self, state):
        return False
    
    def property(self, key):
        return self.info[key] if key in self.info else None
    
    def notify(self, message):
        data = message.split("=", 1) + [True]
        self.info[data[0]] = data[1]
        return
    
    def name(self):
        return self.property("name")
    
    def role(self):
        return self.property("role")


class random_agent(agent):
    """ base agent for agents with random behavior """
    
    def __init__(self, options = ""):
        super().__init__(options)
        seed = self.property("seed")
        if seed is not None:
            random.seed(int(seed))
        return
    
    def choice(self, seq):
        target = random.choice(seq)
        return target
    
    def shuffle(self, seq):
        random.shuffle(seq)
        return
class weight_agent(agent):
    """ base agent for agents with weight tables """
    
    def __init__(self, options = ""):
        super().__init__(options)
        self.net = []
        self.tuple_list = [[ 0,  1,  2,  3], # 4 rows
                           [ 4,  5,  6,  7],
                           [ 8,  9, 10, 11],
                           [12, 13, 14, 15],
                           [ 0,  4,  8, 12], # 4 column
                           [ 1,  5,  9, 13],
                           [ 2,  6, 10, 14],
                           [ 3,  7, 11, 15],
                           [ 0,  1,  4,  5], # 9 cube
                           [ 1,  2,  5,  6],
                           [ 2,  3,  6,  7],
                           [ 4,  5,  8,  9],
                           [ 5,  6,  9, 10],
                           [ 6,  7, 10, 11],
                           [ 8,  9, 12, 13],
                           [ 9, 10, 13, 14],
                           [10, 11, 14, 15]]
        init = self.property("init")
        if init is not None:
            self.init_weights(init)
        load = self.property("load")
        if load is not None:
            self.load_weights(load)
        return
    
    def __exit__(self, exc_type, exc_value, traceback):
        save = self.property("save")
        if save is not None:
            self.save_weights(save)
        return
    
    def init_weights(self, info):
        for _ in range(8):
            self.net += [weight(65536)]
        return
    
    def load_weights(self, path):
        input = open(path, 'rb')
        size = array('L')
        size.fromfile(input, 1)
        size = size[0]
        for i in range(size):
            self.net += [weight()]
            self.net[-1].load(input)
        return
    def save_weights(self, path):
        output = open(path, 'wb')
        array('L', [len(self.net)]).tofile(output)
        for w in self.net:
            w.save(output)
        return

    def V(self, state):
        result = 0
        for i in range(8):
            feature = 0
            for _ in self.tuple_list[i]:
                feature = feature * 15 + state[_]
            result += self.net[i][feature]
        return result

class learning_agent(agent):
    """ base agent for agents with a learning rate """
    
    def __init__(self, options = ""):
        super().__init__(options)
        self.alpha = 0.1
        alpha = self.property("alpha")
        if alpha is not None:
            self.alpha = float(alpha)
        return

class rndenv(random_agent):
    """
    random environment
    add a new random tile to an empty cell
    2-tile: 90%
    4-tile: 10%
    """
    def __init__(self, options = ""):
        super().__init__("name=random role=environment " + options)
        self.bag = [1,2,3]
        return
    
    def take_action(self, state, weight = None):
        empty = [pos for pos, tile in enumerate(state.state) if not tile]
        fil = [[12,13,14,15],[0,4,8,12],[0,1,2,3],[3,7,11,15]]
        if state.op is not None:
            empty = list(filter(lambda x: x in fil[state.op], empty))
        if empty:
            pos = self.choice(empty)
            if self.bag == []:
                self.bag = [1,2,3]
            tile = self.choice(self.bag)
            self.bag.remove(tile)
            return action.place(pos, tile)
        else:
            return action()

    def reset(self):
        self.bag=[1,2,3]
        return    
    
class player(random_agent):
    """
    dummy player
    select a legal action randomly
    """
    
    def __init__(self, options = ""):
        super().__init__("name=dummy role=player " + options)
        self.weight = weight_agent(options)
        self.weight.init_weights("")
        return
    
    def take_action(self, state,):
        #evaluate
        legal = list(filter(lambda x:x[1] != -1,[ (op,board(state).slide(op) + self.weight.V(state)) for op in range(4) ]))
        if legal:
            op =  max(legal,key=itemgetter(1))[0]
            state.op = op
            return action.slide(op)
        else:
            return action()
    
if __name__ == '__main__':
    print('2048 Demo: agent.py\n')
    pass