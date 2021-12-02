awk '/forward/ {x += $2} /up/ {y -= $2} /down/ {y += $2} END {print (x * y)}' input.txt
awk '/forward/ {x += $2; y += $2 * aim} /up/ {aim -= $2} /down/ {aim += $2} END {print (x * y)}' input.txt