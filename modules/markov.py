# For Flask


try:
    from .dictogram import Dictogram
    from . import sample
    from . import data_provider
except:
    from dictogram import Dictogram
    import sample
    import data_provider

# For local
# import string_utils
# from dictogram import Dictogram
# import sample

class Markov:
    def __init__(self):
        self.states = {}
        self.start_token = {'start_state': Dictogram()}
        self.stop_token = {'stop_state': Dictogram()}

    def refresh_markov(self):
        self.states = {}

    def build_chain_n_order(self, sentence_list, order):

        # Run through sentences
        for sentence_index in range(len(sentence_list)):
            word_list = sentence_list[sentence_index].split(" ")

            # Only analyze sentences whose length is bigger than order
            if len(sentence_list[sentence_index]) > order:
                for word_index in range(len(word_list) - order):
                    c_state = []  # Current State could be "I was sitting"
                    n_state = []  # Next State could be "was sitting in"

                    for i in range(0, order):
                        c_state.append(word_list[word_index + i])
                        n_state.append(word_list[word_index + 1 + i])  # We add one to shift one to the right

                    # Add first state to start token dictogram
                    if word_index == 0:
                        self.start_token['start_state'].add_count((*c_state,))

                    # Add last state to stop token dictogram
                    if word_index == (len(word_list) - order - 1):
                        self.stop_token['stop_state'].add_count((*n_state,))

                    if tuple(c_state) not in self.states.keys():
                        self.states[(*c_state,)] = Dictogram((*n_state,))
                    else:
                        self.states[(*c_state,)].add_count((*n_state,))

        # print("Start tokens: {}".format(self.start_token))
        # print("Stop tokens: {}".format(self.stop_token))

    def generate_sentence_n_order(self, order):
        sentence = []
        current_state = None

        counter = 0

        while(current_state not in self.stop_token['stop_state'].keys()):
            if counter == 100:
                break

            if len(sentence) == 0:
                # Generate first phrase, should be completely random for now
                first_phrase = self.start_token['start_state'].sample()
                # print("first phrase: {}".format(first_phrase))
                for word in first_phrase:
                    sentence.append(word)

                current_state = first_phrase

            if current_state in self.states.keys():
                current_state = self.states[current_state].sample()
                new_word = current_state[order - 1]
                sentence.append(new_word)

            counter += 1

        return " ".join(sentence)


if __name__ == "__main__":
    word_list_1 = ['one', 'fish', 'two', 'fish', 'three', 'fish', 'blue', 'fish', 'blue']
    sentence_list = data_provider.get_sentence_list_from_string("I am cold and I am happy and you are crazy. But we all know why. The song sings for me. I am not afraid of the dark.")
    # word_list = word_frequency.get_list_from_book("sample_book_text.txt")

    mk = Markov()
    mk.build_chain_n_order(sentence_list, 3)

    print("Input word list: {}".format(sentence_list))
    print("-----------------------------------------")
    print("Output chain: {}".format(mk.states))

    print("Generated sentence: {}".format(mk.generate_sentence_n_order(3)))
