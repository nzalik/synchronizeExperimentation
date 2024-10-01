import matplotlib.pyplot as plt
import time

# Exemple de données JSON
data = {
    "result": [
        {
            "metric": {
                "destination_workload": "teastore-auth",
                "source_workload": "teastore-webui"
            },
            "values": [
                [1727671820, "917.4470691043205"],
                [1727671920, "920.123456789"],
                [1727672020, "918.987654321"]
            ]
        },
        {
            "metric": {
                "destination_workload": "teastore-auth",
                "source_workload": "teastore-persistence"
            },
            "values": [
                [1727671820, "917.4470691043205"],
                [1727671920, "915.654321987"],
                [1727672020, "916.876543210"]
            ]
        }
    ]
}

# Initialisation de la figure pour le plot
plt.ion()  # Mode interactif pour mettre à jour le graphique en temps réel
fig, ax = plt.subplots()


# Fonction pour mettre à jour le graphique
def update_plot(data):
    ax.clear()  # Efface le graphique précédent

    # Boucle sur chaque série de données dans le JSON
    for series in data['result']:
        source = series['metric']['source_workload']
        destination = series['metric']['destination_workload']

        # Extraction des timestamps et des valeurs
        timestamps = [time_point[0] for time_point in series['values']]
        values = [float(time_point[1]) for time_point in series['values']]

        # Tracer les données pour cette paire source/destination
        ax.plot(timestamps, values, label=f'{source} → {destination}')

    # Ajout des légendes et des titres
    ax.set_title('Metrics between Microservices')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Value')
    ax.legend(loc='upper left')

    plt.draw()
    plt.pause(0.1)  # Pause pour permettre à matplotlib de mettre à jour le graphique


# Boucle continue pour simuler la mise à jour en temps réel
try:
    while True:
        # Mettre à jour le graphique avec les données actuelles
        update_plot(data)

        # Pause de 5 secondes avant la prochaine mise à jour (vous pouvez ajuster ce délai)
        time.sleep(5)

        # Simuler une mise à jour des données (vous pouvez remplacer cela par une requête à l'API Prometheus)
        # Ajout d'une nouvelle valeur pour la série "teastore-webui -> teastore-auth"
        data['result'][0]['values'].append([data['result'][0]['values'][-1][0] + 100, "918.123456789"])
        data['result'][1]['values'].append([data['result'][1]['values'][-1][0] + 100, "914.876543210"])

except KeyboardInterrupt:
    print("Interrompu par l'utilisateur")
    plt.close()
