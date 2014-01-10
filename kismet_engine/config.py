########################
#
# the dice and hand info
#
########################

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
    count = np.sum(np.where(numbers==value,1,0))
    return count

def count_ones(hand):
    return 1*count_dice(hand, 1)
def count_twos(hand):
    return 2*count_dice(hand, 2)
def count_threes(hand):
    return 3*count_dice(hand, 3)
def count_fours(hand):
    return 4*count_dice(hand, 4)
def count_fives(hand):
    return 5*count_dice(hand, 5)
def count_sixes(hand):
    return 6*count_dice(hand, 6)

def straight(hand):
    numbers = [a.number for a in hand]
    numbers.sort()
    if numbers == [1,2,3,4,5]:
        score = 30
    elif numbers == [2,3,4,5,6]:
        score = 30
    else:
        score = 0
    return score

def three_kind(hand):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    for a in counts:
        if count >=3:
            score += np.sum(numbers)
    return score

def four_kind(hand):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    for a in counts:
        if count >=4:
            score += np.sum(numbers)+25
    return score

def kismet(hand):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    for a in counts:
        if count ==5:
            score += np.sum(numbers) +50
    return score

def full_house(hand):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    if 3 in counts:
        if 2 in counts:
            score += np.sum(numbers) +15
    return score

def fh_sc(hand):
    score = 0
    numbers = np.array([a.number for a in hand])
    counts = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
    if 3 in counts:
        if 2 in counts:
            if flush(hand)==35:
                score += np.sum(numbers) +20
    return score

def flush(hand):
    colors = [a.color for a in hand]
    col_count = {'black':0,'green':0,'red':0}
    for color in colors:
        col_count[color]+=1
    if 5 in col_count.values():
        score = 35
    else:
        score = 0
    return score

def tp_sc(hand):
    score = 0
    colors = [a.color for a in hand]
    col_count = {'black':0,'green':0,'red':0}
    for color in colors:
        col_count[color]+=1
    if (4 in col_count.values()) or (5 in col_count.values()):
        numbers = np.array([a.number for a in hand])
        counts = np.histogram(numbers, bins = np.arange(-0.5, 6.51,1.0))
        if np.sum(np.where(counts>=2,counts, 0))>=4:
            score += np.sum(numbers)
    return score
        
def top_bonus(scorecard):
    top_score = 0
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

def Yarborough(hand):
    score = np.sum(np.array([a.number for a in hand]))
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
