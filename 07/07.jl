function readInput(filename::String)::Vector{Int}
	open(filename) do file
		return parse.(Int, split(readline(file), ","))
	end
end

function centroid(vec::Vector{<:Real}; weight_fun::Function)::Int
	min_ = typemax(Int)
	for i in minimum(vec):maximum(vec)
		min_ = min(min_, sum(weight_fun.(abs.(vec .- i))))
	end
	return min_
end

part1(vec) = centroid(vec, weight_fun=n -> n)
part2(vec) = centroid(vec, weight_fun=n -> sum(1:n))

vec = readInput("input.txt")
println(part1(vec))
println(part2(vec))
