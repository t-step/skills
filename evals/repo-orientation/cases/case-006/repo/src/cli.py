import argparse

from src.crawler import crawl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    broken = crawl(args.url)
    for link in broken:
        print(link)


if __name__ == "__main__":
    main()
