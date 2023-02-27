# File for a user-run Wordle
import numpy as np
import re, inits, sys
from wordfreq import word_frequency

# frequency arrays of letters
char_arr = np.array([5012.0, 1346.0, 1551.0, 2060.0, 5429.0, 885.0, 1334.0, 1371.0, 3088.0, 264.0, 1295.0, 2652.0, 1660.0, 2377.0, 3684.0, 1652.0, 83.0, 3260.0, 5997.0, 2566.0, 2045.0, 541.0, 844.0, 251.0, 1649.0, 394.0])
char_score_arr = char_arr/np.sum(char_arr)

def validate_guess(guess):
    """Function that takes in a guess and returns its regex and converted hint list.
    
    Input: guess
    Output: hint list, regex"""
    
    # ask user for hint list
    res = list(map(int, list(input("Guess result: "))))
    
    # convert to regex
    out_s = ""
    for ind, i in enumerate(res):
        if i == 0: out_s += "."
        elif i == 1: out_s += guess[ind]
        else: out_s += f"[^{guess[ind]}]"
    
    # print(res, out_s)
    return np.array(res), out_s

def check_letters(guess, mins, maxs):
    """Function that ensures a candidate's letters are bound by their
    known maximums and minimums. (Accounts for repeated letters)
    
    Input: guess, array of minimums for letters, array of maximums for letters
    Output: True if guess is valid, False if not"""
    np_guess = np.array(list(guess))
    res = [np.sum(np_guess == a) >= mins[ord(a)-ord('a')] and np.sum(np_guess == a) <= maxs[ord(a)-ord('a')] \
         for a in guess]
    
    return all(res)

def play_game(word_arr, win_arr, guess="soare"):
    """Function to help with playing a game of Wordle.
    
    Input: array of accepted guess words, array of accepted win words, initial guess
    Output: none"""
    turn = 1
    solved = False
    max_count = np.repeat(5, 26) # initialize each letter to maximum of 5
    
    # main loop
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
        # compute new minimums (cumulative)
        min_count = np.zeros(26)
        for i, char in enumerate(cor_array):
            if char > 0:
                min_count[ord(guess[i])-ord('a')] += 1

        in_list = np.array(list(guess))[np.where(cor_array == 2)]
        not_list = np.array(list(guess))[np.where(cor_array == 0)]

        # set new maximums if applicable
        for char in np.array(list(guess))[(np.where((cor_array == 2) | (cor_array == 1)))]:
            if char in not_list:
                max_count[ord(char)-ord('a')] = np.sum(np.array(list(guess))[(np.where((cor_array == 2) | (cor_array == 1)))] == char)
        
        # adjust not_list for repeated letters
        not_list = np.array(list(set(not_list) - set(np.array(list(guess))[(np.where((cor_array == 1) | (cor_array == 2)))])))
        
        # prune words further / done doubly for case of 0 matched letters (to be altered)
        win_arr = win_arr[[not any(np.isin(not_list, list(a))) \
                            and all(np.isin(in_list, list(a))) for a in win_arr]]

        win_arr = win_arr[[check_letters(a, min_count, max_count) is True for a in win_arr]]

        word_arr = word_arr[[not any(np.isin(not_list, list(a))) \
                            and all(np.isin(in_list, list(a))) for a in word_arr]]

        word_arr = word_arr[[check_letters(a, min_count, max_count) is True for a in word_arr]]
        
        
        #print(not_list, in_list)

        # find best word to guess
        if np.sum(cor_array) == 0:
            # if no matched letters, choose next most common word
            word_scores = inits.find_best(word_arr, char_score_arr)
            guess = word_arr[np.argmax(word_scores)]
        else:
            # otherwise, revise guess by choosing most common English word out of available
            try:
                guess = win_arr[np.argmax([word_frequency(a, 'en', wordlist='large') for a in win_arr])]
            except ValueError:
                print("Sorry. This word isn't in my word list yet.")
                solved = True
                break
        turn += 1
    
    return None

if __name__ == "__main__":
    guess = "soare"
    if len(sys.argv) > 1: guess = sys.argv[1].lower()

    with open("wordle-allowed-guesses.txt", 'r') as file1:
        with open("wordle-answers-alphabetical.txt", 'r') as file2:
            wins = file2.read()
            play_game(sorted((file1.read() + "\n" + wins).split("\n")),
                      wins.split("\n"),
                      guess=guess)