import random
import os
import sys
import termios
import tty
import select

FIELD_SIZE = 30

class Zmeya:
    def __init__(self):
        self.speed = [0, 1]
        self.segments = [[FIELD_SIZE // 2, 1]]
        self.directions = {'h': [0, -1],
                           'j': [1, 0],
                           'k': [-1, 0],
                           'l': [0, 1]}
    def get_head(self):
        if self.speed == [0, 1]:
            return '>'
        elif self.speed == [0, -1]:
            return '<'
        elif self.speed == [1, 0]:
            return 'v'
        elif self.speed == [-1, 0]:
            return '^'

    def move(self, dir, sweetie):
        if dir:
            self.speed = self.directions.get(dir, self.speed)
        head = self.segments[0]
        new_position = [head[0] + self.speed[0], head[1] + self.speed[1]]
        if new_position in self.segments:
            return False
        new_position = self.wraparound(new_position)
        self.segments = [new_position] + self.segments
        if sweetie != new_position:
            self.segments.pop()
        return True

    def wraparound(self, new_position):
        if new_position[0] < 1:
            new_position[0] = FIELD_SIZE
        if new_position[1] < 1:
            new_position[1] = FIELD_SIZE
        if new_position[0] > FIELD_SIZE:
            new_position[0] = 1
        if new_position[1] > FIELD_SIZE:
            new_position[1] = 1
        return new_position

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        rlist, _, _ = select.select([fd], [], [], 0.5)
        if rlist:
            return sys.stdin.read(1)
        else:
            return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

zmeya = Zmeya()
sweetie = None

while True:
    if len(zmeya.segments) == FIELD_SIZE ** 2:
        print("YOU WON!")
        break

    os.system('clear')
    sweetie = sweetie or zmeya.segments[0]
    while sweetie in zmeya.segments:
        sweetie = [random.randint(1, FIELD_SIZE), random.randint(1, FIELD_SIZE)]

    for i in range(FIELD_SIZE + 2):
        for j in range(FIELD_SIZE + 2):
            if [i, j] == zmeya.segments[0]:
                print(zmeya.get_head(), end='')
            elif [i, j] in zmeya.segments[1:]:
                print('o', end='')
            elif [i, j] == sweetie:
                print('*', end='')
            elif i == 0 or i == FIELD_SIZE + 1:
                print("_", end='')
                if i == 0 and j == FIELD_SIZE + 1:
                    print("\t\t\t", len(zmeya.segments), end='')
            elif j == 0 or j == FIELD_SIZE + 1:
                print('|', end='')
            else:
                print(' ', end='')
            if j == FIELD_SIZE + 1:
                print()

    dir = get_key()
    if not zmeya.move(dir, sweetie):
        print("GAME OVER!")
        break
