using LinearAlgebra

function readInput(filename::String)::Matrix{Int}
	open(filename) do file
		return transpose(hcat([parse.(Int, split(line, "")) for line in readlines(file)]...))
	end
end

function find_low_points(mat::Matrix{Int})::Set{Tuple{Int, Int}}
	lows = Set{Tuple{Int, Int}}()
	h, w = size(mat)
	for i = 1:h
		for j = 1:w
			val = mat[i, j]
			
			if (i <= 1 || val < mat[i - 1, j]) &&
				(i >= h || val < mat[i + 1, j]) && 
				(j <= 1 || val < mat[i, j - 1]) &&
				(j >= w || val < mat[i, j + 1])
				push!(lows, (i, j))
			end
		end
	end
	return lows
end

part1(mat::Matrix{Int})::Int = sum(mat[i, j] + 1 for (i, j) in find_low_points(mat))

function part2(mat::Matrix{Int})::Int
	basins = []
	for (i, j) in find_low_points(mat)
		seen = Set{Tuple{Int, Int}}()
		expand_basin_dfs(mat, seen, i, j)
		push!(basins, length(seen))
	end
	
	return prod(sort(basins, rev=true)[1:3])
end

function expand_basin_dfs(mat::Matrix{Int}, seen::Set{Tuple{Int, Int}}, i::Int, j::Int)
	if ((i, j) in seen || mat[i, j] == 9)
		return
	end
	
	push!(seen, (i, j))
	if (i > 1 && mat[i, j] < mat[i - 1, j])
		expand_basin_dfs(mat, seen, i - 1, j)
	end
	
	if (i < size(mat, 1) && mat[i, j] < mat[i + 1, j])
		expand_basin_dfs(mat, seen, i + 1, j)
	end
	
	if (j > 1 && mat[i, j] < mat[i, j - 1])
		expand_basin_dfs(mat, seen, i, j - 1)
	end
	
	if (j < size(mat, 2) && mat[i, j] < mat[i, j + 1])
		expand_basin_dfs(mat, seen, i, j + 1)
	end
end

mat = readInput("input.txt")

println(part1(mat))
println(part2(mat))