#!/bin/bash

# Input parameters
NGINX_ADDR="$1"
MEDIA_ADDR="$2"
INTENSITY_FILE="$3"
COMP_OPT="$4"
LOCUST_DIR="$5"
shift 5
IP_ADDRESSES=("$@")
echo $IP_ADDRESSES
# Path to the Locust script on the remote machines
LOCUST_SCRIPT_PATH="$LOCUST_DIR/locustfile-custom-scale.py"
REMOTE_CMD="cd $LOCUST_DIR; source venv/bin/activate; env NGINX_ADDR=$NGINX_ADDR MEDIA_ADDR=$MEDIA_ADDR INTENSITY_FILE=$INTENSITY_FILE COMP_OPT=$COMP_OPT locust -f $LOCUST_SCRIPT_PATH --headless --csv=log --csv-full-history"

# Function to run Locust script on a single host
run_locust_on_host() {
    local ip="$1"
    echo "Connecting to $ip..."

    ssh -o StrictHostKeyChecking=no "$ip" "$REMOTE_CMD" > "output_$ip.log" 2>&1 &

    if [ $? -eq 0 ]; then
        echo "Locust script running on $ip"
    else
        echo "Failed to run Locust script on $ip"
    fi
}

# Export the function so it can be used by parallel execution
export -f run_locust_on_host
export REMOTE_CMD

# Run Locust script on all IP addresses in parallel
for ip in "${IP_ADDRESSES[@]}"; do
    run_locust_on_host "$ip"
done

# Wait for all background jobs to finish
wait

echo "All Locust scripts have been executed."
