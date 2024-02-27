#!/bin/sh
input_d=$1
output_d=$2
output_seq=$3

source ~/miniconda3/bin/activate "/mnt/dropbox/23-24/WIN571/envs/571"
python oracle.py "$input_d" "$output_d" "$output_seq"
