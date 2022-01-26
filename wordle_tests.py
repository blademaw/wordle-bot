import numpy as np
import wordle

wordlist, winlist = [], []
history_wins = []
with open("wordle-allowed-guesses.txt", 'r') as file:
    wordlist = file.read().split("\n")
with open("sgb-words.txt", 'r') as file1:
    winlist = file1.read().split("\n")
with open("wordle-answers-alphabetical.txt", 'r') as file2:
    history_wins = file2.read().split("\n")

def run_tests(test_list):
    count = 0
    final = len(test_list)
    turn_arr = np.zeros(20)
    fails = 0
    fail_arr = []
    for word in test_list:
        turns = wordle.play_game(word, winlist, winlist)
        if turns == -1:
            fails += 1
            fail_arr += [word]
        else:
            turn_arr[turns] += 1
        count += 1

        if count/final % (1/4) == 0:
            print("+ 1/4 progress")
    
    return turn_arr, fails, fail_arr, np.sum([ind*a for ind, a in enumerate(turn_arr)])/np.sum(turn_arr), \
        np.sum(turn_arr[:7])/np.sum(turn_arr), np.sum(turn_arr), np.max(np.argwhere(turn_arr > 0))

turn_arr, fails, fail_arr, avg_turn, winrate, total, maxturn = run_tests(history_wins)

print(f"\nWin%:\t{winrate*100}\nFails:\t{fails}\t{fail_arr}\nTotal:\t{int(total)}\nAvg:\t{np.round(avg_turn, 4)}\nMax:\t{maxturn}")