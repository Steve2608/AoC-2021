import re

import numpy as np


def to_coordinate_pairs(line):
    a, b, c, d, e, f = line
    return ((a, b + 1), (c, d + 1), (e, f + 1))


def part2(cubes: dict):
    def get_slice(p: tuple[int, int], ps: np.ndarray):
        start, stop = np.searchsorted(ps, p)
        return slice(start, stop)

    # find boundaries per axis (segments)
    xs, ys, zs = map(np.unique, zip(*cubes))

    # find distances per axis (segments)
    xd, yd, zd = map(np.diff, (xs, ys, zs))
    
    # find size per segment
    sizes = np.einsum('i,j,k -> ijk', xd, yd, zd, dtype=np.int64)
    
    # initialize all with turned-off
    states = np.zeros_like(sizes, dtype=bool)

    for (x, y, z), s in cubes.items():
        x_, y_, z_ = get_slice(x, xs), get_slice(y, ys), get_slice(z, zs)
        states[x_, y_, z_] = s

    return np.sum(sizes[states])


def part1(cubes: dict):
    cubes = {
        ((a, b), (c, d), (e, f)): on for ((a, b), (c, d), (e, f)), on in cubes.items()
        if all(abs(x) <= 50 for x in (a, c, e)) and all(abs(x) <= 51 for x in (b, d, f))
    }

    return part2(cubes)


if __name__ == '__main__':
    if __debug__:
        with open('example.txt') as in_file:
            cubes = { to_coordinate_pairs(map(int, re.findall(r'-?\d+', line))): line.startswith('on') for line in in_file }

        assert part1(cubes) == 474140, f'{part1(cubes)=} != 474140'
        assert part2(cubes) == 2758514936282235, f'{part2(cubes)=} != 2758514936282235'

    with open('input.txt') as in_file:
        cubes = { to_coordinate_pairs(map(int, re.findall(r'-?\d+', line))): line.startswith('on') for line in in_file }

    print(part1(cubes))
    print(part2(cubes))
