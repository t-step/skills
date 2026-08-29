import sys

from src.generate import make_thumbnail


def main():
    with open(sys.argv[1], "rb") as f:
        data = f.read()
    out = make_thumbnail(data, (128, 128))
    with open(sys.argv[2], "wb") as f:
        f.write(out)


if __name__ == "__main__":
    main()
