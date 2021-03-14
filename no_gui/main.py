import sys
import random
import string
import colorama

import numpy as np

from colorama import Fore


def main(rot: dict):
    # mainloop
    while True:
        w = input(">>>")
        k = w.split(" ", 1)
        if k[0] == "-e":
            print(Fore.BLUE + cipher(rot, k[1], "e"))

        elif k[0] == "-d":
            print(Fore.BLUE + cipher(rot, k[1], "d"))

        elif k[0] == "-s":
            save_config(rot, k[1])

        elif k[0] == "-l":
            rot = load_config(k[1])

        elif k[0] == "-q":
            sys.exit(0)

        elif k[0] == "-fe":
            with open(k[1].split()[0], 'rb') as y:
                w = y.read()
                z = filepher(rot, w, 'e')
            with open(k[1].split()[1], 'wb') as x: x.write(z)

        elif k[0] == "-fd":
            with open(k[1].split()[0], 'rb') as y:
                w = y.read()
                z = filepher(rot, w, 'd')

            with open(k[1].split()[1], 'wb') as x:
                x.write(z)

        else:
            raise (Fore.RED +
                   "-e [string]: encrypt\n"
                   "-d [encrypted string]: decrypt\n"
                   "-s [config name]: save the current config\n"
                   "-l [config name] : load a config\n"
                   "-q : exit")


def init():
    x = input("Type \"-l [config name]\" to load a config else press enter to create a new config: ")
    if x.startswith('-l'):
        rot = load_config(x.split(' ')[1])
    else:
        n = int(input("Number of rotors: "))
        rot = [Rotor(a2r(i), generate_permutation()) for i in range(1, n+1)]
    return rot


def save_config(dic: dict, name: str):
    np.save(name + '.npy', dic)
    print(Fore.LIGHTYELLOW_EX + "Configuration Saved")


def load_config(name: str):
    try:
        dic = np.load(name + '.npy', allow_pickle=True)
        print(Fore.LIGHTYELLOW_EX + "Configuration Loaded")
        return dic

    except:
        print(Fore.RED + "No Config Named " + name)
        dic = init()
        return dic


def a2r(i: int):
    RMAP = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'),
            (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    r = []
    for v, s in RMAP:
        while i >= v:
            r.append(s)
            i -= v
    return ''.join(r)


def generate_permutation():
    return ''.join(random.choice(string.printable) for _ in range(len(string.printable)))


def cipher(dic: dict, msg: str, mode: str):
    if mode == "e":
        encode = ''
        for char in msg:
            q = char
            for rot in dic:
                q = rot.permute(q)
            encode += q
        for rot in dic:
            rot.position = 0
        return encode

    elif mode == "d":
        decode = ''
        for char in msg:
            q = char
            for rot in dic:
                q = rot.reverse(q)
            decode += q
        for rot in dic:
            rot.position = 0
        return decode


def filepher(dic: dict, msg: str, mode: str):
    if mode == "e":
        encode = bytes()
        for char in msg:
            q = char
            for rot in dic:
                q = rot.bpermute(q)
            encode += bytes([q])
        for rot in dic:
            rot.position = 0
        return encode

    elif mode == "d":
        decode = bytes()
        for char in msg:
            q = char
            for rot in dic:
                q = rot.breverse(q)
            decode += bytes([q])
        for rot in dic:
            rot.position = 0
        return decode


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
    colorama.init(autoreset=True)
    main(init())