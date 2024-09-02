#!/bin/bash

export PATH="$HOME/.local/bin:$PATH"

target="localhost"

#nb_thread=32

#workload_dir="../Load/profiles_$workload_date"
workload_dir="../Load/profiles_2024-07-31"

#pwd

#workload_files=($(ls "$workload_dir"/*.csv))

java -jar httploadgenerator.jar director -s $target -a "../Load/profiles_2024-07-16/constants/temp/constant_10requests_per_sec.csv" -l "./teastore_browse.lua" -o "temp_test_jaeger.csv"


