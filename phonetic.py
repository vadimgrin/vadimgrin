from typing import *

NATO = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot","Golf",  "Hotel", "India",
        "Juliet","Kilo", "Lima",   "Mike",  "November","Oscar",  "Papa",  "Quebec","Romeo",
        "Sierra","Tango","Uniform","Victor","Whiskey", "Xray",   "Yankee", "Zulu"]


def translate(word: str) -> str:
    print(list(map(lambda x: NATO[ord(x.upper()) - ord('A')], word)))


if __name__ == '__main__':
    translate('RedFox')
