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


dice_combos_out = []
for a in range(1,7):
    for b in range(1,7):
        if b>=a:
            for c in range(1,7):
                if c>=b:
                    for d in range(1,7):
                        if d>=c:
                            for e in range(1,7):
                                if e>=d:
                                    dice_combos_out.append([a,b,c,d,e])

dice_combos_out = np.array(dice_combos_out)

dice_combos_in = []
for a in range(0,7):
    for b in range(0,7):
        if b>=a:
            for c in range(0,7):
                if c>=b:
                    for d in range(0,7):
                        if d>=c:
                            for e in range(0,7):
                                if e>=d:# if 0 in [a,b,c,d,e]:
                                    dice_combos_in.append([a,b,c,d,e])

dice_combos_in = np.array(dice_combos_in)

transition_matrix = np.zeros((dice_combos_in.shape[0], dice_combos_out.shape[0]))-1

for row,a in enumerate(dice_combos_in):
    for col, b in enumerate(dice_combos_out):
        transition_matrix[row,col] = get_prob(a,b)
        
#print transition_matrix[0:5,0:5]
#print transition_matrix[35:40,35:40]

#print len(np.where(transition_matrix>0)[0])
#print np.sum(transition_matrix, axis =1)

class score_array():
    def __init__(self, hand_name):
        self.hand_name = hand_name
        self.roll1_score = [hand_score(a,{'roll':1}) for a in dice_combos_out]
        self.roll23_score = [hand_score(a,{'roll':2}) for a in dice_combos_out]

