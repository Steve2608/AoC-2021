from functools import partial

import z3


def solve(code: list[list[str]]):
    int64 = partial(z3.BitVec, bv=64)
    int64val = partial(z3.BitVecVal, bv=64)

    def encode_digits(solver):
        inp = [int64(name=f'd_{i}') for i in range(14)]
        for d in inp:
            solver.add(z3.And(1 <= d, d <= 9))
        return inp

    def add_program_constraints(solver, digits):
        input_iter = iter(digits)
        for i, inst in enumerate(code):
            # read input
            if inst[0] == 'inp':
                reg[inst[1]] = next(input_iter)
            else:
            instr, a, b = inst
                b = reg[b] if b in reg else int(b)
                c = int64(name=f'v_{i}')
            
            if instr == 'add':
                    solver.add(c == reg[a] + b)
            elif instr == 'mul':
                    solver.add(c == reg[a] * b)
            elif instr == 'mod':
                    solver.add(c == reg[a] % b)
            elif instr == 'div':
                    solver.add(c == reg[a] / b)
            elif instr == 'eql':
                    solver.add(c == z3.If(reg[a] == b, one, zero))
            else:
                raise ValueError(f'Invalid state: {instr}')

                reg[a] = c

        # finally z needs to be
        solver.add(reg['z'] == 0)

    def parse_result(model) -> int:
        return int(''.join(map(str, (model[d] for d in inp_digits))))
    
    # constants
    zero, one = int64val(0), int64val(1)
    reg = {v: zero for v in 'xyzw'}
    solver = z3.Optimize()

    # input constraints
    inp_digits = encode_digits(solver)
    # constraints by code
    add_program_constraints(solver, inp_digits)

    # formulate input
        inp = sum((10 ** i) * d for i, d in enumerate(inp_digits[::-1]))
    for optimize in (solver.maximize, solver.minimize):
        solver.push()
        optimize(inp)
        
        # 'run' solver
        yield parse_result(solver.model()) if solver.check() else None
        
        solver.pop()


if __name__ == '__main__':
    with open('input.txt') as in_file:
        code = [line.split() for line in in_file if line]

    p1, p2 = solve(code)
    print(p1)
    print(p2)
