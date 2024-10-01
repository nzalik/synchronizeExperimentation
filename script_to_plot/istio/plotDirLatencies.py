import json
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Chemin du répertoire contenant les fichiers JSON
json_directory = '/home/erods-chouette/PycharmProjects/synchronizeExperimentation/Fetcher/temp/datadir/'

# Lister tous les fichiers JSON dans le répertoire
json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]

# Parcourir chaque fichier JSON
for json_filename in json_files:
    json_path = os.path.join(json_directory, json_filename)

    # Charger le fichier JSON
    with open(json_path) as f:
        data = json.load(f)

    # Extraire les résultats
    results = data['data']['result']

    # Initialiser une figure pour chaque fichier
    plt.figure()

    # Pour chaque métrique dans les résultats
    for result in results:
        metric = result['metric']
        destination_workload = metric.get('destination_workload', 'unknown')

        # Extraire les timestamps et les valeurs associées
        timestamps = [point[0] for point in result['values']]  # Les timestamps
        heures = [datetime.fromtimestamp(ts).strftime('%H:%M') for ts in timestamps]
        values = [float(point[1]) for point in result['values']]  # Les valeurs (converties en float)
        print(f"Fichier {json_filename} - Maximum pour {destination_workload}: {max(values)}")

        # Plotter les données
        plt.plot(heures, values, label=f'{destination_workload}')

    # Ajouter des labels et des légendes
    plt.xlabel('Timestamp')
    plt.ylabel('Latency (ms)')
    plt.title(f'Latency over time - {json_filename}')
    plt.legend()

    # Enregistrer le graphique avec le même nom que le fichier JSON mais avec l'extension .png
    output_filename = os.path.splitext(json_path)[0] + '.png'
    plt.savefig(output_filename)

    # Afficher le graphique (optionnel, selon si tu veux voir le plot à l'écran)
    plt.show()

    # Imprimer le nom du fichier sauvegardé
    print(f"Graphique sauvegardé sous {output_filename}")
