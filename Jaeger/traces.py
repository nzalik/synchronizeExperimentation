from argparse import ArgumentParser
from json import dump, loads
from math import floor
from os import makedirs
from os.path import join, exists
from requests import get

# Jaeger Query API endpoint
JAEGER_API_URL_t = "http://{}/api/traces"


def open_json(filepath):
    with open(filepath, "r") as trace_file:
        x = trace_file.read()
    return loads(x)

def get_traces(jaeger_url, start_time, end_time, limit=150000):
    # Define the query parameters
    params = {
        "service": 'nginx-web-server',
        "limit": limit,
        "start": start_time,
        "end": end_time,
    }

    # Make a GET request to the Jaeger API
    response = get(jaeger_url, params=params)
    print(f"Requested traces from: {response.request.url}")

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve traces: {response.status_code}")
        return None
    
def count_requests_per_second(traces, extract_first_level=True):
    # Dictionary to hold the count of requests per second for each operation
    requests_per_second = {}
    start_time = int(traces["start_time"]/1e6)
    end_time = start_time + 300
    # end_time = int(traces["end_time"]/1e6)
    # start_time = traces["start_time"]
    # end_time = traces["end_time"]
    for trace in traces["data"]:
        for span in trace["spans"]:
            if not extract_first_level or not span["references"]:
                operation_name = span['operationName']
                start_time_unix = span['startTime'] / 1e6  # assuming startTime is in microseconds
                time_key = floor(start_time_unix)

                if requests_per_second.get(operation_name, None) is None:
                    requests_per_second[operation_name] = {}
                
                if time_key < end_time and time_key > start_time - 1:
                    if requests_per_second[operation_name].get(time_key, None) is None:
                        requests_per_second[operation_name][time_key] = 0

                    requests_per_second[operation_name][time_key] += 1

    # Sort each operation's timestamps
    sorted_requests_per_second = {}
    for operation_name, timestamps in requests_per_second.items():
        sorted_requests_per_second[operation_name] = dict(sorted(timestamps.items()))

    return sorted_requests_per_second

def store_traces(sorted_request_type_traces, data_directory, intensity):
    # Check if directory exists, create if not
    data_dir = f'{data_directory}/traces_directory2'
    if not exists(data_dir):
        makedirs(data_dir)

    for operation_name in sorted_request_type_traces.keys():
        file_name = f"{intensity}_{operation_name.replace('/', '_')}.json"
        file_path = join(data_dir, file_name)
        with open(file_path, 'w') as outfile:
            dump(sorted_request_type_traces[operation_name], outfile)
    


def main():
    # Parse command-line arguments
    parser = ArgumentParser(description='Retrieve Jaeger traces for a given service.')
    parser.add_argument('jaeger_IP', help='Jaeger IP with port')
    parser.add_argument('start_time', type=int, help='Start time in microseconds since epoch')
    parser.add_argument('end_time', type=int, help='End time in microseconds since epoch')
    parser.add_argument('output_directory', type=str, help='Output path directory for traces')
    parser.add_argument('workload_intensity', type=str, help='Name of the workload intensity file')

    args = parser.parse_args()

    # Assign arguments to variables
    jaeger_url = JAEGER_API_URL_t.format(args.jaeger_IP)
    start_time = args.start_time
    end_time = args.end_time
    data_dir = args.output_directory
    intensity = args.workload_intensity

    traces = get_traces(jaeger_url, start_time, end_time)
    traces["start_time"] = int(start_time)
    traces["end_time"] = int(end_time)
    print(f"Total traces retrieved: {len(traces['data'])}")
    
    sorted_req_type_traces = count_requests_per_second(traces)
    store_traces(sorted_req_type_traces, data_dir, intensity)

    with open(f"{data_dir}/traces_directory/{intensity}_complete.json", "w") as outfile:
        dump(traces, outfile)

if __name__ == "__main__":
    main()
