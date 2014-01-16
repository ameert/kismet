import sys
import os
from kismet_scorecard import *
import random as ran
from config import *

def exit_game():
    """Ends the game when called"""
    print "Exiting the game now."
    sys.exit()
    return

def welcome():
    print """
___________________________
   KISMET: "It is Fate"
___________________________
Enter your choice:
1) New Game
2) Exit
"""
    while (1):
        try:
            choice = int(raw_input("Enter your choice:"))
        except:
            choice = -1
        if choice in [1,2]:
            break

    return choice

def start_game():
    """This function sets up game info dictionary"""
    print "hello govnar"
    name = 99
    to_store = -1
    while name==99:
        try:
            name = str(raw_input("What's your name? (Enter it now):"))
        except:
            print "improper name! try again!"
            name = 99
    while to_store == -1:
        try:
            to_store = int(raw_input("Store results?\n 1 for yes, 2 for no:"))
        except:
            to_store = -1
        if to_store not in [1,2]:
            print "improper entry! try again!"
            to_store = -1

    game_info = {
        'scorecard':scorecard(name),
        'seed':get_seed(),
        'status':-1,
        'to_store':to_store
        }

    return game_info

def get_seed():
    """Pulls a seed value for the ranom number generator from the os"""
    seed_size = 42 # number of random bits to pull 
    newseed =os.urandom(seed_size)
    return newseed

def roll_dice(num_to_roll):
    """returns a specified number of dice, up to 5"""
    new_dice = []
    while len(new_dice)<min([num_to_roll,5]):
        new_dice.append(ran.choice(dice_set))
    return new_dice

def run_game(game_info):
    """runs the game"""
    ran.seed(game_info['seed'])
    
    while game_info['status']<0:
        raw_input("Hit enter to roll dice...")
        roll=1
        new_hand = False
        hand_dice = roll_dice(5)
        while not new_hand:
            disp_dice([a.number for a in  hand_dice])
            new_hand, to_keep = keep_or_score(hand_dice, roll, game_info)
            roll +=1
            hand_dice = to_keep + roll_dice(5-len(to_keep))
        print game_info['scorecard'].print_card()
        if card_full(game_info['scorecard']):
            game_info['status']=0
    return game_info

def keep_or_score(hand_dice, roll, game_info):
    """decides what the payer must do given the turn state of the game"""
    return True, hand_dice

def card_full(player_card):
    """determines if a players card if full"""
    full = True
    for row in player_card.scores.values():
        if full and not row.isscored:
            full = False
    return full

def store_results(game_info, storefile):
    """writes the game info to a file for later analysis"""
    outfile = open(storefile, 'a')
    outfile.write(str(game_info)+'\n')
    outfile.close()
    return

def end_game(game_info):
    """prints end of game info and scorecard"""
    print game_info['scorecard'].print_card()
    print "game seed:", game_info['seed']
    print "game over!!!"
    return
