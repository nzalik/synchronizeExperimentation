#/!/bin/bash

dir=$(pwd)
gen_d="${dir}/workload_generators"
fetch_d="${dir}/metric_fetcher"

############################################# TeaStore single load generator ##########################################################
teastore_load_generator() {
	duration=$1
	time_step=$2
	webui_addr=$3
	prometheus_url=$4
	namespace=$5
	intensity=$6
	node_ip=$7

	sed_str="s/http:\/\/.*\/t/http:\/\/${webui_addr}\/t/"

	echo "TeaStore Workload Generation"
	data_dir="$dir/data/teastore/"
	if [ ! -d "$data_dir" ]; then
		mkdir $data_dir
	fi

	#for REQUEST in teastore_browse teastore_buy; do
	for REQUEST in teastore_browse; do
		sed -i "$sed_str" $gen_d/httploadgenerator/$REQUEST.lua

		for i in $(ls $gen_d/httploadgenerator/intensity_profiles/); do 
		#for i in $(ls $gen_d/load-profiles/alibaba_loads_lower/*.csv); do 
			INTENSITY=$( basename ${i%.*} )
			begin_t=$(date +%s)
			end_t=$(date -d "+${duration} minutes" +%s)
			now_t=$(date +%s)

			echo "----- Starting workload $REQUEST with intensity $INTENSITY for $duration minutes -----"
			while [ $begin_t -le $now_t -a $now_t -le $end_t  ]; do
				outfile="../out_${REQUEST}_${INTENSITY}_${now_t}"
				java -jar $gen_d/httploadgenerator/httploadgenerator.jar loadgenerator &
				#java -jar $gen_d/httploadgenerator/httploadgenerator.jar director -s localhost -a $gen_d/httploadgenerator/intensity_profiles/$i -l $gen_d/httploadgenerator/$REQUEST.lua -o $outfile.csv -t 256
				java -jar $gen_d/httploadgenerator/httploadgenerator.jar director -s localhost -a $i -l $gen_d/httploadgenerator/$REQUEST.lua -o $outfile.csv -t 256
				kill $(pidof java)
				sleep 5
				now_t=$(date +%s)

			done
			echo "Fetching metrics..."
			python3 $fetch_d/prometheus_fetch.py $prometheus_url \
				-N "teastore" -d "$data_dir" -p "node_dist_1/hw_spec_2/pod_spec_0/$REQUEST/$INTENSITY/" \
				-t $duration -s $time_step -c $fetch_d/metrics.ini -n $namespace
			#python3 $fetch_d/prometheus_fetch.py $prometheus_url \
			#	-N "teastore" -d "$data_dir" -p "anom_1/node_dist_1/hw_spec_2/pod_spec_0/$REQUEST/$INTENSITY/" \
			#	-t $duration -s $time_step -c $fetch_d/metrics.ini -n $namespace

		done
	done
#CLEANUP: kubectl delete all --all
}
#######################################################################################################################################

