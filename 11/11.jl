using LinearAlgebra

function readInput(filename::String)::Matrix{Int}
	open(filename) do file
		return transpose(hcat([parse.(Int, split(line, "")) for line in readlines(file)]...))
	end
end

function print_matrix(mat::Matrix{Int})
    show(stdout, "text/plain", mat)
    println()
end

function flash(mat::Matrix{Int})::Tuple{Matrix{Int}, Matrix{Bool}}
    w, h = size(mat)
    is_flashing = fill(false, w, h)
    s_old, s_new = -1, sum(is_flashing)
    while s_old != s_new
        for i = 1:h
            for j = 1:w
                if mat[i, j] > 9 && !is_flashing[i, j]
                    y_min = max(1, j - 1)
                    y_max = min(w, j + 1)
                    x_min = max(1, i - 1)
                    x_max = min(h, i + 1)
                    mat[x_min:x_max, y_min:y_max] .+= 1

                    is_flashing[i, j] = true
                end
            end
        end
        s_old = s_new
        s_new = sum(is_flashing)
    end

    return mat, is_flashing
end

function part1(mat::Matrix{Int}; steps::Int = 100)::Int
    n_flashes = 0
    mat = deepcopy(mat)
    for _ in 1:steps
        mat .+= 1
        
        mat, _ = flash(mat)

        n_flashes += sum(mat .> 9)
        mat[mat .> 9] .= 0
    end

    return n_flashes
end

function part2(mat::Matrix{Int})::Int
    mat = deepcopy(mat)
    i = 1
    while true
        mat .+= 1
        
        mat, is_flashing = flash(mat)

        if all(is_flashing)
            return i
        end

        mat[mat .> 9] .= 0
        i += 1
    end
end

mat = readInput("input.txt")
# print_matrix(mat)

println(part1(mat, steps=100))
println(part2(mat))
