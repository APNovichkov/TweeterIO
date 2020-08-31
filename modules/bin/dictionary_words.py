import sys
import random
import rearrange


NUM_WORDS_AVAIL = 235886
WORDS_PATH = "/usr/share/dict/words"

def get_words():
    all_words = []
    with open(WORDS_PATH, "r") as f:
        for line in f:
            all_words.append(line.strip())

    return all_words

def get_random_words(num_words):
    output_words = []
    random_indexes = generate_random_indexes(int(num_words), NUM_WORDS_AVAIL)

    current_index = 0

    with open(WORDS_PATH, "r") as f:
        for line in f:
            if current_index in random_indexes:
                output_words.append("{} ".format(line.strip()))
            current_index += 1

    return output_words


def generate_random_indexes(num_indexes, max_index):
    indexes = []
    for i in range(num_indexes):
        indexes.append(random.randint(0, max_index))
    return indexes

def list_to_string(input_list):
    output_string = ""
    for item in input_list:
        output_string += item
    return output_string

def is_word_in_dictionary(word):
    return word in get_words()


if __name__ == "__main__":
    print(list_to_string(rearrange.rearrange_words(get_random_words(sys.argv[1]))))
