import sys
import numpy as np
from scipy.misc import factorial as factorial

sys.path.append('../kismet_engine/')

from config import *
from kismet_scorecard import *
from make_transition_table import get_prob

hold_hands = ['ones','twos','threes','fours','fives','sixes',
              'tp_sc','three_kind','straight','flush','full_house',
              'fh_sc','four_kind','scar','kismet']
tmp_scorecard = scorecard('tmp')
hold_hand_rowvals = [tmp_scorecard.scores[a].rownum for a in hold_hands]
del tmp_scorecard

transition_info = np.load('../AI/transition_info.npz')
#contains [dice_combos, transition_matrix]

dice_combos = transition_info['dice_combos']
transition_matrix = transition_info['transition_matrix']

class score_array():
    def __init__(self):
        self.hands = hold_hands
        self.hand_rowvals = hold_hand_rowvals
        
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

        average_top_score = np.array(self.score_adjust)*3.*np.arange(1,self.score_adjust.shape[1]+1) # 3 of each dice
        
        if top_score<63:
            a = (self.bonus_adjust-average_top_score)/(63.-top_score)
            a = np.where(a>1., 1., a)
        else:
            a = 0*self.bonus_adjust
        if top_score<71:
            b = (self.bonus_adjust-average_top_score)/(71.-top_score)
            b = np.where(b>1., 1., a)
        else:
            b = 0*self.bonus_adjust
        if top_score<78:
            c = (self.bonus_adjust-average_top_score)/(78.-top_score)
            c = np.where(c>1., 1., a)
        else:
            c = 0*self.bonus_adjust
       
        self.bonus_adjust = (a*35 + b*(55-35) +c*(75-55))

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

    out_dice = hand_dice
    hand = [a.number for a in hand_dice]
            
    if len(options.keys())>1:
        curr_hand_choice = np.where(choice_hands(hand, 3)==1)[0] #use roll 3 to check current hand
        print curr_hand_choice, ' currchoice'

        if rollnum == 1:
            tmp_score = test_score.roll1_score+test_score.bonus_adjust
        else:
            tmp_score = test_score.roll23_score+test_score.bonus_adjust
        curr_scores = (np.array(tmp_score[curr_hand_choice,:])*np.array(test_score.open_scores))[0,:]

        print curr_scores
        stop_choice = np.argsort(curr_scores)[-1]
        stop_score = curr_scores[stop_choice]
        choice =  test_score.hand_rowvals[stop_choice]
        print 'present ',stop_choice, stop_score, choice

        if 999 in options.keys():
            choice_arr =choice_hands(hand, rollnum) 
            curr_trans_arr = (choice_arr*transition_matrix.T).T
            future_all_score = np.array(curr_trans_arr*test_score.roll23_score)*np.array(test_score.open_scores)
            future_score = np.sum(future_all_score, axis =1)
            future_choice = np.where(future_score == np.max(future_score))[0]
            future_score = np.max(future_all_score[future_choice])
            future_all_score[future_choice]
            print 'future ',future_choice, future_score

            if future_score>stop_score:
                out_dice = []
                choice = 999
                best_hand = np.array(dice_combos[future_choice]).flatten()
                hand_dice_copy = [a for a in hand_dice]
                print 'best_hand ',best_hand
                for a in best_hand:
                    for count, b in enumerate(hand_dice_copy):
                        if a == b.number:
                            out_dice.append(hand_dice_copy.pop(count))
                            break

    else: # if there is only one choice
        choice = options.keys()[0]

    if choice not in options.keys():
        print "bad choice, %d\nchoosing %d instead" %(choice, options.keys()[0])
        choice = options.keys()[0]
    return choice, out_dice


