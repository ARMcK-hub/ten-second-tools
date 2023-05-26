"""
Scryb - SQL DB Mock Dataset (functions)
Author: Andrew McKinney
Creation Date: 2020-02-08
"""

# import dependencies
import random
import numpy as np

#  returns a random string of letters and numbers of given length
def randstr(string_length=5, bias=1, all_nums=False):
    # string_length is length of returned string
    # bias is the ratio bias of letters to numbers, rounds to nearest integer
    # all_nums = True will do essentially random.randint except returned as a string

    # creating general values
    bias = round(bias)
    string_range = np.arange(0, string_length)
    letter_choice = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number_choice = "1234567890"

    # artificial number-letter biased in random selection
    char_biased = {0: letter_choice}

    for num in range(1, bias + 1):
        char_biased[num] = number_choice

    # empty string initiated
    string_out = ""

    # constructing string from random choice of a letter or number, based on bias input
    for chars in string_range:
        if all_nums == True:
            char_choice = random.choice(number_choice)
        else:
            char_choice = char_biased[random.randint(0, len(char_biased) - 1)]
        char = random.choice(char_choice)
        string_out += char

    return string_out


# randlist chooses a random amount of random items from an iterable item ranging from 0 to the entire iter_item
def randlist(iter_item):
    # iter_item is the iterable to be chosen from

    # copying iterration item and generating count choice
    item_list = iter_item[:]
    iter_item_len = len(item_list)
    iter_item_count_choice = np.arange(0, iter_item_len + 1)

    count = random.choice(iter_item_count_choice)

    # empty return list
    return_items = []

    # bypassing a choice of 0 items
    if count == 0:
        return return_items

    # returning random choice of count # of items
    else:
        for item_count in np.arange(0, count):
            item = random.choice(item_list)
            item_list.remove(item)
            return_items.append(item)

        return return_items
