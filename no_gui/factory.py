import random
import string
import numpy as np
from colorama import Fore


def main():
    name = input("Name of the config: ")
    save_config(make(), name)


def make():
    n = int(input("Number of rotors: "))
    rot = [Rotor(a2r(i), generate_permutation()) for i in range(1, n+1)]
    return rot


def generate_permutation():
    return ''.join(random.choice(string.printable) for _ in range(len(string.printable)))


def a2r(i: int):
    RMAP = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'),
            (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    r = []
    for v, s in RMAP:
        while i >= v:
            r.append(s)
            i -= v
    return ''.join(r)


def save_config(dic: dict, name: str):
    np.save('configs/' + name + '.npy', dic)
    print(Fore.LIGHTYELLOW_EX + "Configuration Saved")


class Rotor:

    def __init__(self, name: str, permutation: str, position: int = 0):
        self.name = name
        self.permutation = permutation
        self.position = position

    def turn(self):
        self.position += 1


if __name__ == '__main__':
    main()
