import random

quotes = [
    'This is amazing',
    "I have the best view of the city",
    "Wow look at that moon"]

def random_python_quote():
    random_index = random.randint(0, len(quotes) - 1)
    return quotes[random_index]


if __name__ == "__main__":
    print(random_python_quote())
