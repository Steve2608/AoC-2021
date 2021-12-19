import itertools as it
from collections import defaultdict


def parse_scanners(scanners_text: list[str]) -> list[list[tuple[int, int, int]]]:
    return [ 
        {tuple(map(int, line.strip().split(','))) for line in lines.splitlines()[1:]}
        for lines in scanners_text
    ]


def map_beacons(scanners_text: list[str], min_match: int = 12) -> set[tuple[int, int, int]]:
    def attempt_merge(already_mapped: set[tuple[int, int, int]], target: set[tuple[int, int, int]]):
        for x_dir, y_dir, z_dir in it.product((1, -1), repeat=3):
            for i_x, i_y, i_z in it.permutations((0, 1, 2)):
                counts = defaultdict(int)
                for coord, (x, y, z) in it.product(target, already_mapped):
                    x_new = x + x_dir * coord[i_x]
                    y_new = y + y_dir * coord[i_y]
                    z_new = z + z_dir * coord[i_z]

                    counts[(x_new, y_new, z_new)] += 1

                if counts[(scanner_pos := max(counts, key=counts.get))] >= min_match:
                    x, y, z = scanner_pos
                    data_new = {(
                        x - x_dir * coord[i_x],
                        y - y_dir * coord[i_y],
                        z - z_dir * coord[i_z]
                    ) for coord in target}
                    
                    return already_mapped | data_new, scanner_pos

    ocean_map, *to_do = parse_scanners(scanners_text)
    scanners = [(0, 0, 0)]

    while to_do:
        for t in to_do:
            if result := attempt_merge(ocean_map, t):
                ocean_map, new_scanner = result
                scanners.append(new_scanner)
                to_do.remove(t)
    
    return ocean_map, scanners


def part12(scanners_text: list[str]) -> int:
    def manhattan(ab: tuple) -> int:
        return sum(abs(a_i - b_i) for a_i, b_i in zip(*ab))

    beacons, scanners = map_beacons(scanners_text)
    return len(beacons), max(map(manhattan, it.combinations(scanners, r=2)))


if __name__ == '__main__':
    if __debug__:
        with open('example.txt') as in_file:
            scanners_text = in_file.read().split('\n\n')

        p1, p2 = part12(scanners_text)
        assert p1 == 79, f'{p1=} != 79'
        assert p2 == 3621, f'{p2=} != 3621'

    with open('input.txt') as in_file:
        scanners_text = in_file.read().split('\n\n')
        
    p1, p2 = part12(scanners_text)
    print(p1)
    print(p2)
