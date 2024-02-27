#!/bin/sh
input_grammar=$1
input_sent=$2
output_f=$3

# source ~/miniconda3/bin/activate "/mnt/dropbox/23-24/WIN571/envs/571"
/mnt/dropbox/23-24/WIN571/envs/571/python semantics.py "$input_grammar" "$input_sent" "$output_f"

