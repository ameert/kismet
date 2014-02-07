from game_funcs import *
import sys
import os
import random as ran
import copy
from config import *
from kismet_scorecard import *
import time

game_info = {
    'scorecard':scorecard("computer"),
    'seed':get_seed(),
    'status':-1,
    'to_store':1
    }

storefile =  '/home/ameert/git_projects/kismet/data/computer_records.dat'


def keep_or_score(hand_dice, game_info):
    """decides what the payer must do given the turn state of the game"""
    options = score_repor(hand_dice, game_info)
    if game_info['roll']<3:
        options.append((999,'cont_roll','choose dice and continue rolling', -1))
    options = dict([[a[0], a[1:]] for a in options])
    if 999 in options.keys():
        choice = 999
    else: 
        best = (-1,-1)
        for a in options.items():
            if a[1][2] > best[1]:
                best = (a[0], a[1][2])
        choice = best[0]

    if choice == 999:
        new_hand=False
        hand_dice = choose_keepdie(hand_dice)
    else:
        new_hand = True
        game_info['scorecard'].update_score(options[choice][0],options[choice][2])
    return new_hand, hand_dice

def choose_keepdie(hand_dice):
    letters = ['a','b','c','d','e']
    dice_dict = dict(zip(letters,hand_dice))
    to_keep = ['a','b','c']
    
    return [dice_dict[key] for key in to_keep]


if __name__ == "__main__":
    ran.seed(game_info['seed'])
    
    while game_info['status']<0:
        game_info['roll']=1
        new_hand = False
        hand_dice = roll_dice(5)
        while not new_hand:
            new_hand, to_keep = keep_or_score(hand_dice, game_info)
            game_info['roll'] +=1
            hand_dice = to_keep + roll_dice(5-len(to_keep))
        print game_info['scorecard'].print_card()
        disp_dice([a.number for a in  hand_dice])
        time.sleep(1)
        if card_full(game_info['scorecard']):
            game_info['status']=0
    
    if game_info['to_store'] ==1 and game_info['status'] == 0:
        store_results(game_info, storefile)