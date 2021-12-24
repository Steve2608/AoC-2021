import z3


def solve(code: list[list[str]]):
    def encode_digits(solver):
        inp_digits = [z3.BitVec(f'd_{i}', 64) for i in range(14)]
        for d in inp_digits:
            solver.add(1 <= d)
            solver.add(d <= 9)
        return inp_digits

    def add_program_constraints(solver, digits):
        digit_input = iter(digits)
        for i, inst in enumerate(code):
            # read input
            if inst[0] == 'inp':
                registers[inst[1]] = next(digit_input)
                continue

            instr, a, b = inst
            b = registers[b] if b in registers else int(b)
            c = z3.BitVec(f'v_{i}', 64)
            
            if instr == 'add':
                solver.add(c == registers[a] + b)
            elif instr == 'mul':
                solver.add(c == registers[a] * b)
            elif instr == 'mod':
                solver.add(c == registers[a] % b)
            elif instr == 'div':
                solver.add(c == registers[a] / b)
            elif instr == 'eql':
                solver.add(c == z3.If(registers[a] == b, one, zero))
            else:
                raise ValueError(f'Invalid state: {instr}')

            registers[a] = c

        # finally z needs to be
        solver.add(registers['z'] == 0)

    solver = z3.Optimize()
    
    # constants
    zero, one = z3.BitVecVal(0, 64), z3.BitVecVal(1, 64)
    registers = {v: zero for v in 'xyzw'}

    # input constraints
    inp_digits = encode_digits(solver)
    # constraints by code
    add_program_constraints(solver, inp_digits)

    for func in (solver.maximize, solver.minimize):
        solver.push()

        # construct input
        inp = sum((10 ** i) * d for i, d in enumerate(inp_digits[::-1]))
        
        # fit to func
        func(inp)
        
        # if solver is satisfyable
        if solver.check():
            m = solver.model()
            yield ''.join(str(m[d]) for d in inp_digits)
        solver.pop()


if __name__ == '__main__':
    with open('input.txt') as in_file:
        code = [line.split() for line in in_file if line]

    p1, p2 = solve(code)
    print(p1)
    print(p2)
