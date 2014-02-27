import sys
import os
import random as ran
import copy
from config import *
from kismet_scorecard import *
import time
try:
    from simulate_game import  AI_keep_or_score
except ImportError:
    print "cannot import AI!!!!"

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

    game_info = {'seed':get_seed(),'to_store':to_store,'status':-1,
                 'player_names':[name,],
                 name:{
            'scorecard':scorecard(name),
            'computer_player':False}
                 }

    while 1:
        try:
            with_computer = raw_input("Play against the computer?(yes or no):")
        except:
            with_computer = -1
        if with_computer =='yes':
            with_computer = True
            break
        elif with_computer == 'no':
            with_computer = False
            break
        else:
            print "improper entry! Please enter 'yes' or 'no'. Try again!"
        
    if with_computer:
        game_info['Computer'] = {
        'scorecard':scorecard('Computer'),
        'computer_player':True}
        game_info['player_names'].append('Computer')
    
    print_cards_all(game_info)
    return game_info

def print_cards_all(game_info):
    cards = []
    for key in game_info['player_names']:
        cards.append(game_info[key]['scorecard'].print_card())
    cards = [a.split('\n') for a in cards]
    for line in zip(*cards):
        print "{line1:<50s}{line2:<50s}".format(line1=line[0], line2=line[1])
    return 

def get_seed():
    """Pulls a seed value for the ranom number generator from the os"""
    max_seed = 2**50 # number of random bits to pull 
    newseed =ran.SystemRandom().randint(0,max_seed)
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
        for name in game_info['player_names']:
            print_cards_all(game_info)
            if not game_info[name]['computer_player']:
                raw_input("Hit enter to roll dice...")
            game_info[name]['roll']=1
            new_hand = False
            hand_dice = roll_dice(5)
            while not new_hand:
                if not game_info[name]['computer_player']:
                    new_hand, to_keep = keep_or_score(hand_dice, game_info[name])
                else:
                    disp_dice([a.number for a in  hand_dice])
                    new_hand, to_keep = AI_keep_or_score(hand_dice, game_info[name])                   
                    time.sleep(1)
                game_info[name]['roll'] +=1
                hand_dice = to_keep + roll_dice(5-len(to_keep))            
        card_check = np.array([1 if card_full(game_info[name]['scorecard']) else 0 for name in game_info['player_names']])
        if np.sum(card_check) == len(game_info['player_names']):
            game_info['status']=0
    return game_info

def keep_or_score(hand_dice, game_info):
    """decides what the player must do given the turn state of the game"""
    options = score_repor(hand_dice, game_info)
    if game_info['roll']<3:
        options.append((999,'cont_roll','choose dice and continue rolling', -1))
    options.append((888,'print_card','print your score card', -1))
    options = dict([[a[0], a[1:]] for a in options])
    OK = False
    while not OK:
        choice = -1
        while choice not in options.keys():
            disp_dice([a.number for a in  hand_dice])
            print_options(options)
            print "What is your choice?"
            try:
                choice = int(raw_input("Enter it now:"))
            except:
                choice = -1
            if choice not in options.keys():
                print "Choice not recognized! Try again"
            if choice == 888:
                print game_info['scorecard'].print_card()
                raw_input("Hit enter to continue")
                choice = -1

        if choice == 999:
            new_hand=False
            hand_dice, OK = choose_keepdie(hand_dice)
            if not OK:
                choice = -1
        else:
            OK=True
            new_hand = True
            game_info['scorecard'].update_score(options[choice][0],options[choice][2],game_info['roll'],[a.number for a in hand_dice])
    return new_hand, hand_dice

def choose_keepdie(hand_dice):
    letters = ['a','b','c','d','e']
    dice_dict = dict(zip(letters,hand_dice))
    print "Which dice would you like to keep?"
    for let in letters:
        print "%s) number: %d color:%s" %(let, dice_dict[let].number,dice_dict[let].color)
    choice = raw_input("Enter your choices (%s):" %','.join(letters))
    to_keep = []
    for a in choice:
        if a in letters and a not in to_keep:
            to_keep.append(a)
    print "keep these: %s" %','.join(to_keep)
    if raw_input("Enter choice [Y]/n:")=='n':
        OK = False
        to_keep = letters
    else:
        OK = True
    return [dice_dict[key] for key in to_keep], OK
            

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
    for name in new_game_info['player_names']:
        new_game_info[name]['scorecard'] = game_info[name]['scorecard'].print_card(full_info=True)
    outfile.write(str(new_game_info)+'\n')
    outfile.close()
    return

def end_game(game_info):
    """prints end of game info and scorecard"""
    print_cards_all(game_info)
    print "game seed:", game_info['seed']
    print "game over!!!"
    return

