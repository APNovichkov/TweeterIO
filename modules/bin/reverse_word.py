import sys

def reverse_word(input_word):
    chars = list(input_word)
    output_word = ""

    for i in range(len(chars)):
        output_word += chars[len(chars) - 1 - i]

    return output_word


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sample_word = "Hello"
        print("Reversing {} -> {}".format(sample_word, reverse_word(sample_word)))
    else:
        input_word = sys.argv[1]
        print("Reversing {} -> {}".format(input_word, reverse_word(input_word)))
