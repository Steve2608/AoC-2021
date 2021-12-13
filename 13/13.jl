using LinearAlgebra

function readInput(filename::String)
	x::Vector{Int} = []
    y::Vector{Int} = []
    folds::Vector{Tuple{String, Int}} = []
    open(filename) do file
        for line in readlines(file)
            if isempty(line)
                continue
            end

            if occursin(",", line)
                x_line, y_line = parse.(Int, split(line, ","))
                push!(x, x_line)
                push!(y, y_line)
            else
                if occursin("x", line)
                    x_ = parse.(Int, line[length("fold along x=") + 1:end])
                    push!(folds, ("x", x_))
                else
                    y_ = parse.(Int, line[length("fold along y=") + 1:end])
                    push!(folds, ("y", y_))
                end
            end
        end
    end
    max_x = maximum(x) + 1
    max_y = maximum(y) + 1
    m = falses(max_x, max_y)

    for (xᵢ, yᵢ) in zip(x, y)
        m[xᵢ + 1, yᵢ + 1] = true
    end

    return BitMatrix(transpose(m)), folds
end

function print_matrix(mat)
    show(stdout, "text/plain", mat)
    println()
end

function fold_y(mat, y::Int)
    r = size(mat, 1)
    top_half = mat[1:y, :]
    bot_half = mat[y+2:end, :]
    if y + 1 > r / 2
        top_half[end-size(bot_half, 1)+1:end, :] .|= reverse(bot_half, dims=1)
        return top_half
    else
        bot_half[end-size(top_half, 1)+1:end, :] .|= reverse(top_half, dims=1)
        return reverse(bot_half, dims=1)
    end
end

function fold_x(mat, x::Int)
    c = size(mat, 2)
    left_half = mat[:, 1:x]
    rigt_half = mat[:, x+2:end]
    if x + 1 > c / 2
        left_half[:, end-size(rigt_half, 2)+1:end] .|= reverse(rigt_half, dims=2)
        return left_half
    else
        rigt_half[:, end-size(left_half, 2)+1:end] .|= reverse(left_half, dims=2)
        return reverse(rigt_half, dims=2)
    end
end

function part1(mat, folds)::Int
    dir, n = folds[1]
    if dir == "x"
        return sum(fold_x(mat, n))
    else
        return sum(fold_y(mat, n))
    end
end

function part2(mat, folds)
    for (dir, n) in folds
        if dir == "x"
            mat = fold_x(mat, n)
        else
            mat = fold_y(mat, n)
        end
    end
    
    return mat
end

mat, folds = readInput("input.txt")

println(part1(mat, folds))
print_matrix(part2(mat, folds))