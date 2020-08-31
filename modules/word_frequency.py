import sys
import pandas as pd

# For Flask
try:
    from .utils import time_it
    from . import string_utils
    from .dictogram import Dictogram
except:
    from utils import time_it
    import string_utils
    from dictogram import Dictogram


# For Local
# from utils import time_it
# import string_utils
# from dictogram import Dictogram


@time_it
def histogram_as_dict(source_text_as_list):
    """Return histogram as a dict: {'one': 1, 'fish': 4}..."""
    output_dict = Dictogram()

    for word in source_text_as_list:
        output_dict.add_count(word)

    return output_dict

@time_it
def histogram_as_list_of_tuples(source_text_as_list):
    """Return histogram as a list of tuples: [('one', 1), ('fish', 4)]..."""
    output_dict = {}
    output_list_of_tuples = []

    for word in source_text_as_list:
        if word in output_dict.keys():
            output_dict[word] += 1
        else:
            output_dict[word] = 1

    for key, value in output_dict.items():
        output_list_of_tuples.append((key, value))

    return output_list_of_tuples

@time_it
def histogram_as_list_of_lists_(source_text_as_list):
    """Return histogram as a list of lists: [['one', 1], ['fish', 4]]..."""
    output_dict = {}
    output_list_of_lists = []

    for word in source_text_as_list:
        if word in output_dict.keys():
            output_dict[word] += 1
        else:
            output_dict[word] = 1

    for key, value in output_dict.items():
        output_list_of_lists.append([key, value])

    return output_list_of_lists

@time_it
def unique_words(input_histogram_as_dict):
    """Return num of unique words in histogram."""
    return len(input_histogram_as_dict)

# @time_it
def get_list_from_book(text_path):
    """Return a list given a path to a txt file."""
    output_list = []

    with open(text_path, 'r') as f:
        for line in f:
            words = line.split()
            for word in words:
                word = string_utils.strip_string(word).lower()
                if word.isalpha():
                    output_list.append(word)

    return output_list

def save_to_file(histogram_as_dict, filename):
    """Save dictogram to filename."""
    with open(filename, 'w+') as f:
        for key, value in histogram_as_dict.items():
            f.write("{}\t{}\n".format(key, value))

def sort_words(histogram_as_dict):
    """Return sorted dictogram based on dict values(integers)."""
    df = pd.DataFrame.from_dict(histogram_as_dict, orient='index')
    df.columns = ['count']
    df = df.sort_values(by='count', ascending=False)

    return df.to_dict()['count']

def frequency(word, histogram):
    """Return the frequency of that word in the whole dictogram (num_words/total_words)."""
    return histogram.get(word) / sum(histogram.values())


if __name__ == "__main__":
    source_text_as_list = []

    if len(sys.argv) == 2:
        source_text_as_list = get_list_from_book(sys.argv[1])
    else:
        print("You entered too many arguments or no arguments. So we are going to analyze \"The trial of Captain John Kimber\"")
        source_text_as_list = get_list_from_book("sample_book_text.txt")

    print(source_text_as_list)
    # print("Text histogram as dict: {}".format(histogram_as_dict(source_text_as_list)))
    # print("------------------------------------------------------------------------------------")
    # print("Text histogram as list of tuples: {}".format(histogram_as_list_of_tuples(source_text_as_list)))
    # print("------------------------------------------------------------------------------------")
    # print("Text histogram as list of lists: {}".format(histogram_as_list_of_lists(source_text_as_list)))
    # print("------------------------------------------------------------------------------------")
    # print("Number of unique words in histogram: {}".format(unique_words(histogram_as_dict(source_text_as_list))))
    # print("Sorted list: {}".format(sort_words(histogram_as_dict(source_text_as_list))))

    # save_to_file(sort_words(histogram_as_dict(source_text_as_list)), "output_histogram.txt")
