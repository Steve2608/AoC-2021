using ArgParse

function readInput(filename::String)
    open(filename) do file
        data = read(file, String)
        line, image = map(strip, split(data, "\n\n"))
        line = map(x -> x == "#", split(line, ""))
    
        rows = split(image, "\n")
        matrix = falses(length(rows), length(rows))
        for (i, row) in enumerate(rows)
            matrix[i, :] = map(x -> x == "#", split(row, ""))
        end

        return line, matrix
    end
end

function step(line, image, pad_value; pad=2)
    function pad_false(image, pad)
        image_padded = falses(size(image) .+ pad*2)
        image_padded[1+pad:end-pad, 1+pad:end-pad] .= image
        return image_padded
    end
    
    function pad_true(image, pad)
        image_padded = trues(size(image) .+ pad*2)
        image_padded[1+pad:end-pad, 1+pad:end-pad] .= image
        return image_padded
    end

    image_padded = pad_value ? pad_true(image, pad) : pad_false(image, pad)
    image_next = pad_value != line[1] ? trues(size(image_padded)) : falses(size(image_padded))

    kernel = 1 .<< (8:-1:0)
    for x in 2:size(image_next, 1) - 1
        for y in 2:size(image_next, 2) - 1
            view = image_padded[x - 1:x + 1, y - 1:y + 1]
            # row first
            index = sum(kernel .* vec(transpose(view)))
            image_next[x, y] = line[1 + index]
        end
    end

    # keep image size as small as possible
    pivot = image_next[1, 1]
    while all(image_next[pad + 1, :] .== pivot) && all(image_next[end-pad, :] .== pivot) && 
        all(image_next[:, pad + 1] .== pivot) && all(image_next[:, end-pad] .== pivot)
        image_next = image_next[2:end-1, 2:end-1]
    end

    return image_next
end

function multiple_steps(line, image; steps::Int, pad_odd::Bool = false, pad_even::Bool = false)
    for i in 1:steps
        image = step(line, image, i % 2 == 1 ? pad_odd : pad_even)
    end
    return image, sum(image)
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
if args["example"]
    line, image = readInput("example.txt");

    image2, sum_image2 = multiple_steps(line, image, steps=2);
    @assert sum_image2 == 35;

    image50, sum_image50 = multiple_steps(line, image2, steps=48);
    @assert sum_image50 == 3351;
end

line, image = readInput("input.txt");

image2, sum_image2 = multiple_steps(line, image, steps=2, pad_even=true);
println(sum_image2);

image50, sum_image50 = multiple_steps(line, image2, steps=48, pad_even=true);
println(sum_image50);

# using BenchmarkTools
# @btime multiple_steps(line, image, steps=50, pad_even=true);