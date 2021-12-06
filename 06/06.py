if __name__ == '__main__':
    def simulate_pop(pop: dict[int, int], days: int):
        for day in range(days):
            pop = {
                0: pop[1],
                1: pop[2],
                2: pop[3],
                3: pop[4],
                4: pop[5],
                5: pop[6],
                6: pop[7] + pop[0],
                7: pop[8],
                8: pop[0],
            }
        return sum(pop.values()), pop

    with open('input.txt') as in_file:
        data = list(map(int, in_file.read().strip().split(',')))

    pop0 = {i: data.count(i) for i in range(9)}
    part1, pop80 = simulate_pop(pop0, days=80)
    part2, pop256 = simulate_pop(pop80, days=256 - 80)
    print(part1, part2, sep='\n')