# File to test wordle-bot

import numpy as np
import wordle
from tqdm import tqdm

wordList, winList = [], []
history_wins = []

with open("wordle-allowed-guesses.txt", 'r') as file:
    wordList = file.read().split("\n")
with open("sgb-words.txt", 'r') as file1:
    winList = file1.read().split("\n")
with open("wordle-answers-alphabetical.txt", 'r') as file2:
    history_wins = file2.read().split("\n")

def run_tests(testList, wordList, winList):
    """ Test wordle-bot.

    Input: array of words to test on, array of words to guess from, array of words accepted by Wordle.
    Output: array where ith position is number of games that took i turns, number of fails, words failed on,
            average game length, total win rate, total games played, length of longest game played

    """

    count = fails = 0
    turn_arr = np.zeros(20)
    fail_arr = []

    # for each word, play game
    for word in tqdm(testList):
        turns = wordle.play_game(word, wordList, winList)
        if turns == -1:
            fails += 1
            fail_arr += [word]
        else:
            turn_arr[turns] += 1
        count += 1
    
    return (turn_arr,
            fails,
            fail_arr,
            np.sum([ind*a for ind, a in enumerate(turn_arr)])/np.sum(turn_arr),
            np.sum(turn_arr[:7])/np.sum(turn_arr), 
            np.sum(turn_arr), 
            np.max(np.argwhere(turn_arr > 0)))

 
turn_arr, fails, fail_arr, avg_turn, winrate, total, maxturn = run_tests(history_wins, history_wins, history_wins)
print(f"\nWin%:\t{winrate*100}\nFails:\t{fails}\t{fail_arr}\nTotal:\t{int(total)}\nAvg:\t{np.round(avg_turn, 4)}\nMax:\t{maxturn}")