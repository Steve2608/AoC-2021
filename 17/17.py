from math import ceil, sqrt
import re


def part1(y_min: int) -> int:
    n = abs(y_min) - 1
    return n * (n + 1) >> 1


def part2(x_min: int, x_max: int, y_min: int, y_max: int) -> int:
    def generate_x(dx):
        x = 0
        while x <= x_max: 
            yield x >= x_min
            x += dx
            if dx > 0:
                dx -= 1

    def generate_y(dy):
        y = 0
        while y >= y_min:
            yield y <= y_max
            y += dy
            dy -= 1
    
    def both(x, y) -> bool:
        return x and y
    
    def inverse_gaussian_sum(m: int):
        return ceil((-1 + sqrt(1 + m << 3)) / 2)

    # clever brute force
    return sum(
        sum(any(map(both, generate_x(x), generate_y(y))) for y in range(y_min, -y_min))
        for x in range(inverse_gaussian_sum(x_min), x_max + 1)
    )


if __name__ == '__main__':
    if __debug__:
        with open('example.txt') as in_file:
           x_min, x_max, y_min, y_max = map(int, re.findall(r'-?\d+', in_file.read()))
        assert part1(y_min) == 45, f'{part1(y_min)=} != 45'
        assert part2(x_min, x_max, y_min, y_max) == 112, f'{part2(x_min, x_max, y_min, y_max)=} != 112'

    with open('input.txt') as in_file:
        x_min, x_max, y_min, y_max = map(int, re.findall(r'-?\d+', in_file.read()))
    print(part1(y_min))
    print(part2(x_min, x_max, y_min, y_max))
