import sys

from helpers import count_words

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        print(count_words(f.read()))
