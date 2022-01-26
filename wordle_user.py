# File for a user-run Wordle
from multiprocessing.sharedctypes import Value
import matplotlib.pyplot as plt
import numpy as np
import re
import inits
from wordfreq import word_frequency

char_arr = np.array([5012.0, 1346.0, 1551.0, 2060.0, 5429.0, 885.0, 1334.0, 1371.0, 3088.0, 264.0, 1295.0, 2652.0, 1660.0, 2377.0, 3684.0, 1652.0, 83.0, 3260.0, 5997.0, 2566.0, 2045.0, 541.0, 844.0, 251.0, 1649.0, 394.0])
char_score_arr = char_arr/np.sum(char_arr)

def validate_guess(guess):
    # returns regex to match
    res = list(map(int, list(input("Guess result: "))))
    
    out_s = ""
    for ind, i in enumerate(res):
        if i == 0: out_s += "."
        elif i == 1: out_s += guess[ind]
        else: out_s += f"[^{guess[ind]}]"
    
    print(res, out_s)
    return np.array(res), out_s
        

def play_game(word_arr, win_arr, guess="soare"):
    turn = 1
    solved = False
    
    while not solved:
        print(f"{turn}\tI think\t{guess.upper()} from {len(win_arr)} candidates")
        cor_array, out_s = validate_guess(guess)
        if np.all(cor_array == 1):
            solved = True
            break

        # revise guess
        # 1 - keep only words with letters we know are(n't) in positions
        r = re.compile(out_s)
        win_arr = np.array(list(filter(r.match, win_arr)))
        word_arr = np.array(list(filter(r.match, word_arr)))

        # 2 — axe words with(out) specific characters
        # cand_count = np.zeros(26)
        # for i, char in enumerate(cor_array):
        #     if char > 0: cand_count[ord(guess[i])-ord('a')] += 1

        in_list = np.array(list(guess))[np.where(cor_array == 2)]
        not_list = np.array(list(guess))[np.where(cor_array == 0)]
        not_list = np.array(list(set(not_list) - set(np.array(list(guess))[(np.where((cor_array == 1) | (cor_array == 2)))])))
        win_arr = win_arr[[not any(np.isin(not_list, list(a))) \
                            and all(np.isin(in_list, list(a))) for a in win_arr]]

        word_arr = word_arr[[not any(np.isin(not_list, list(a))) \
                            and all(np.isin(in_list, list(a))) for a in word_arr]]
        
        
        print(not_list, in_list)

        # find best word to guess
        if np.sum(cor_array) == 0:
            # if totally blank, choose next most common word
            word_scores = inits.find_best(word_arr, char_score_arr)
            guess = word_arr[np.argmax(word_scores)]
        else:
            # otherwise, revise guess
            try:
                guess = win_arr[np.argmax([word_frequency(a, 'en', wordlist='large') for a in win_arr])]
            except ValueError:
                print("Sorry. This word isn't in my word list yet.")
                solved = True
                break
        turn += 1
    
    return None

with open("wordle-allowed-guesses.txt", 'r') as file1:
    with open("sgb-words.txt", 'r') as file2:
        wins = file2.read()
        play_game(sorted((file1.read() + "\n" + wins).split("\n")), wins.split("\n"))