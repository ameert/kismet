from kismet_scorecard import *
import random as ran
import os
from game_funcs import *

seed_size = 42 # number of random bits to pull from the random number generator
# seed the random number generator
newseed =os.urandom(seed_size)
print newseed 
ran.seed(newseed)


welcome()

