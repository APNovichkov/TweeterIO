import string_utils
import word_frequency


class Node:
    def __init__(self, char):
        self.char = char
        self.nodes = []
        self.is_word = False
        self.num_words_at_letter = 0


def add_word(root, input_word):
    """Add word given a root node."""

    cNode = root

    for char in list(input_word):
        does_exist_in_cNode_children = False

        for node in cNode.nodes:
            if node.char == char:
                does_exist_in_cNode_children = True
                cNode.num_words_at_letter += 1
                cNode = node

        if not does_exist_in_cNode_children:
            new_node = Node(char)
            cNode.nodes.append(new_node)
            cNode.num_words_at_letter += 1
            cNode = new_node

    #cNode.num_words_at_letter += 1
    cNode.is_word = True


def contains_word(root, input_word):
    """Check if word is in the Trie and return True/False."""

    cNode = root

    for char in list(input_word):
        found_match = False
        for node in cNode.nodes:
            if node.char == char:
                found_match = True
                cNode = node
                break

        if not found_match:
            print("Exited in for loop")
            return False

    return cNode.is_word

def contains_prefix(root, input_prefix):
    """Check if prefix exists and return True/False w/ num of words with that prefix."""

    output_list = []

    cNode = root

    for char in list(input_prefix):
        found_match = False
        for node in cNode.nodes:
            if node.char == char:
                found_match = True
                cNode = node
                break
        if not found_match:
            return False, 0

    return True, cNode.num_words_at_letter


def get_words_with_prefix(root, input_prefix):
    """Return list of words with given prefix."""

    cNode = root
    input_prefix = input_prefix.lower()

    # Check if prefix exists, only continue if it does
    if not contains_prefix(root, input_prefix):
        return []

    print("Getting to last char of prefix: {}".format(input_prefix))

    # Gets to the last node in the prefix
    for char in list(input_prefix):
        print("At char: {}".format(char))
        for node in cNode.nodes:
            if node.char == char:
                print("Found matching char in cNode, going to the next char: {}".format(node.char))
                cNode = node
                break


    # cNode is now at the last node in the prefix, need all words that stem from that root
    words_from_root = get_all_words_from_root(cNode)

    print("Found {} words from root char: {}".format(len(words_from_root), cNode.char))

    output_list = []

    for word in words_from_root:
        output_list.append("{}{}".format(input_prefix, word))

    return output_list


# Helper functions
def get_all_words_from_root(root):
    if len(root.nodes) == 0:
        return " "

    output_list = []

    for node in root.nodes:
        for element in get_all_words_from_root(node):
            #print("Adding element: {}".format(element))
            output_list.append(node.char + element.strip())

    return output_list

def _get_all_words_from_root(root, input_words):
    # Breaking point
    if len(root.nodes) == 0:
        return root.char

    output_words = input_words

    print("Getting all words from root: {}".format(root.char))

    for node in root.nodes:

        output_words.append(node.char)
        print("In node: {}".format(node.char))

        for word in get_all_words_from_root(node, output_words):
            print("Appending {} to output_words".format(word))
            output_words.append(word)

    print("Done with recursion for root: {}".format(root))

    return output_words


if __name__ == "__main__":
    root = Node("*")
    list_of_words = word_frequency.get_list_from_book("/usr/share/dict/words")

    word_counter = 0

    print("Length of list of words: {}".format(len(list_of_words)))

    for word in list_of_words:
        word = word.lower()
        word = string_utils.strip_string(word)

        if word.isalpha():
            word_counter += 1
            add_word(root, word)

    print("Finished adding {} words to trie\n\n".format(word_counter))

    test_prefix = "an"
    does_contain, num_words = contains_prefix(root, test_prefix)
    if does_contain:
        print("Trie contains the prefix: \"{}\", and has {} words with that prefix".format(test_prefix, num_words))
    else:
        print("Trie does not contain the prefix: {}".format(test_prefix))

    words_from_prefix = get_words_with_prefix(root, test_prefix)

    print("The words with prefix \"{}\" are:".format(test_prefix))
    print(words_from_prefix)

if __name__ == "__main___":
    root = Node("*")

    add_word(root, "andrey")
    add_word(root, "andrea")
    add_word(root, "andres")
    add_word(root, "ass")
    add_word(root, "another")
    add_word(root, "dope")

    test_word = "andrea"
    if contains_word(root, test_word):
        print("Trie contains the word {}".format(test_word))
    else:
        print("Trie DOES NOT contain the word {}".format(test_word))

    test_prefix = "a"
    does_contain, num_words = contains_prefix(root, test_prefix)
    if does_contain:
        print("Trie contains the prefix: \"{}\" and has {} words with that prefix".format(test_prefix, num_words))
    else:
        print("Trie does not contain the prefix: {}".format(test_prefix))

    words_from_prefix = get_words_with_prefix(root, test_prefix)

    #print("The words with prefix \"{}\" are:".format(test_prefix))
    #print(words_from_prefix)
