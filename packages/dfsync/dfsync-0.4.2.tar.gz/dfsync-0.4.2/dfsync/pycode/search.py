import ipdb
from .oai import *


def main():
    inps = ["The dog is barking", "The cat is purring", "The bear is growling"]

    x = embedings(*inps)
    ipdb.set_trace()


if __name__ == "__main__":
    main()
