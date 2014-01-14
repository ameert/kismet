import sys
import os


def exit():
    """Ends the game when called"""
    print "Exiting the game now."
    sys.exit()
    return

def welcome():
    print """
___________________________
   KISMET: "It is Fate"
___________________________
Enter your choice:
1) New Game
2) Exit
"""
    while (1):
        try:
            choice = int(raw_input("Enter your choice:"))
        except:
            choice = -1
        if choice == 1:
            start_game()
        elif choice == 2:
            exit()
                
        #except:
        #    pass

def start_game():
    """This function runs the game"""
    print "hello govnar"




    return
