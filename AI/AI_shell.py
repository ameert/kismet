import sys
import numpy as np
from scipy.misc import factorial as factorial

sys.path.append('../kismet_engine/')

from config import *
from kismet_scorecard import *
from make_transition_table import get_prob


transition_info = np.load('../AI/transition_info.npz')
#contains [dice_combos, transition_matrix]

dice_combos = transition_info['dice_combos']
transition_matrix = transition_info['transition_matrix']

class score_array():
    def __init__(self):
        self.hands = ['ones','twos','threes','fours','fives','sixes',
                      'tp_sc','three_kind','straight','flush','full_house',
                      'fh_sc','four_kind','scar','kismet']
        
        self.roll1_score = np.matrix(np.zeros((dice_combos.shape[0],len(self.hands))))
        self.roll23_score = np.matrix(np.zeros((dice_combos.shape[0],len(self.hands))))

        self.score_adjust = np.matrix(np.zeros((dice_combos.shape[0],len(self.hands))))
        
        for col, handname in enumerate(self.hands):
            for row, outhand in enumerate(dice_combos):
                if 0 in outhand:
                    self.roll1_score[row,col] = 0.0
                    self.roll23_score[row,col] = 0.0
                else:
                    outhand_d = [ dice_set[a-1] for a in outhand]
                    self.roll1_score[row,col] = hand_score[handname](outhand_d,{'roll':1})
                    self.roll23_score[row,col] = hand_score[handname](outhand_d,{'roll':2})
                    if handname in ['ones','twos','threes','fours','fives','sixes']:
                        self.score_adjust[row,col] =1 
                        
        

    def update_open_scores(self, scorecard, rollnum):
        self.open_scores = [0 if scorecard.scores[hand].isscored else 1 for hand in self.hands]
        if rollnum ==1:
            self.bonus_adjust = np.array(self.roll1_score)*np.array(self.score_adjust)
        else:
            self.bonus_adjust = np.array(self.roll23_score)*np.array(self.score_adjust)
        
        top_score = scorecard.scores['top_total'].rowscore- scorecard.scores['top_bonus'].rowscore
        print self.bonus_adjust[300:,:6]
        print self.roll23_score[300:,:6]
        a = self.bonus_adjust/(63.-top_score)
        a = np.where(a>1., 1., a)
        a = np.where(a<0., 0., a)
        b = self.bonus_adjust/(61.-top_score)
        b = np.where(b>1., 1., a)
        b = np.where(b<0., 0., a)
        c = self.bonus_adjust/(78.-top_score)
        c = np.where(c>1., 1., a)
        c = np.where(c<0., 0., a)

        self.bonus_adjust = a*35 + b*(55-35) +c*(75-55)

        print dice_combos[300:]
        print self.bonus_adjust[300:,:6]
        return self.open_scores, self.bonus_adjust


def choice_hands(hand, roll):
    hand_arr = np.zeros(dice_combos.shape[0])
    for count, row in enumerate(dice_combos):
        if 0 in row:
            if roll == 3:
                continue
        if get_prob(row, hand)>0:
            hand_arr[count] = 1
        
    return hand_arr

def AI_choose_option(options, scorecard, rollnum, hand_dice):
    test_score = score_array()
    test_score.update_open_scores(scorecard, rollnum)

    out_dice = []
    for count in [17,15,14,13,12,11]:
        if count in options.keys():
            if options[count][2]>0:
                choice = count
                out_dice = hand_dice
                break
    else:
        if 999 in options.keys():
            choice = 999
            hand = [a.number for a in hand_dice]
            choice_arr =choice_hands(hand, rollnum) 
            curr_trans_arr = (choice_arr*transition_matrix.T).T
            future_score = np.array(curr_trans_arr*test_score.roll23_score)*np.array(test_score.open_scores)
            future_choice = np.sum(future_score, axis =1)
            best_hand = np.where(future_choice == np.max(future_choice))[0]
            best_hand = np.array(dice_combos[best_hand]).flatten()
            hand_dice_copy = [a for a in hand_dice]
            print 'best_hand ',best_hand
            for a in best_hand:
                for count, b in enumerate(hand_dice_copy):
                    if a == b.number:
                        out_dice.append(hand_dice_copy.pop(count))
                        break
            
        else: 
            best = (-1,-1)
            for a in options.items():
                if a[1][2] > best[1]:
                    best = (a[0], a[1][2])
            choice = best[0]
            out_dice = hand_dice

    return choice, out_dice


