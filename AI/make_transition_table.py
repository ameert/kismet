#++++++++++++++++++++++++++
#
# TITLE: make_transition_table.py
#
# PURPOSE: build the transition tables
#          for probability calculations
#          made by the program
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE:7 FEB 2014
#
#-----------------------------------
import numpy as np
from scipy.misc import factorial as factorial
import sys

sys.path.append('../kismet_engine/')

from config import *
from kismet_scorecard import *

scorecard = scorecard('test')

def get_prob(a, b):
    """Returns the probability of starting with dice combination a 
    and ending a roll with dice combination b"""

    indice = a[:]
    outdice = b[:]

    dice_sides = 6 # the number of sides on the dice
    dice_nums = [1,2,3,4,5,6]
    free_dice = 0 # the number representing a dice that will be rolled this turn
    num_free = 0

    pos=0
    while pos < len(indice):
        if indice[pos] ==free_dice:
            num_free+=1
            indice=np.delete(indice,pos)
        else:
            pos +=1
        
    match = []

    pos = 0
    while pos<len(indice):
        outpos = 0
        while outpos < len(outdice) and len(indice)>0 and pos < len(indice):
            if indice[pos] ==outdice[outpos]:
                match.append(indice[pos])
                indice=np.delete(indice,pos)
                outdice=np.delete(outdice,outpos)
                outpos=0
            else:
                outpos +=1
        pos +=1

    
    if num_free<len(outdice):
        prob=0
    else:
        bincounts, bins = np.histogram(outdice,bins = np.arange(0.5, 6.51, 1.0))
        bincounts=bincounts.astype(int)
        prob=(factorial(len(outdice))/np.prod(factorial(bincounts)))/(dice_sides**len(outdice))
        

    return prob

dice_combos = []
for a in range(0,7):
    for b in range(0,7):
        if b>=a:
            for c in range(0,7):
                if c>=b:
                    for d in range(0,7):
                        if d>=c:
                            for e in range(0,7):
                                if e>=d:# if 0 in [a,b,c,d,e]:
                                    dice_combos.append([a,b,c,d,e])

dice_combos = np.array(dice_combos)

transition_matrix = np.zeros((dice_combos.shape[0], dice_combos.shape[0]))-1

for row,a in enumerate(dice_combos):
    for col, b in enumerate(dice_combos):
        if 0 in b:
            transition_matrix[row,col] = 0.0
        else:
            transition_matrix[row,col] = get_prob(a,b)

print transition_matrix.shape        
print transition_matrix[0:5,0:5]
print transition_matrix[:35,350:]

print len(np.where(transition_matrix>0)[0])
print np.sum(transition_matrix, axis =1)

class score_array():
    def __init__(self):
        self.hands = ['ones','twos','threes','fours','fives','sixes',
                      'tp_sc','three_kind','straight','flush','full_house',
                      'fh_sc','four_kind','scar','kismet']
        
        self.roll1_score = np.zeros((dice_combos.shape[0],len(self.hands)))
        self.roll23_score = np.zeros((dice_combos.shape[0],len(self.hands)))


        for col, handname in enumerate(self.hands):
            for row, outhand in enumerate(dice_combos):
                if 0 in outhand:
                    self.roll1_score[row,col] = 0.0
                    self.roll23_score[row,col] = 0.0
                else:
                    outhand_d = [ dice_set[a-1] for a in outhand]
                    self.roll1_score[row,col] = hand_score[handname](outhand_d,{'roll':1})
                    self.roll23_score[row,col] = hand_score[handname](outhand_d,{'roll':2})


    def update_open_scores(self, scorecard):
        self.open_scores = [0 if scorecard.scores[hand].isscored else 1 for hand in self.hands]
        print self.open_scores
        return self.open_scores


test_score = score_array()

print test_score.roll1_score.shape
print test_score.roll23_score.shape
print test_score.roll1_score
print test_score.roll23_score
print test_score.roll1_score[:,:6]
print test_score.roll23_score[:,:6]
test_score.update_open_scores(scorecard)

