import json
import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np
# Exemple de données JSON (remplace par tes données réelles)
name='teastore-auth'
json_filename = '/home/erods-chouette/PycharmProjects/synchronizeExperimentation/Fetcher/temp/datadir2bis/latencies_to_'+name+'.json'

# Charger le JSON depuis un fichier

with open(json_filename) as f:
    data = json.load(f)

    def get_color_for_serviceInit(service_name):
        service_name = service_name.lower()

        # Switch case avec 7 cas différents
        match service_name:
            case 'teastore-webui':
                return '#8ECAE6'
            case 'teastore-persistence':
                return '#219EBC'
            case 'teastore-db':
                return '#126782'
            case 'teastore-registry':
                return '#023047'
            case 'teastore-auth':
                return '#FFB703'
            case 'teastore-image':
                return '#FD9E02'
            case 'teastore-recommender':
                return '#FB8500'
            case _:
                return 'black'

plot_window = 60
timestamps = []
# Fonction pour traiter et tracer les données
def plot_metrics(data):
    # Extraire les résultats
    global timestamps
    results = data['data']['result']

    # Pour chaque métrique dans les résultats
    for result in results:
        metric = result['metric']
        source_workload = metric.get('source_workload', 'unknown')

        # Extraire les timestamps et les valeurs
        timestamps = [point[0] for point in result['values']]  # Timestamps
        values = [0 if point[1] == "NaN" else float(point[1]) for point in result['values']]  # Remplacer NaN par 0

        # Convertir les timestamps en format heure lisible
        heures = [datetime.fromtimestamp(ts).strftime('%M') for ts in timestamps]

        color = get_color_for_serviceInit(source_workload)
        # Plotter les données
        plt.plot(timestamps, values, color=color, label=f'{source_workload}')

    # Ajouter des labels et une légende
    workload_name = "teastore-webui"
    start_time = min(timestamps)
    end_time = max(timestamps)

    ticks = np.arange(start_time, end_time + 1, plot_window)
    ticks_seconds = [((ts - start_time) // plot_window) * plot_window for ts in ticks]
    plt.xticks(ticks, ticks_seconds)

    plt.xlabel('Time (minutes)')
    plt.ylabel('Latency (ms)')
    plt.title('Latency from others services to '+name)
    plt.legend()
    output_filename = os.path.splitext(json_filename)[0] + '.png'
    # Afficher le graphique
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.show()


# Appeler la fonction pour tracer les données
plot_metrics(data)
