import re

def strip_string(input_string):
    regex = re.compile('[^(a-zA-Z\.)]')

    output_string = regex.sub('', input_string)

    return output_string

def get_list_from_text(input_text):
    output_list = []

    for word in input_text.split(" "):
        output_list.append(word)

    return output_list


# Mainly for testing purposes, this is a helper module
if __name__ == "__main__":
    sample_string = "lj^7kjsdf&love"
    print("Stripped {} -> {}".format(sample_string, strip_string(sample_string)))
