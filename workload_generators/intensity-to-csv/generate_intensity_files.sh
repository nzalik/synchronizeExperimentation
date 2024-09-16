#!/bin/bash

duration=300
max_req=1000
min_req=300
nb_files_per_func=8
nb_f_offset=17

touch csv_gen.out

# Sin profiles
echo "- Sin files" >> csv_gen.out
for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
	rand_floor=$((RANDOM % (rand_ceil - min_req + 1) + min_req))
	peaks=$((RANDOM % 3 + 1))
	python3 gen_load_intensity_csv.py -f "intensity_profiles/si_sin_$i.csv" -g sin -t $duration --ceil $rand_ceil --floor $rand_floor -p $peaks -n
	echo "sin_$i: ceil=$rand_ceil | floor=$rand_floor | peaks=$peaks" >> csv_gen.out
done

# Cos profiles
#echo "- Cos files" >> csv_gen.out
#for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
#	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
#	rand_floor=$((RANDOM % (rand_ceil - min_req + 1) + min_req))
#	peaks=$((RANDOM % 3 + 1))
#	python3 gen_load_intensity_csv.py -f "intensity_profiles/si_cos_$i.csv" -g cos -t $duration --ceil $rand_ceil --floor $rand_floor -p $peaks -n
#	echo "cos_$i: ceil=$rand_ceil | floor=$rand_floor | peaks=$peaks" >> csv_gen.out
#done

# AbsSin profiles
#echo "- AbsSin files" >> csv_gen.out
#for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
#	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
#	rand_floor=$((RANDOM % (rand_ceil - min_req + 1) + min_req))
#	peaks=$((RANDOM % 3 + 1))
#	python3 gen_load_intensity_csv.py -f "intensity_profiles/si_abssin_$i.csv" -g abssin -t $duration --ceil $rand_ceil --floor $rand_floor -p $peaks -n
#	echo "abssin_$i: ceil=$rand_ceil | floor=$rand_floor | peaks=$peaks" >> csv_gen.out
#done

# AbsCos profiles
#echo "- AbsCos files" >> csv_gen.out
#for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
#	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
#	rand_floor=$((RANDOM % (rand_ceil - min_req + 1) + min_req))
#	peaks=$((RANDOM % 3 + 1))
#	python3 gen_load_intensity_csv.py -f "intensity_profiles/si_abscos_$i.csv" -g abscos -t $duration --ceil $rand_ceil --floor $rand_floor -p $peaks -n
#	echo "abscos_$i: ceil=$rand_ceil | floor=$rand_floor | peaks=$peaks" >> csv_gen.out
#done

# Log profiles
#echo "- Log files" >> csv_gen.out
#for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
#	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
#	rand_floor=$((RANDOM % (rand_ceil - min_req + 1) + min_req))
#	multiplier=$((RANDOM % 21 - 10))
#	python3 gen_load_intensity_csv.py -f "intensity_profiles/si_log_$i.csv" -g log -t $duration --ceil $rand_ceil --floor $rand_floor -a $multiplier -n
#	echo "log_$i: ceil=$rand_ceil | floor=$rand_floor | a=$multiplier" >> csv_gen.out
#done
# Bell profiles
#echo "- Bell files" >> csv_gen.out
#for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
#	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
#	rand_floor=$((RANDOM % (rand_ceil - min_req + 1) + min_req))
#	python3 gen_load_intensity_csv.py -f "intensity_profiles/rd_bell_$i.csv" -g bell -t $duration --ceil $rand_ceil --floor $rand_floor
#	echo "bell_$i: ceil=$rand_ceil | floor=$rand_floor" >> csv_gen.out
#done

# Random Stairs profiles
echo "- Random Stairs files" >> csv_gen.out
for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
	python3 gen_load_intensity_csv.py -f "intensity_profiles/rd_stairs_$i.csv" -g rdstairs -t $duration --ceil $rand_ceil --floor $min_req 
	echo "rdstairs_$i: ceil=$rand_ceil | floor=$min_req" >> csv_gen.out
done

# Random Jump profiles
echo "- Random Jump files" >> csv_gen.out
for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
	python3 gen_load_intensity_csv.py -f "intensity_profiles/rd_jump_$i.csv" -g rdjump -t $duration --ceil $rand_ceil --floor $min_req 
	echo "rdjump_$i: ceil=$rand_ceil | floor=$min_req" >> csv_gen.out
done


# Const profiles
#echo "- Const files" >> csv_gen.out
#for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
#	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
#	python3 gen_load_intensity_csv.py -f "intensity_profiles/li_const_$i.csv" -g const -t $duration --ceil $rand_ceil
#	echo "const_$i: ceil=$rand_ceil" >> csv_gen.out
#done

# Linear profiles
echo "- Linear files" >> csv_gen.out
for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
	rand_floor=$((RANDOM % (rand_ceil - min_req + 1) + min_req))
	inclination=$((RANDOM % 3 + 1))
	python3 gen_load_intensity_csv.py -f "intensity_profiles/li_linear_$i.csv" -g linear -t $duration --ceil $rand_ceil --floor $rand_floor -a $inclination -n
	echo "linear_$i: ceil=$rand_ceil | floor=$rand_floor | a=$inclination" >> csv_gen.out
done

# Stairs Up profiles
echo "- Stairs Up files" >> csv_gen.out
for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
	python3 gen_load_intensity_csv.py -f "intensity_profiles/li_stairsu_$i.csv" -g stairsu -t $duration --ceil $rand_ceil --floor $min_req 
	echo "stairsu_$i: ceil=$rand_ceil | floor=$min_req" >> csv_gen.out
done

# Stairs Down profiles
echo "- Stairs Down files" >> csv_gen.out
for ((i=nb_f_offset; i<nb_files_per_func+nb_f_offset; i++));do
	rand_ceil=$((RANDOM % (max_req - min_req + 1) + min_req))
	python3 gen_load_intensity_csv.py -f "intensity_profiles/li_stairsd_$i.csv" -g stairsd -t $duration --ceil $rand_ceil --floor $min_req 
	echo "stairsd_$i: ceil=$rand_ceil | floor=$min_req" >> csv_gen.out
done







