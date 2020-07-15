#!/bin/bash
for i in {1..1000}
do
python3 pokemonsim.py > silent_output.txt
done
echo "done-----"