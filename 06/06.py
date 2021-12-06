from collections import Counter
# from time import perf_counter_ns

from sim import simulate_pop

if __name__ == '__main__':
    with open('input.txt') as in_file:
        counts = Counter(map(int, in_file.read().strip().split(',')))

    pop = [counts[i] for i in range(9)]
    # t1 = perf_counter_ns()
    part1 = simulate_pop(pop, days=80, offset=0)
    part2 = simulate_pop(pop, days=256 - 80, offset=80)
    # t2 = perf_counter_ns()
    # print(f'algo(...) :: {t2 - t1}')
    print(part1, part2, sep='\n')
