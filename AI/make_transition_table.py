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

dice_combos = []
for a in range(1,7):
    for b in range(1,7):
        if b>=a:
            for c in range(1,7):
                if c>=b:
                    for d in range(1,7):
                        if d>=c:
                            for e in range(1,7):
                                if e>=d:
                                    dice_combos.append([a,b,c,d,e])

print dice_combos
print len(dice_combos)
