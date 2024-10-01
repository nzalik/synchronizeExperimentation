import json
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Nom du fichier JSON (par exemple 'data.json')
json_filename = '/home/erods-chouette/PycharmProjects/synchronizeExperimentation/Fetcher/temp/datadir/from_teastore-recommender_to_teastore-persistence.json'

# Charger le JSON depuis un fichier

with open(json_filename) as f:
    data = json.load(f)

# Extraire les résultats
results = data['data']['result']

# Pour chaque métrique dans les résultats
for result in results:
    metric = result['metric']
    destination_workload = metric.get('destination_workload', 'unknown')

    # Extraire les timestamps et les valeurs associées
    timestamps = [point[0] for point in result['values']]  # Les timestamps
    heures = [datetime.fromtimestamp(ts).strftime('%H:%M') for ts in timestamps]
    values = [float(point[1]) for point in result['values']]  # Les valeurs (converties en float)
    print("le maximum")
    print(max(values))
    # Plotter les données
    plt.plot(heures, values, label=f'{destination_workload}')

# Ajouter des labels et des légendes
plt.xlabel('Timestamp')
plt.ylabel('Latency (ms)')
plt.title('Latency over time')
plt.legend()

# Enregistrer le fichier avec le même nom que le fichier JSON mais avec l'extension .png
output_filename = os.path.splitext(json_filename)[0] + '.png'
print("le chemin")
print(output_filename)
plt.savefig(output_filename)

# Afficher le graphique
plt.show()

# Imprimer le nom du fichier sauvegardé
print(f"Graphique sauvegardé sous {output_filename}")
