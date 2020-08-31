import dictionary_words
import rearrange
import sys
import itertools

dic_words = dictionary_words.get_words()

def get_all_anagrams(word):
    output_anagrams = []

    word_chars = list(word)

    for n in range(len(word_chars) - 1):
        for permutation in itertools.permutations(word_chars, len(word_chars)):
            current_str = set_to_string(permutation).lower()
            output_anagrams.append(current_str)

    return remove_duplicates(output_anagrams)

def get_anagrams_from_dictionary(word):
    output_anagrams = []

    for dic_word in dic_words:
        # Only look if length matches
        if len(dic_word) == len(word):
            original_dic_word = dic_word

            word_chars = list(word.lower())
            dic_word_chars = list(dic_word.lower().strip())

            is_match = True
            for word_char in word_chars:
                if word_char not in dic_word_chars:
                    is_match = False
                    break
                else:
                    dic_word_chars.pop(dic_word.find(word_char))
                    dic_word = dictionary_words.list_to_string(dic_word_chars)

            if is_match:
                output_anagrams.append(original_dic_word)

    return remove_duplicates(output_anagrams)

def set_to_string(input_set):
    output_string = ""
    for item in input_set:
        output_string += item

    return output_string

def remove_duplicates(input_list):
    output_list = []

    for item in input_list:
        if item not in output_list:
            output_list.append(item)

    return output_list


if __name__ == "__main__":
    input_word = sys.argv[1]

    print("Anagrams of your word: {} that is in the dictionary...".format(input_word))

    print(get_anagrams_from_dictionary(input_word))
