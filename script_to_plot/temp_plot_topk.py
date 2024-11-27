import json
import matplotlib.pyplot as plt
import datetime

file_path="/home/erods-chouette/Documents/synchronizeExperimentation/locust/nantes/train/sequential/27-11-2024/temp_15m_collect_warmup_load1/hyperthreading/SearchTicket/li_linear_5/aggregation/1_top_pods_li_linear_5.json"


# Lire les données depuis un fichier JSON
with open(file_path, 'r') as file:
    data = json.load(file)

# Accéder à la liste des résultats
results = data["data"]["result"]

# Initialisation des variables pour le tracé
plt.figure(figsize=(12, 8))

# Parcourir chaque objet dans les résultats
for result in results:
    pod_name = result["metric"]["pod"]  # Nom du pod
    pod_data = result["values"]  # Données du pod

    # Extraire les timestamps et les valeurs
    timestamps = [entry[0] for entry in pod_data]
    values = [float(entry[1]) for entry in pod_data]

    # Convertir les timestamps en format lisible
    readable_timestamps = [datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]

    # Tracer les données
    plt.plot(readable_timestamps, values, marker='o', label=pod_name)

# Configurer le graphique
plt.title('Pod Metrics Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Metric Value')
plt.xticks(rotation=45, ha='right')
plt.legend(title="Pods")
#plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Afficher le graphique
plt.show()