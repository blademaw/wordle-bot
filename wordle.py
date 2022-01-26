# File to play around with Wordle
import matplotlib.pyplot as plt
import numpy as np
import re
import inits
from wordfreq import word_frequency

char_arr = np.array([5012.0, 1346.0, 1551.0, 2060.0, 5429.0, 885.0, 1334.0, 1371.0, 3088.0, 264.0, 1295.0, 2652.0, 1660.0, 2377.0, 3684.0, 1652.0, 83.0, 3260.0, 5997.0, 2566.0, 2045.0, 541.0, 844.0, 251.0, 1649.0, 394.0])
char_score_arr = char_arr/np.sum(char_arr)

def validate_guess(word, guess):
    used_arr = np.zeros(26)
    for char in word: used_arr[ord(char)-ord('a')] += 1
    
    res = np.zeros(5)
    out_s = []
    for i, char in enumerate(guess):
        if char not in word:
            res[i] = 0
            out_s += ["_"]
            continue
        elif char == word[i]:
            res[i] = 1
            out_s += [char.upper()]
        elif used_arr[ord(char)-ord('a')] > 0:
            res[i] = 2
            out_s += [char]
        used_arr[ord(char)-ord('a')] -= 1
    
    return res, "".join(out_s)
        

def play_game(word, word_arr, win_arr, guess="soare"):
    turn = 0
    solved = False
    
    while not solved:
        #print(f"{turn}\tI think\t{guess.upper()} from {len(word_arr)} candidates")
        turn += 1
        cor_array, out_s = validate_guess(word, guess)
        #print(f"{turn}\tResult\t{out_s}")
        if np.all(cor_array == 1):
            solved = True
            #print(f"I found the answer in {turn} turns")
            return turn

        # revise guess
        # 1 - keep only words with letters we know are(n't) in positions
        r_str = ""
        for char in out_s.replace("_", "."):
            if char.islower():
                r_str += f"[^{char}]"
            else:
                r_str += char.lower()
        
        r = re.compile(r_str)
        win_arr = np.array(list(filter(r.match, win_arr)))
        word_arr = np.array(list(filter(r.match, word_arr)))

        # 2 — axe words with(out) characters
        in_list = np.array(list(guess))[np.where(cor_array == 2)]
        not_list = np.array(list(guess))[np.where(cor_array == 0)]
        not_list = np.array(list(set(not_list) - set(np.array(list(guess))[(np.where((cor_array == 1) | (cor_array == 2)))])))
        win_arr = win_arr[[not any(np.isin(not_list, list(a))) \
                            and all(np.isin(in_list, list(a))) for a in win_arr]]

        word_arr = word_arr[[not any(np.isin(not_list, list(a))) \
                            and all(np.isin(in_list, list(a))) for a in word_arr]]

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
                #print("Couldn't find the word.")
                return -1
        
    
    return None
