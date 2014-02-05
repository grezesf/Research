#!/bin/sh

set -x

#part 4.3 of the paper.

datadir=/home/felix/reservoirs/datasets/oger-dev/ 
echo "weights optimization"
python weights_param.py $datadir