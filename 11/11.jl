using Base.Iterators
using LinearAlgebra

function readInput(filename::String)::Matrix{Int}
    open(filename) do file
        return transpose(hcat([parse.(Int, split(line, "")) for line in readlines(file)]...))
    end
end

function flash(mat::Matrix{Int}, flashing_at::Int)::Tuple{Matrix{Int}, Matrix{Bool}}
    w, h = size(mat)
    is_flashing = falses(size(mat))
    s_old, s_new = -1, sum(is_flashing)
    while s_old != s_new
        for i = 1:h
            for j = 1:w
                if mat[i, j] > flashing_at && !is_flashing[i, j]
                    y_min = max(1, j - 1)
                    y_max = min(w, j + 1)
                    x_min = max(1, i - 1)
                    x_max = min(h, i + 1)
                    mat[x_min:x_max, y_min:y_max] .+= 1

                    is_flashing[i, j] = true
                end
            end
        end
        s_old, s_new = s_new, sum(is_flashing)
    end

    return mat, is_flashing
end

function part1(mat::Matrix{Int}; steps::Int = 100, flashing_at::Int = 9)::Int
    n_flashes = 0
    for _ in 1:steps
        mat, _ = flash(mat .+ 1, flashing_at)
        n_flashes += sum(mat .> flashing_at)
        mat[mat .> flashing_at] .= 0
    end
		
    return n_flashes
end

function part2(mat::Matrix{Int}; flashing_at::Int = 9)::Int
    for i in countfrom(1)
        mat, is_flashing = flash(mat .+ 1, flashing_at)
        if all(is_flashing)
            return i
        end

        mat[mat .> flashing_at] .= 0
    end
end

mat = readInput("input.txt")

println(part1(mat, steps=100))
println(part2(mat))