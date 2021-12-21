using Base.Iterators
using DataStructures
using ArgParse

function readInput(filename::String)
    regex = r"Player (\d+) starting position: (\d+)"
    player1, value1 = -1, -1
    player2, value2 = -1, -1

    open(filename) do file
        for line in readlines(file)
            m = match(regex, line)
            if m[1] == "1"
                player1, value1 = parse.(Int, (m[1], m[2]))
            else
                player2, value2 = parse.(Int, (m[1], m[2]))
            end
        end
    end
    return (player1, value1), (player2, value2)
end

function playGame(p1, p2; winning_score::Int = 1000)
    roll_dice(offset::Int) = sum(((offset:offset+2) .- 1) .% 100 .+ 1)
    
    p1, p2 = p1 - 1, p2 - 1
    s1, s2, dice_i = 0, 0, 0
    for i in countfrom(1)
        if i % 2 == 1
            p1 = (p1 + roll_dice(dice_i + 1)) % 10
            s1 += p1 + 1

            s1 >= winning_score && return i * s2 *3
        else
            p2 = (p2 + roll_dice(dice_i + 1)) % 10
            s2 += p2 + 1

            s2 >= winning_score && return i * s1 * 3
        end

        dice_i = (dice_i + 3) % 100
    end
end


function dirac_game(p1, p2; winning_score::Int=21)
    s1, p1 = 0, p1 - 1
    s2, p2 = 0, p2 - 1
    wins = [0, 0]

    three_dice = vec(sum.(collect(product(1:3, 1:3, 1:3))))
    
    prev_step = Dict{Tuple{Int, Int, Int, Int}, Int}((p1, s1, p2, s2) => 1)
    turn = true
    while length(prev_step) != 0
        next_step = DefaultDict{Tuple{Int, Int, Int, Int}, Int}(0)
        for k in keys(prev_step)
            v = prev_step[k]
            p1, s1, p2, s2 = k

            for dice in three_dice
                if turn
                    s1_ = s1 + (p1 + dice) % 10 + 1
                    if s1_ >= winning_score
                        wins[1] += v
                    else
                        p1_ = (p1 + dice) % 10
                        next_step[(p1_, s1_, p2, s2)] += v
                    end
                else
                    s2_ = s2 + (p2 + dice) % 10 + 1
                    if s2_ >= winning_score
                        wins[2] += v
                    else
                        p2_ = (p2 + dice) % 10
                        next_step[(p1, s1, p2_, s2_)] += v
                    end
                end
            end
        end
        turn = !turn
        prev_step = next_step
    end
    return maximum(wins)
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
    (_, p1), (_, p2) = readInput("example.txt")
    
    score = playGame(p1, p2)
    @assert score == 739785

    w = dirac_game(p1, p2)
    @assert w == 444356092776315
end

(_, p1), (_, p2) = readInput("input.txt")
score = playGame(p1, p2)
w = dirac_game(p1, p2)

println(score)
println(w)