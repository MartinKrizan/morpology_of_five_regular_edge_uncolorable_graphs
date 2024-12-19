#!/bin/bash
for i in $(eval echo {$1..$2});

do
   ./../../../tools/genreg/genreg 16 5 -g -c -m $i 100
done