############################################### TeaStore double load generator ########################################################
teastore_double_load_generator() {
	duration=$1
	time_step=$2
	webui_addr=$3
	prometheus_url=$4
	namespace=$5
	generator_one_ip=$6
	generator_two_ip=$7
	intensity=$8
	
	sed_str="s/http:\/\/.*\/t/http:\/\/${webui_addr}\/t/"

	echo "TeaStore Workload Generation"

	#for REQUEST in teastore_browse teastore_buy; do
	for REQUEST in teastore_browse; do
		sed -i "$sed_str" $gen_d/httploadgenerator/$REQUEST.lua

		for i in intesity_profiles/*.csv; do 
			INTENSITY=$( basename ${i%.*} ) 
			begin_t=$(date +%s)
			end_t=$(date -d "+${duration} minutes" +%s)
			now_t=$(date +%s)
			
			echo "----- Starting workload $REQUEST with intensity $INTENSITY for $duration minutes -----"
			while [ $begin_t -le $now_t -a $now_t -le $end_t  ]; do
				outfile="out_${REQUEST}_${INTENSITY}_${now_t}"
				ssh $generator_one_ip "sh -c '( ( nohup java -jar $gen_d/httploadgenerator/httploadgenerator.jar loadgenerator ) & )'"
				ssh $generator_two_ip "sh -c '( ( nohup java -jar $gen_d/httploadgenerator/httploadgenerator.jar loadgenerator ) & )'"
				java -jar $gen_d/httploadgenerator/httploadgenerator.jar director -s $generator_one_ip,$generator_two_ip -a $gen_d/httploadgenerator/$INTENSITY.csv -l $gen_d/httploadgenerator/$REQUEST.lua -o $outfile.csv -t 256
				ssh $generator_one_ip 'kill $(pidof java)'
				ssh $generator_two_ip 'kill $(pidof java)'
				sleep 5
				now_t=$(date +%s)

			done
			python3 $fetch_d/prometheus_fetch.py $prometheus_url -N "double_${REQUEST}_${INTENSITY}" -t $duration -s $time_step -c $fetch_d/metrics.ini
		done
	done
#CLEANUP: kubectl delete all --all
}
#######################################################################################################################################

######################################## DeathStarBench's Social Network load generator ###############################################
socialnetwork_load_generator() {
	duration=$1
	time_step=$2
	webui_addr=$3
	media_addr=$4
	prometheus_url=$5
	namespace=$6
	ip_port_split=(${3//:/ })
	duration_s=$((60*duration))
	
	shift 6
	generators="$@"

	data_dir="$dir/data/socialnetwork/"
	if [ ! -d "$data_dir" ]; then
		mkdir -p $data_dir
	fi

	echo "DeathStarBench's Social Network Workload Generation"
	cd $gen_d/locust
	source venv/bin/activate
	
	python3 warmup.py --addr=$webui_addr
	#for REQUEST in 'composePost' 'readHomeTimeline' 'readUserTimeline' 'mixed' 'std_comp'; do
	for REQUEST in 'std_comp' ; do

		#for i in $(ls intensity_profiles/*.csv); do 
		for i in $(ls ../load-profiles/alibaba_loads/*.csv); do 
			INTENSITY=$( basename ${i%.*} ) 
			begin_t=$(date +%s)
			end_t=$(date -d "+${duration} minutes" +%s)
			now_t=$(date +%s)

			while [ $begin_t -le $now_t -a $now_t -le $end_t  ]; do

				# Generate http requests based on API Composition
				echo "----- Starting workload $REQUEST with intensity $INTENSITY for $duration minutes -----"
				#env NGINX_ADDR=$webui_addr MEDIA_ADDR=$media_addr INTENSITY_FILE=$i COMP_OPT=$REQUEST locust -f locustfile-custom-scale.py --headless --csv=log --csv-full-history 
				timeout -k 10 "$(($duration+1))"m ./run_locust_parallel.sh $webui_addr $media_addr $i $REQUEST $gen_d/locust $generators
				python3 $fetch_d/prometheus_fetch.py $prometheus_url \
					-N "socialnetwork_${REQUEST}_${INTENSITY}" -d "$data_dir" -p "node_dist_1/hw_spec_1/pod_spec_1/$REQUEST/$INTENSITY/" \
					-t $duration -s $time_step -c $fetch_d/metrics.ini -n $namespace

				mkdir -p $data_dir/locust-logs-test-test/$REQUEST/$INTENSITY/
				mv $gen_d/locust/log_* 	$data_dir/locust-logs-test-test/$REQUEST/$INTENSITY/
				mv $gen_d/locust/*.log 	$data_dir/locust-logs-test-test/$REQUEST/$INTENSITY/

				sleep 35
				now_t=$(date +%s)
	
			done
		done
	done
	cd $dir
}
#####################################################################################################################################

################################## DeathStarBench's Hotel Reservation load generator ################################################
hotelreservation_load_generator() {
	duration_h=$1
	time_step=$2
	webui_addr=$3
	prometheus_url=$4
	duration_s=$((60*60*duration_h))

	echo "DeathStarBench's Hotel Reservation Workload Generation"

	casts_path="$dir/media-microservices/casts.json"
	movies_path="$dir/media-microservices/movies.json"
	python3 $dir/media-microservices/write_movie_info.py -c $casts_path -m $movies_path --server_address $webui_addr && $dir/media-microservices/register_users.sh 	&& $dir/media-microservices/register_movies.sh

	cd $gen_d/wrk2
	make
	cd ..

	for INTENSITY in 10 50 100; do

		# Compose Review
		echo "----- Starting workload mediamicroservices_compose_review with intensity $INTENSITY for $duration_h hours -----"
		./wrk2/wrk -D exp -t 4 -c 4 -d $duration_s -L -s ./wrk2/scripts/media-microservices/compose-review.lua \ 
			"$webui_addr/wrk2-api/review/compose" -R $INTENSITY
		python3 $fetch_d/prometheus_fetch.py $prometheus_url -N "mediamicroservices_compose_review_${INTENSITY}" -t $duration_h -s $time_step -c $fetch_d/metrics.ini
	
	done

	cd $gen_d/wrk2
	make clean
	cd $dir
}
#####################################################################################################################################

##################################### DeathStarBench's Media Service load generator #################################################
mediaservice_load_generator() {	
	echo "DeathStarBench's Media Service Workload Generation"
}
#####################################################################################################################################

############################################## TrainTicket load generator ###########################################################
trainticket_load_generator() {
	echo "TrainTicket Workload Generation"
}
#####################################################################################################################################

