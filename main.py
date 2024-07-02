import random
import os
import select
import sys

FIELD_SIZE = 30 

class Zmeya:
    speed: list[int] = [0, 1]
    segments: list[list[int]] = [[FIELD_SIZE//2, 1]]
    directions = {'h': [0, -1],
                  'j': [1, 0],
                  'k': [-1, 0],
                  'l': [0, 1],
                  }


    def move(self, dir, sweetie):
        if dir:
            dir = dir[0].readline().strip()
        self.speed = self.directions.get(dir, self.speed)
        head = self.segments[0]
        new_position = [head[0] + self.speed[0],
                        head[1] + self.speed[1]]
        if new_position in self.segments:
            return False
        new_position = self.wraparound(new_position)
        self.segments = [new_position, *self.segments]
        if sweetie != new_position:
            self.segments = self.segments[:-1]

        return True
    
    def wraparound(self, new_position):
        if new_position[0] < 1:
            new_position[0] = FIELD_SIZE
        if new_position[1] < 1:
            new_position[1] = FIELD_SIZE
        if new_position[0] > FIELD_SIZE:
            new_position[0] =  1
        if new_position[1] > FIELD_SIZE:
            new_position[1] =  1

        return new_position



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
            if [i, j] in zmeya.segments:
                print('o', end='')
            elif [i, j] == sweetie:
                print('*', end='')
            elif i == 0 or i == FIELD_SIZE + 1:
                print("_", end='')
                if i == 0 and j == FIELD_SIZE + 1:
                    print(len(zmeya.segments), end='')
            elif j == 0 or j == FIELD_SIZE + 1:
                print('|', end='')
            else:
                print(' ', end='')
            if j == FIELD_SIZE + 1:
                print()

    # dir = subprocess.call('read -t 1')
    i, o, e = select.select( [sys.stdin], [], [], 1)
    if not zmeya.move(i or '', sweetie):
        print("GAME OVER!")
        break
