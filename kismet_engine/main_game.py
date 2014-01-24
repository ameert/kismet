from game_funcs import *
import sys

sys.path.append("/home/ameert/git_projects/kismet/kismet_engine'")

storefile = '/home/ameert/git_projects/data/game_records.dat'

while (1):
    choice = welcome()
    if choice == 1:
        game_info = start_game()
        game_info = run_game(game_info)
        if game_info['to_store'] ==1 and game_info['status'] == 0:
            store_results(game_info, storefile)
        end_game(game_info)
    elif choice == 2:
        exit_game()
   
