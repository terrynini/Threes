#!/usr/bin/env python3

"""
Framework for 2048 & 2048-like Games (Python 3)

Author: Hung Guei (moporgic)
        Computer Games and Intelligence (CGI) Lab, NCTU, Taiwan
        http://www.aigames.nctu.edu.tw
"""

from board import board
from action import action
from episode import episode
from statistic import statistic
from agent import player
from agent import rndenv
from agent import weight_agent
import sys


if __name__ == '__main__':
    print('threes Demo: ' + " ".join(sys.argv))
    print()
    
    total, block, limit = 1000, 0, 0
    play_args, evil_args = "", ""
    load, save = "", ""
    summary = False
    for para in sys.argv[1:]:
        if "--total=" in para:
            total = int(para[(para.index("=") + 1):])
        elif "--block=" in para:
            block = int(para[(para.index("=") + 1):])
        elif "--limit=" in para:
            limit = int(para[(para.index("=") + 1):])
        elif "--play=" in para:
            play_args = para[(para.index("=") + 1):]
        elif "--evil=" in para:
            evil_args = para[(para.index("=") + 1):]
        elif "--load=" in para:
            load = para[(para.index("=") + 1):]
        elif "--save=" in para:
            save = para[(para.index("=") + 1):]
        elif "--summary" in para:
            summary = True
    
    stat = statistic(total, block, limit)
    
    if load:
        input = open(load, "r")
        stat.load(input)
        input.close()
        summary |= stat.is_finished()
    
    with player(play_args) as play, rndenv(evil_args) as evil, weight_agent(play_args) as weight:
        while not stat.is_finished():
            #play.open_episode("~:" + evil.name())
            #evil.open_episode(play.name() + ":~")
            stat.open_episode(play.name() + ":" + evil.name())
            game = stat.back()
            evil.reset()
            for _ in range(9):
                game.apply_action(evil.take_action(game.state()))
            while True:
                #who = game.take_turns(play, evil)
                game.ep_time = game.millisec()
                if not game.apply_action(play.take_action(game.state(),weight)) :#or who.check_for_win(game.state()):
                    break
                cstate = board(game.state())
                game.ep_time = game.millisec()
                game.apply_action(evil.take_action(game.state()))
                play.learning(cstate, game.state(), weight)
            win = game.last_turns(play, evil)
            stat.close_episode(win.name())
            #break
            #play.close_episode(win.name())
            #evil.close_episode(win.name())
    if summary:
        stat.summary()
    
    if save:
        output = open(save, "w")
        stat.save(output)
        output.close()