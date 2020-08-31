import nltk
nltk.download('punkt')
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def get_sentence_list_from_corpus(text_path):
    output_list = []

    with open(text_path, 'r') as f:
        f_as_string = f.read().replace("\n", " ")
        output_list = tokenizer.tokenize(f_as_string)

    return output_list

def get_sentence_list_from_string(input_string):
    return tokenizer.tokenize(input_string)


if __name__ == "__main__":
    path = "/Users/andreynovichkov/Desktop/Make-School/Term-2/CS1_2/10.21/CS-1.2-Intro-Data-Structures/Tweet_generator/static/text/treasure_island.txt"

    listt = get_sentence_list_from_corpus(path)

    print(listt)
