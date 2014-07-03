from game_funcs import *
import sys
import os
import random as ran
import copy
from config import *
from kismet_scorecard import *
import time

sys.path.append('../AI/')
from AI_shell import *

def AI_keep_or_score(hand_dice, game_info):
    """decides what the payer must do given the turn state of the game"""
    from game_funcs import score_repor, print_options
    options = score_repor(hand_dice, game_info)
    if game_info['roll']<3:
        options.append((999,'cont_roll','choose dice and continue rolling', -1))
    options = dict([[a[0], a[1:]] for a in options])
    print_options(options)    
    
    choice, hand_dice = AI_choose_option(options, game_info['scorecard'],game_info['roll'], hand_dice)
    print "Computer chooses %d" %choice
    if choice == 999:
        new_hand=False
    else:
        new_hand = True
        game_info['scorecard'].update_score(options[choice][0],options[choice][2], game_info['roll'], hand_dice)
    return new_hand, hand_dice

if __name__ == "__main__":
    game_info = {
        'scorecard':scorecard("computer"),
        'seed':get_seed(),
        'status':-1,
        'to_store':0
        }

    storefile =  '/home/ameert/git_projects/kismet/data/computer_records.dat'

    ran.seed(game_info['seed'])
    
    while game_info['status']<0:
        game_info['roll']=1
        new_hand = False
        hand_dice = roll_dice(5)
        while not new_hand:
            disp_dice([a.number for a in  hand_dice])
            new_hand, to_keep = AI_keep_or_score(hand_dice, game_info)
            game_info['roll'] +=1
            hand_dice = to_keep + roll_dice(5-len(to_keep))
        print game_info['scorecard'].print_card()
        time.sleep(1)
        if card_full(game_info['scorecard']):
            game_info['status']=0
    
    if game_info['to_store'] ==1 and game_info['status'] == 0:
        store_results(game_info, storefile)
