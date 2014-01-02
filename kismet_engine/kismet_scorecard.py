import numpy as np

class row():
    def __init__(self, rownum, rowtext, rowscore, section):
        self.rownum = rownum
        self.rowtext = rowtext
        self.rowscore = rowscore
        self.section = section
        return

class scorecard():
    def __init__(self, name):
        self.player_name = name
        self.scores = {}
        
        scores = [('ones', (1,'ones', 0, 'top')), 
                  ('twos', (2,'twos', 0, 'top')),
                  ('threes', (3,'threes', 0, 'top')), 
                  ('fours', (4,'fours', 0, 'top')),
                  ('fives', (5,'fives', 0, 'top')), 
                  ('sixes', (6,'sixes', 0, 'top')),
                  ('top_bonus',(7,'top bonus',0,'none')), 
                  ('top_total',(8, 'top total', 0,'none')),
                  ('tp_sc',(9,'two pair, same color',0, 'bottom')), 
                  ('three_kind',(10, 'three of a kind', 0, 'bottom')),
                  ('straight',(11,'straight',0, 'bottom')), 
                  ('flush',(12, 'flush', 0, 'bottom')),
                  ('full_house',(13,'full_house',0, 'bottom')), 
                  ('fh_sc',(14, 'full_house, same color', 0, 'bottom')),
                  ('four_kind',(15, 'four of a kind', 0, 'bottom')),
                  ('scar',(16, 'Yarborough', 0, 'bottom')),
                  ('kismet',(17, 'Kismet', 0, 'bottom')),
                  ('bot_total',(18, 'bottom total', 0,'none')),
                  ('all_total',(19, 'Grand Total', 0,'none'))]

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
        new_dict = dict([(a.rownum, (a.rowtext,a.rowscore)) for a in self.scores.values()])
        
        for key in new_dict.keys():
            outstring += "#{0[0]:^28s}|{0[1]:^7d}\n".format(new_dict[key])
            if key in minor_dividers:
                outstring += "-"*37 +'\n'
        
        outstring += "="*37 +'\n'
        print outstring
        return
    
    def update_score(self, hand, score):
        self.scores[hand].rowscore = score
        self.update_tots()
        return


if __name__ == "__main__":
    alan_score = scorecard("Alan")

    print alan_score.player_name
    print alan_score.scores.keys()
    alan_score.print_card()

    alan_score.update_score('ones',10)
    alan_score.print_card()

    alan_score.update_score('tp_sc',10)
    alan_score.print_card()

    
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
