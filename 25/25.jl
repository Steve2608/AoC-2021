using Base.Iterators
using ArgParse

function readInput(filename::String)
    open(filename) do file
        data = read(file, String)

        rows = split(data, "\n")
        matrix = zeros(Int, length(rows), length(rows[1]))
        for (i, row) in enumerate(rows)
            row = split(row, "")
            row_int = zeros(Int, size(row))
            row_int[row .== "."] .= 0
            row_int[row .== ">"] .= 1
            row_int[row .== "v"] .= 2
            matrix[i, :] = row_int
        end
        return matrix
    end
end

function one_step(seafloor)
    seafloor_next = copy(seafloor)
    x, y = size(seafloor_next)
    moved_already = falses(size(seafloor_next))
    for i in 1:x
        for j in 1:y
            if seafloor_next[i, j] == 1 && !moved_already[i, j]
                j_next = j + 1
                if j_next > y
                    j_next = 1
                end
                if seafloor_next[i, j_next] == 0 && !moved_already[i, j_next]
                    seafloor_next[i, j_next] = 1
                    seafloor_next[i, j] = 0

                    moved_already[i, j_next] = true
                    moved_already[i, j] = true
                end
            end
        end
    end

    moved_already .= false
    for i in 1:x
        for j in 1:y
            if seafloor_next[i, j] == 2 && !moved_already[i, j]
                i_next = i + 1
                if i_next > x
                    i_next = 1
                end

                if seafloor_next[i_next, j] == 0 && !moved_already[i_next, j]
                    seafloor_next[i_next, j] = 2
                    seafloor_next[i, j] = 0

                    moved_already[i_next, j] = true
                    moved_already[i, j] = true
                end
            end
        end
    end
    return seafloor_next
end

function part1(seafloor)
    for i in countfrom(1)
        next = one_step(seafloor)
        all(seafloor .== next) && return i
        seafloor = next
    end
end

function parse_cli()
    s = ArgParseSettings()
    @add_arg_table s begin
        "--example"
            help = "Calculate example"
            action = :store_true
    end
    return parse_args(s)
end

args = parse_cli();
if args["example"] || true
    seafloor = readInput("example.txt");

    n_steps = part1(seafloor);
    @assert n_steps == 58;
end

seafloor = readInput("input.txt");

n_steps = part1(seafloor);
println(n_steps);
