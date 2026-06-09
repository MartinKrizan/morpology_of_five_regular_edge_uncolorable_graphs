#!/usr/bin/env bash

INPUT="all_12v_m2.txt"

for start in $(seq 1 1000000 17000001); do
    end=$((start + 999999))

    out_start=$(( (start - 1) / 1000000 ))
    out_end=$(( out_start + 1 ))

    (
        echo "Processing lines ${start}-${end}..."

        sed -n "${start},${end}p;${end}q" "$INPUT" \
            | filter-uncol \
            > "uncol_12_m2_${out_start}-${out_end}M.txt"

        echo "Finished ${start}-${end}"
    ) &
done

wait
echo "All jobs completed."
