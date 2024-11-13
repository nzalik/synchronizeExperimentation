# from traces import open_json, count_requests_per_second, store_traces
# from json import dump
# import os

# data_dir = "/home/ojamil/metric-dataset-generator/data/socialnetwork/"
# folder = "traces_directory"
# for filename in os.listdir(f"{data_dir}{folder}/"):
#     if filename.endswith("complete.json"):
#         traces = open_json(f"{data_dir}{folder}/{filename}")
#         sorted_req_traces = count_requests_per_second(traces)
#         intensity = filename.replace("_complete.json", "")
#         store_traces(sorted_req_traces, data_dir, intensity)

#         with open(f"{data_dir}traces_directory2/{filename}", "w") as outfile:
#             dump(traces, outfile)



# import json
# import os
# from math import ceil, floor

# root_dir = "/home/ojamil/metric-dataset-generator/data/socialnetwork/traces_directory2/"
# # root_dir = "/home/ojamil/metric-dataset-generator/rearranged_data/socialnetwork/nginx-thrift/node_dist_1/hw_spec_1/pod_spec_1/std_comp/traces/"
# merged_items = {}
# for fname in os.listdir(root_dir):
#     if fname.endswith("complete.json") or fname.endswith("__.json"):
#         continue
#     api_name = fname.split("/")[-1].split("__")[-1].replace(".json", "")
#     f = open(f"{root_dir}{fname}")
#     data = json.load(f)
    
#     merged_items[api_name] = merged_items.get(api_name, []) + [x for x in data.values()]

# for x in merged_items.keys():
#     max_val = max(merged_items[x])
#     print(f"{x}: \nmax value: {max_val}\tscaled value: {ceil(max_val*1.2)}")





root_dir = "/home/ojamil/metric-dataset-generator/rearranged_data/socialnetwork/nginx-thrift/node_dist_1/hw_spec_1/pod_spec_1/std_comp"
files = []
merged_traces = {"wrk2-api_home-timeline_read": {}, "wrk2-api_user-timeline_read": {}, "wrk2-api_post_compose": {}}
removed_dirs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    #if dirnames in functions:
    dirnames[:] = [d for d in dirnames if d not in removed_dirs]
    if not dirpath.endswith("/traces"):
        continue
    for filename in filenames:
        if filename.endswith("__.json"):
            continue
        filepath = os.path.join(dirpath, filename)
        if not filename.endswith("complete.json"): 
            files.append(filepath)
            continue
        f = open(filepath)
        data = json.load(f)
        start_time = int(data["start_time"]/1e6)
        end_time = start_time + 300
        for i in range(start_time, end_time):
            for k in merged_traces.keys():
                merged_traces[k][i] = 0

for x in merged_traces.keys():
    print(len(merged_traces[x]))
    
for fname in files:
    f = open(fname)
    data = json.load(f)
    api_name = fname.split("/")[-1].split("__")[-1].replace(".json", "")
    for k,v in data.items():
        k = int(k)
        if merged_traces[api_name].get(k, None) is not None:
            merged_traces[api_name][k] = v
        else:
            # print(merged_traces[api_name], len(merged_traces[api_name]))
            print(k, api_name, fname)
            break
    merged_traces[api_name] |= {int(k):v for k,v in data.items()}
sorted_timestamps = {}
for operation_name, timestamps in merged_traces.items():
    sorted_timestamps[operation_name] = dict(sorted(timestamps.items()))
merged_traces = {}
for operation_name in sorted_timestamps.keys():
    merged_traces[operation_name] = [(k,v) for k,v in sorted_timestamps[operation_name].items()]

for x in merged_traces.keys():
    print(merged_traces[x][0], merged_traces[x][-1], len(merged_traces[x]))


