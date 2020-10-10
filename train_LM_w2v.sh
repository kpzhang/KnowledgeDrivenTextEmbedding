#!/bin/sh
gcc LM-w2v.c -o LM-w2v -lm -pthread -O2 -Wall -funroll-loops -Wno-unused-result

for i in 0 1 2 3 4 5 6 7 8 9
do
for year in 2012 2013 2014 2015 2016 2017
do
echo "${i}-th iter for val year ${year}"
./LM-w2v -size 200 -train ../data/${year}trainEmbed.txt -label labels_LM_binary.txt -read-vocab vocab_${year}.txt -debug 2 -lambda 4e-4 -output LM_${year}_${i}.txt -window 5 -sample 1e-4 -hs 0 -negative 5 -constraints 32 -beta-m 1 -beta-c 1 -threads 5 -epochs 1
done
done
