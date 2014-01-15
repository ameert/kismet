import sys
import os
from kismet_scorecard import *
import random as ran

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

def run_game(game_info):
    """runs the game"""
    ran.seed(game_info['seed'])
    return game_info

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
