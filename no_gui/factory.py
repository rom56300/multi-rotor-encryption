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
    np.save(name + '.npy', dic)
    print(Fore.LIGHTYELLOW_EX + "Configuration Saved")


class Rotor:

    def __init__(self, name: str, permutation: str, position: int = 0):
        self.name = name
        self.permutation = permutation
        self.position = position

    def turn(self):
        self.position += 1

    def permute(self, char: str = None):
        if char is not None:
            pos = self.position
            perm = list(self.permutation)
            letter = perm[pos]
            new = ord(char) + ord(letter)
            if new > 1112064: new -= 1112064
            new_letter = chr(new)
            self.turn()
            if self.position == len(string.printable):
                self.position = 0
            return new_letter

    def reverse(self, char: str = None):
        if char is not None:
            pos = self.position
            perm = list(self.permutation)
            letter = perm[pos]
            old = ord(char) - ord(letter)
            if old < 0: old += 1112064
            old_letter = chr(old)
            self.turn()
            if self.position == len(string.printable):
                self.position = 0
            return old_letter

    def bpermute(self, byte: int = None):
        if byte is not None:
            pos = self.position
            perm = list(self.permutation)
            letter = perm[pos]
            new = byte + ord(letter)
            if new >= 256: new -= 256
            self.turn()
            if self.position == len(string.printable):
                self.position = 0
            return new

    def breverse(self, byte: bytes = None):
        if byte is not None:
            pos = self.position
            perm = list(self.permutation)
            letter = perm[pos]
            old = byte - ord(letter)
            if old < 0: old += 256
            self.turn()
            if self.position == len(string.printable):
                self.position = 0
            return old


if __name__ == '__main__':
    main()