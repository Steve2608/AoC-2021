from collections import Counter
# from time import perf_counter_ns

from sim import simulate_pop

if __name__ == '__main__':
    # t1 = perf_counter_ns()
    with open('input.txt') as in_file:
        counts = Counter(map(int, in_file.read().strip().split(',')))

    pop = [counts[i] for i in range(9)]
    # t2 = perf_counter_ns()
    part1 = simulate_pop(pop, days=80, i=0)
    part2 = simulate_pop(pop, days=256 - 80, i=80 % 9)
    # t3 = perf_counter_ns()
    # print(f'pop = ... :: {t2 - t1}')
    # print(f'algo(...) :: {t3 - t2}')
    print(part1, part2, sep='\n')
