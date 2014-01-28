########################
#
# the dice and hand info
#
########################
import numpy as np

first_roll_multiplier = 2


# modify np.sum to produce ints rather than int64 to
# prevent formatting errors

def alan_sum(vals):
    return int(np.sum(vals))


dice_vals = {'numbers':[1,2,3,4,5,6],
             'colors':['black','red','green','green','red','black']
             }

class dice():
    def __init__(self):
        self.number = -1
        self.color = 'none'
        return

    def set_color(self, color):
        self.color = color
        return

    def set_number(self, number):
        self.number = number
        return

dice_set = []

for a,b in zip(dice_vals['numbers'],dice_vals['colors']):
    new_dice = dice()
    new_dice.color = b
    new_dice.number = a
    dice_set.append(new_dice)

def count_dice(hand, value):
    numbers = np.array([a.number for a in hand])
    count = alan_sum(np.where(numbers==value,1,0))
    return count

def count_ones(hand, game_info):
    val = 1*count_dice(hand, 1)
    if game_info['roll']==1:
        val *= first_roll_multiplier
    return val
def count_twos(hand, game_info):
    val = 2*count_dice(hand, 2)
    if game_info['roll']==1:
        val *= first_roll_multiplier
    return val
def count_threes(hand, game_info):
    val = 3*count_dice(hand, 3)
    if game_info['roll']==1:
        val *= first_roll_multiplier
    return val
def count_fours(hand, game_info):
    val = 4*count_dice(hand, 4)
    if game_info['roll']==1:
        val *= first_roll_multiplier
    return val
def count_fives(hand, game_info):
    val = 5*count_dice(hand, 5)
    if game_info['roll']==1:
        val *= first_roll_multiplier
    return val
def count_sixes(hand, game_info):
    val = 6*count_dice(hand, 6)
    if game_info['roll']==1:
        val *= first_roll_multiplier
    return val

def straight(hand, game_info):
    numbers = [a.number for a in hand]
    numbers.sort()
    if numbers == [1,2,3,4,5]:
        score = 30
    elif numbers == [2,3,4,5,6]:
        score = 30
    else:
        score = 0
    if game_info['roll']==1:
        score *= first_roll_multiplier
    return score

def three_kind(hand, game_info):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts, bins = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    for count in counts:
        if count >=3:
            score += alan_sum(numbers)
    if game_info['roll']==1:
        score *= first_roll_multiplier
    return score

def four_kind(hand, game_info):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts,bins = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    for count in counts:
        if count >=4:
            score += alan_sum(numbers)
    if game_info['roll']==1:
        score *= first_roll_multiplier
    if score>0:
        score+=25
    return score

def kismet(hand, game_info):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts,bins = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    for count in counts:
        if count ==5:
            score += alan_sum(numbers)
    if game_info['roll']==1:
        score *= first_roll_multiplier
    if score>0:
        score+=50
    return score

def full_house(hand, game_info):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts,bins = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    if 3 in counts:
        if 2 in counts:
            score += alan_sum(numbers) 
    if game_info['roll']==1:
        score *= first_roll_multiplier
    if score>0:
        score+=15
    return score 

def fh_sc(hand, game_info):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts,bins = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    if 3 in counts:
        if 2 in counts:
            if flush(hand, game_info)==35:
                score += alan_sum(numbers) 
    if game_info['roll']==1:
        score *= first_roll_multiplier
    if score>0:
        score+=20
    return score
    
def flush(hand, game_info):
    colors = [a.color for a in hand]
    col_count = {'black':0,'green':0,'red':0}
    for color in colors:
        col_count[color]+=1
    if 5 in col_count.values():
        score = 35
    else:
        score = 0
    if game_info['roll']==1:
        score *= first_roll_multiplier
    return score

def tp_sc(hand, game_info):
    score = 0
    colors = [a.color for a in hand]
    col_count = {'black':0,'green':0,'red':0}
    for color in colors:
        col_count[color]+=1
    if (4 in col_count.values()) or (5 in col_count.values()):
        numbers = np.array([a.number for a in hand])
        counts,bins = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
        if alan_sum(np.where(counts>=2,counts, 0))>=4:
            score += alan_sum(numbers)
    if game_info['roll']==1:
        score *= first_roll_multiplier
    return score
        
def top_bonus(top_score):
    if top_score > 62:
        if top_score > 70:
            if top_score > 77:
                score = 75
            else:
                score = 55
        else:
            score = 35
    else:
        score = 0
    return score

def Yarborough(hand, game_info):
    score = alan_sum(np.array([a.number for a in hand]))
    if game_info['roll']==1:
        score *= first_roll_multiplier
    return score
    
        
hand_score = {'ones':count_ones,
              'twos':count_twos,
              'threes':count_threes,
              'fours':count_fours,
              'fives':count_fives,
              'sixes':count_sixes,
              'top_bonus':top_bonus,
              'tp_sc':tp_sc,
              'three_kind':three_kind,
              'straight':straight,
              'flush':flush,
              'full_house':full_house,
              'fh_sc':fh_sc,
              'four_kind':four_kind,
              'scar':Yarborough,
              'kismet':kismet
             }
