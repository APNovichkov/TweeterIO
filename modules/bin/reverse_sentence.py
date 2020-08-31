import sys

def reverse_sentence(input_sentence=sys.argv[1:]):
    output_sentence = ""

    for i in range(len(input_sentence)):
        output_sentence += "{} ".format(input_sentence[len(input_sentence) - 1 - i])

    return output_sentence


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sample_sentence = ['Hello', 'World']
        print("Reversing {} -> {}".format(sample_sentence, reverse_sentence(sample_sentence)))
    else:
        input_sentence = sys.argv[1:]
        print("Reversing {} -> {}".format(input_sentence, reverse_sentence(input_sentence)))
