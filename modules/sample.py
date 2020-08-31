import sys
import random

try:
    from . import word_frequency
except:
    import word_frequency

def sample_word(input_histogram):
    input_keys = list(input_histogram.keys())
    random_index = random.randint(0, len(input_keys) - 1)

    return input_keys[random_index]


def sample_by_frequency_(input_histogram):
    list = []
    for key, value in input_histogram.items():
        for i in range(value):
            list.append(key)

    random_index = random.randint(0, len(list) - 1)

    return list[random_index]


# @time_it
# Optimize for speed once dataset is big enough
def sample_by_frequency(input_histogram):
    frequencies = {}
    output_word = ""
    num_words = sum(input_histogram.values())
    for key, value in input_histogram.items():
        frequencies[key] = value / num_words

    random_num = random.random()

    temp_sum = 0
    for key, value in frequencies.items():
        temp_sum += value
        if random_num <= temp_sum:
            output_word = key
            break

    return output_word


def test_sample_by_frequency(input_histogram):
    output_dict = {}

    for i in range(1000):
        sampled_word = sample_by_frequency(input_histogram)
        if sampled_word in output_dict.keys():
            output_dict[sampled_word] += 1
        else:
            output_dict[sampled_word] = 1

    return output_dict


if __name__ == "__main__":
    input_list = sys.argv[1:]

    histogram = word_frequency.histogram_as_dict(input_list)

    print("Freqency distribution of input words: {}".format(test_sample_by_frequency(histogram)))
