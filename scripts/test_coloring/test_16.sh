#!/bin/bash
for i in $(eval echo {$1..$2});
do
   ./test_col 16_5_3#$i.g6 > uncol$i.g6
done