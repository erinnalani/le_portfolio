#!/bin/sh
grammar_file=$1
sentences=$2
output_file=$3

source ~/miniconda3/bin/activate "/mnt/dropbox/23-24/WIN571/envs/571"
python cky2.py "$grammar_file" "$sentences" "$output_file"