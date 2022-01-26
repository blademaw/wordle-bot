import matplotlib.pyplot as plt
import numpy as np

# char_arr = np.array([5011, 1346, 1551, 2060, 5429, 885, 1333, 1371, 3088, 264, 1295, 2652, 1660,\
#                     2377, 3684, 1652, 83, 3259, 5996, 2566, 2044, 541, 844, 251, 1649, 394])
# char_score_arr = char_arr/np.sum(char_arr)

# obtaining frequencies of letters
# with open("wordle-allowed-guesses.txt", 'r') as file:
#     char_arr = np.zeros(26)
#     s = file.read().replace('\n', '')
#     for char in s:
#         char_arr[ord(char)-ord('a')] += 1
    
#     print(list(char_arr))

# with open("wordle-allowed-guesses.txt", 'r') as file:
#     word_arr = file.read().split("\n")

def find_best(arr, char_score_arr, k=.5):
    word_score_arr = np.zeros(len(arr))
    for i, word in enumerate(arr):
        cur_word_list = []
        for char in word:
            if char in cur_word_list:
                word_score_arr[i] += char_score_arr[ord(char)-ord('a')]*k
            else:
                word_score_arr[i] += char_score_arr[ord(char)-ord('a')]
            
            cur_word_list += [char]

    return word_score_arr

# init_words = find_best(word_arr, char_score_arr)
# print(word_arr[np.argmax(init_words)])