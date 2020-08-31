import random
import sys


def rearrange_words(input_list):
    input_pool_indexes = list(range(len(input_list)))
    new_list = []

    while(len(input_pool_indexes) != 0):
        random_index = random.randint(0, len(input_pool_indexes) - 1)
        new_list.append(input_list[input_pool_indexes[random_index]])
        input_pool_indexes.pop(random_index)

    return new_list

def rearrange_letters(word):
    word_in_chars = list(word)
    input_word_indexes = list(range(len(word_in_chars)))
    new_word = ""

    while(len(input_word_indexes) != 0):
        random_index = random.randint(0, len(word_in_chars) - 1)
        new_word += word_in_chars[input_word_indexes[random_index]]
        input_word_indexes.pop(random_index)

    return new_word


if __name__ == "__main__":
    print(rearrange_words(sys.argv[1:]))
