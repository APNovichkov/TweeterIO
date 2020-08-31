import time

def time_it(func):
    """Time the runtime of a function that it is wrapping."""

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("{} took {} ms to complete".format(func.__name__, (end - start) * 1000))

        return result

    return wrapper
