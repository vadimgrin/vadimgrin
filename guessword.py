import enchant
import plotly


if __name__ == '__main__':
    my_dict = enchant.Dict("en_US")
    letters = 'qwtyaefjkzxcvbm'
    for first in letters:
        for second in letters:
            # ======= 1 == 2 === 3 === 4 === 5 ==
            word = (' %s   A   %s    E   Y' % (first, second)).replace(' ', '')
            if my_dict.check(word):
                print(word, my_dict.check(word))

