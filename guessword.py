import enchant


if __name__ == '__main__':
    my_dict = enchant.Dict("en_US")
    letters = 'qwtyupdfgajklzxcvbnm'
    for first in letters:
        for second in letters:
            for third in letters:
                # ======= 1 == 2 === 3 === 4 === 5 ==
                word = (' n    a    %s    %s     %s   ' % (first, second, third)).replace(' ', '')
                if my_dict.check(word):
                    print(word, my_dict.check(word))

