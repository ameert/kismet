import numpy as np
from config import *

class ScoreError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class row():
    def __init__(self, rownum, rowtext, rowscore, section, isscored):
        self.rownum = rownum
        self.rowtext = rowtext
        self.rowscore = rowscore
        self.section = section
        self.isscored = isscored
        return

    def score_row(self, score):
        if not self.isscored:
            self.rowscore = score 
            self.isscored = True
        else:
            raise ScoreError("Row Already Scored!!!")    
        return

class scorecard():
    def __init__(self, name):
        self.player_name = name
        self.scores = {}
        
        scores = [('ones', (1,'ones', 0, 'top',False)), 
                  ('twos', (2,'twos', 0, 'top',False)),
                  ('threes', (3,'threes', 0, 'top',False)), 
                  ('fours', (4,'fours', 0, 'top',False)),
                  ('fives', (5,'fives', 0, 'top',False)), 
                  ('sixes', (6,'sixes', 0, 'top',False)),
                  ('top_bonus',(7,'top bonus',0,'none',True)), 
                  ('top_total',(8, 'top total', 0,'none',True)),
                  ('tp_sc',(9,'two pair, same color',0, 'bottom',False)), 
                  ('three_kind',(10, 'three of a kind', 0, 'bottom',False)),
                  ('straight',(11,'straight',0, 'bottom',False)), 
                  ('flush',(12, 'flush', 0, 'bottom',False)),
                  ('full_house',(13,'full house',0, 'bottom',False)), 
                  ('fh_sc',(14, 'full house, same color', 0, 'bottom',False)),
                  ('four_kind',(15, 'four of a kind', 0, 'bottom',False)),
                  ('scar',(16, 'Yarborough', 0, 'bottom',False)),
                  ('kismet',(17, 'Kismet', 0, 'bottom',False)),
                  ('bot_total',(18, 'bottom total', 0,'none',True)),
                  ('all_total',(19, 'Grand Total', 0,'none',True))]

        for a in scores:
            self.scores[a[0]]=row(*a[1])

        return

    def update_tots(self):
        new_top = 0
        new_bottom = 0
        for a in self.scores.values():
            if a.section=='top':
                new_top += a.rowscore
            elif a.section == 'bottom':
                new_bottom += a.rowscore

        self.scores['top_total'].rowscore = new_top
        self.scores['bot_total'].rowscore = new_bottom
        self.scores['all_total'].rowscore = new_bottom+new_top
        
        return

    def print_card(self):
        minor_dividers = [6,8,17]
        outstring = """
#####################################
# KISMET SCORECARD
# Player Name: {name}
#####################################      
#           Hand             | Score    
#####################################
""".format(name = self.player_name)
        new_dict = dict([(a.rownum, (a.rowtext,a.rowscore,a.isscored)) for a in self.scores.values()])
        
        for key in new_dict.keys():
            if new_dict[key][2]:
                outstring += "#{0[0]:^28s}|{0[1]:^7d}\n".format(new_dict[key])
            else:
                outstring += "#{0[0]:^28s}|  ---  \n".format(new_dict[key])
            if key in minor_dividers:
                outstring += "-"*37 +'\n'
        
        outstring += "="*37 +'\n'
        return outstring
    
    def update_score(self, hand, score):
        try:
            self.scores[hand].score_row(score)
            self.update_tots()
            isgood = True
        except ScoreError as e:
            print e.value
            isgood = False
        return isgood

    def dump_card(self, filename):
        outfile = open(filename, 'a')
        outfile.write(self.print_card())
        outfile.close()
        return

diceart = """ 
 _________     _________     _________     _________     _________
/         \   /         \   /         \   /         \   /         \     
|  {0[0]}   {0[1]}  |   |  {1[0]}   {1[1]}  |   |  {2[0]}   {2[1]}  |   |  {3[0]}   {3[1]}  |   |  {4[0]}   {4[1]}  |
|  {0[2]} {0[3]} {0[4]}  |   |  {1[2]} {1[3]} {1[4]}  |   |  {2[2]} {2[3]} {2[4]}  |   |  {3[2]} {3[3]} {3[4]}  |   |  {4[2]} {4[3]} {4[4]}  |
|  {0[5]}   {0[6]}  |   |  {1[5]}   {1[6]}  |   |  {2[5]}   {2[6]}  |   |  {3[5]}   {3[6]}  |   |  {4[5]}   {4[6]}  | 
\_________/   \_________/   \_________/   \_________/   \_________/
"""

dice_dots = {1:[' ',' ',' ','O',' ',' ',' '], 2:['O',' ',' ',' ',' ',' ','O'],
             3:['O',' ',' ','O',' ',' ','O'], 4:['O','O',' ',' ',' ','O','O'],
             5:['O','O',' ','O',' ','O','O'], 6:['O','O','O',' ','O','O','O'] }

def disp_dice(dice_vals):
    print diceart.format(*[dice_dots[a] for a in dice_vals])
    print "Dice values: %s" %(str(dice_vals))
    return

if __name__ == "__main__":
    from game_funcs import *
    alan_score = scorecard("Alan")

    print alan_score.player_name
    print alan_score.scores.keys()
    print alan_score.print_card()

    alan_score.update_score('ones',10)
    print alan_score.print_card()

    alan_score.update_score('tp_sc',10)
    print alan_score.print_card()

    alan_score.update_score('tp_sc', 50)
    disp_dice([1,5,3,5,5])

    
    game_info = {
        'scorecard':scorecard('Alan'),
        'seed':get_seed(),
        'status':-1,
        'to_store':True,
        'roll':1
        }

    hand_dice = roll_dice(5)
    disp_dice([a.number for a in  hand_dice])
    options = score_repor(hand_dice, game_info)
    if game_info['roll']<3:
        options.append((999,'cont_roll','choose dice and continue rolling', -1))
    options = dict([[a[0], a[1:]] for a in options])
    print_options(options)
