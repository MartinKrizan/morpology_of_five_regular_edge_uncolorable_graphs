#!/bin/bash

for file in ../../data/benchmark/*; do
    if [ -f "$file" ]; then
        echo ""
        echo "Processing $file"
        python benchmark_edge_colorability.py --source "$file"
    fi
done