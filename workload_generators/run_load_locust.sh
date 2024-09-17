# shellcheck disable=SC2045
#/!/bin/bash

for i in ../Load/profiles_2024-07-31/*.csv; do
#for i in $(ls ../Load/profiles_2024-07-31/*.csv); do
			INTENSITY=$( basename ${i%.*} )
			begin_t=$(date +%s)
			end_t=$(date -d "+${duration} minutes" +%s)
			now_t=$(date +%s)

			echo "----- Starting workload with intensity $INTENSITY for $duration minutes -----"

			#locust -f teastore_locustfile-custom-scale.py --headless

			env INTENSITY_FILE=$i locust -f ./locust/teastore_locustfile-custom-scale.py --headless --csv=log --csv-full-history


			#while [ $begin_t -le $now_t -a $now_t -le $end_t  ]; do

				# Generate http requests based on API Composition

				#env NGINX_ADDR=$webui_addr MEDIA_ADDR=$media_addr INTENSITY_FILE=$i COMP_OPT=$REQUEST locust -f locustfile-custom-scale.py --headless --csv=log --csv-full-history
#				timeout -k 10 "$(($duration+1))"m ./run_locust_parallel.sh $webui_addr $media_addr $i $REQUEST $gen_d/locust $generators
#				python3 $fetch_d/prometheus_fetch.py $prometheus_url \
#					-N "socialnetwork_${REQUEST}_${INTENSITY}" -d "$data_dir" -p "node_dist_1/hw_spec_1/pod_spec_1/$REQUEST/$INTENSITY/" \
#					-t $duration -s $time_step -c $fetch_d/metrics.ini -n $namespace
#
#				mkdir -p $data_dir/locust-logs-test-test/$REQUEST/$INTENSITY/
#				mv $gen_d/locust/log_* 	$data_dir/locust-logs-test-test/$REQUEST/$INTENSITY/
#				mv $gen_d/locust/*.log 	$data_dir/locust-logs-test-test/$REQUEST/$INTENSITY/
#
#				sleep 35
#				now_t=$(date +%s)

			#done
		done