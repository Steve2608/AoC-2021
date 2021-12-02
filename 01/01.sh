expr $(awk 'prev < $0 {print} {prev=$0}' input.txt | wc -l) - 1
expr $(awk 'prev3 < $0 {print} {prev3=prev2; prev2=prev1; prev1=$0}' input.txt | wc -l) - 3