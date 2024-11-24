import json
import matplotlib.pyplot as plt
import datetime

import numpy as np

from utils.constants import plot_limit

file_path="/home/erods-chouette/Documents/synchronizeExperimentation/locust/grenoble/train/24-11-2024/temp_1temp_profile_login_no_user_creation_at_beginning1/hyperthreading/linear_10/aggregation/1_top_pods_linear_10.json"

# Lire les données depuis un fichier JSON
with open(file_path, 'r') as file:
    data = json.load(file)

# Accéder à la liste des résultats
results = data["data"]["result"]
print(len(results))

# Calculer la consommation moyenne pour chaque pod
pod_metrics = {}
for result in results:
    pod_name = result["metric"]["pod"]
    values = [float(entry[1]) for entry in result["values"]]
    avg_value = sum(values) / len(values)  # Calcul de la moyenne
    #avg_value = max(values)   # Calcul du max
    pod_metrics[pod_name] = {
        "avg": avg_value,
        "timestamps": [entry[0] for entry in result["values"]],
        "values": values
    }

# Trier les pods par consommation moyenne décroissante
sorted_pods = sorted(pod_metrics.items(), key=lambda x: x[1]["avg"], reverse=True)

# Filtrer les top N pods (par exemple, les 3 premiers)
top_n = 10
top_pods = sorted_pods[:top_n]

# Tracer les courbes des top N pods
plt.figure(figsize=(12, 8))
for pod_name, metrics in top_pods:
    # Convertir les timestamps en format lisible
    # readable_timestamps = [
    #     datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #     for ts in metrics["timestamps"]
    # ]
    readable_timestamps = np.arange(0, plot_limit)
    values = metrics["values"][:plot_limit]
    # Tracer les données
    plt.plot(readable_timestamps, values, marker='o', label=f"{pod_name} (Avg: {metrics['avg']:.5f})")

# Configurer le graphique
plt.title(f'Top {top_n} Pod Consumers Over Time')
plt.xlabel('Timestamp')
plt.ylabel('CPU')
plt.xticks(rotation=45, ha='right')
plt.legend(title="Pods")
#plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Afficher le graphique
plt.show()