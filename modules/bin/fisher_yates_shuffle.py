import random
import sys


def fisher_yates_shuffle(input_list):
    counter = len(input_list) - 1
    while counter >= 0:
        random_index = random.randint(0, counter)
        input_list.append(input_list.pop(random_index))
        counter -= 1

    return input_list


if __name__ == "__main__":

    if len(sys.argv) >= 2:
        sample_list = sys.argv[1:]
        print("Sample list: {}".format(sample_list))
        shuffled_list = fisher_yates_shuffle(sample_list)
        print("Shuffled list: {}".format(shuffled_list))

    else:
        print("You did not provide any arguments so I made a sample list for you!")
        sample_list = [1, 2, 5, 4, 10, 9, 20]
        print("Sample list: {}".format(sample_list))
        shuffled_list = fisher_yates_shuffle(sample_list)
        print("Shuffled list: {}".format(shuffled_list))
