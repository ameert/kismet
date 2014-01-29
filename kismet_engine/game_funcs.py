import sys
import os
import random as ran
import copy
from config import *
from kismet_scorecard import *


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
    print "Hello!"
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

    print game_info['scorecard'].print_card()
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
        game_info['roll']=1
        new_hand = False
        hand_dice = roll_dice(5)
        while not new_hand:
            disp_dice([a.number for a in  hand_dice])
            new_hand, to_keep = keep_or_score(hand_dice, game_info)
            game_info['roll'] +=1
            hand_dice = to_keep + roll_dice(5-len(to_keep))
        print game_info['scorecard'].print_card()
        if card_full(game_info['scorecard']):
            game_info['status']=0
    return game_info

def keep_or_score(hand_dice, game_info):
    """decides what the player must do given the turn state of the game"""
    options = score_repor(hand_dice, game_info)
    if game_info['roll']<3:
        options.append((999,'cont_roll','choose dice and continue rolling', -1))
    options = dict([[a[0], a[1:]] for a in options])
    print_options(options)
    choice = -1
    while choice not in options.keys():
        print "What is your choice?"
        try:
            choice = int(raw_input("Enter it now:"))
        except:
            choice = -1
        if choice not in options.keys():
            print "Choice not recognized! Try again"

    if choice == 999:
        new_hand=False
        hand_dice = choose_keepdie(hand_dice)
    else:
        new_hand = True
        game_info['scorecard'].update_score(options[choice][0],options[choice][2],game_info['roll'],[a.number for a in hand_dice])
    return new_hand, hand_dice

def choose_keepdie(hand_dice):
    letters = ['a','b','c','d','e']
    dice_dict = dict(zip(letters,hand_dice))
    print "Which dice would you like to keep?"
    for let in letters:
        print "%s) number: %d color:%s" %(let, dice_dict[let].number,dice_dict[let].color)
    while (1):
        choice = raw_input("Enter your choices (%s):" %','.join(letters))
        to_keep = []
        for a in choice:
            if a in letters:
                to_keep.append(a)
        print "keep these: %s" %','.join(to_keep)
        good = True
        if raw_input("Enter choice [Y]/n:")=='n':
                good = False
        if good:
            break
    return [dice_dict[key] for key in to_keep]
            

def print_options(options):
    print "options:"
    for key in sorted(options.keys()):
        if options[key][2]>=0:
            print "%d: Score %d points in %s" %(key,options[key][2],options[key][1])
        else:
            print "%d: %s" %(key,options[key][1])
    return

def score_repor(hand_dice, game_info):
    options = []
    new_dict = dict([(a.rownum, (b,a.rowtext,a.rowscore, a.isscored)) for (b,a) in game_info['scorecard'].scores.items()])
    first_zero = []
    for key in new_dict.keys():
        if not new_dict[key][3]:
            score = hand_score[new_dict[key][0]](hand_dice, game_info)
            if score >0:
                options.append((key,new_dict[key][0],new_dict[key][1],score))
            elif len(first_zero)==0:
                first_zero.append((key,new_dict[key][0],new_dict[key][1],score))
    if len(options)==0:
        options.append(first_zero[0])
    return options

def card_full(player_card):
    """determines if a players card if full"""
    full = True
    for row in player_card.scores.values():
        if full and not row.isscored:
            full = False
    return full

def store_results(game_info, storefile):
    """writes the game info to a file for later analysis"""
    outfile = open(storefile, 'ab')
    new_game_info = copy.deepcopy(game_info)
    new_game_info['scorecard'] = game_info['scorecard'].print_card(full_info=True)
    outfile.write(str(new_game_info)+'\n')
    outfile.close()
    return

def end_game(game_info):
    """prints end of game info and scorecard"""
    print game_info['scorecard'].print_card()
    print "game seed:", game_info['seed']
    print "game over!!!"
    return
