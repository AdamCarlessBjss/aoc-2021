#!/usr/bin/env python3

def parse_file(filename):
    directions = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            direction = tuple(line.strip("\n").split(" "))
            directions.append(direction)
    return directions

def follow_nav_directions(directions):
    h = 0
    v = 0

    for i in directions:
        if i[0] == "up":
            v -= int(i[1])
        if i[0] == "down":
            v += int(i[1])
        if i[0] == "forward":
            h += int(i[1])

    return h, v


def follow_aim_directions(directions):
    h = 0
    v = 0
    aim = 0

    for i in directions:
        if i[0] == "up":
            aim -= int(i[1])
        if i[0] == "down":
            aim += int(i[1])
        if i[0] == "forward":
            h += int(i[1])
            v += aim * int(i[1])

    return h, v

directions = parse_file("input.txt")

final_position = follow_nav_directions(directions)
print(f'final position multiple: {final_position[0] * final_position[1]}')

final_position = follow_aim_directions(directions)
print(f'final position multiple: {final_position[0] * final_position[1]}')
