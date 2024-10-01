import matplotlib.pyplot as plt
from datetime import datetime

# Data from the input
data = {
    "labels": {
        "source_canonical_service": "teastore",
        "source_workload_namespace": "default"
    },
    "datapoints": [
        [1726837632, "0"], [1726837704, "0"], [1726837776, "0"],
        [1726837848, "0"], [1726837920, "0"], [1726837992, "0"],
        [1726838064, "0"], [1726838136, "0"], [1726838208, "0"],
        [1726838280, "0"], [1726838352, "0"], [1726838424, "4537.666666666667"],
        [1726838496, "14748.8"], [1726838568, "0"], [1726838640, "0"],
        [1726838712, "0"], [1726838784, "0"], [1726838856, "0"],
        [1726838928, "0"], [1726839000, "0"], [1726839072, "0"],
        [1726839144, "0"], [1726839216, "0"], [1726839288, "0"],
        [1726839360, "0"], [1726839432, "0"], [1726839504, "0"],
        [1726839576, "0"], [1726839648, "0"], [1726839720, "0"],
        [1726839792, "0"], [1726839864, "0"], [1726839936, "0"],
        [1726840008, "0"], [1726840080, "0"], [1726840152, "0"],
        [1726840224, "0"], [1726840296, "0"], [1726840368, "0"],
        [1726840440, "0"], [1726840512, "0"], [1726840584, "0"],
        [1726840656, "0"], [1726840728, "0"], [1726840800, "0"],
        [1726840872, "0"], [1726840944, "0"], [1726841016, "0"],
        [1726841088, "0"], [1726841160, "0"], [1726841232, "0"]
    ],
    "name": "tcp_received"
}

# Extracting timestamps and values
timestamps = [datetime.utcfromtimestamp(dp[0]) for dp in data["datapoints"]]
values = [float(dp[1]) for dp in data["datapoints"]]

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(timestamps, values, marker='o', linestyle='-', color='b')

# Formatting the plot
plt.title(f"Plot for {data['name']} (Service: {data['labels']['source_canonical_service']})")
plt.xlabel("Time")
plt.ylabel("Value")
plt.xticks(rotation=45, ha='right')
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.savefig("tcp_recieved_packets.png")
plt.show()
