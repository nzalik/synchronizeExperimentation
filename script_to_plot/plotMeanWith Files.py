import json
import numpy as np
import matplotlib.pyplot as plt

def get_color_for_service(label):
    # Fonction pour obtenir la couleur et le nom du service (à adapter selon vos besoins)
    color = 'blue'  # Exemple : la couleur peut être changée selon le service
    return color, label

def plot_multiple_jsons(file_names, label):
    # Listes pour stocker les timestamps et les valeurs pour chaque fichier
    all_timestamps = []
    all_values = []

    # Lire chaque fichier et stocker les données
    for file_name in file_names:
        with open(file_name, 'r') as file:
            json_data = json.load(file)

        if len(json_data['data']['result']) > 0:
            datas = json_data['data']['result'][0]['values']

            timestamps = np.array([int(ts) for ts, _ in datas])
            values = np.array([float(value) for _, value in datas])

            all_timestamps.append(timestamps)
            all_values.append(values)

    # Assurez-vous que tous les timestamps sont alignés
    common_timestamps = all_timestamps[0]
    for ts in all_timestamps[1:]:
        common_timestamps = np.intersect1d(common_timestamps, ts)

    # Filtrer les valeurs correspondantes aux timestamps communs
    filtered_values = []
    for i, ts in enumerate(all_timestamps):
        mask = np.isin(ts, common_timestamps)
        filtered_values.append(all_values[i][mask])

    print("les données")
    print(filtered_values)
    # Calculer la moyenne pour chaque timestamp commun
    average_values = np.mean(filtered_values, axis=0)

    # Tracer la courbe de la moyenne
    color, base_name = get_color_for_service(label)
    plt.plot(common_timestamps, average_values, color=color, label=f"Moyenne - {label}")

    # Ajouter des légendes, titres, etc.
    plt.xlabel("Timestamp")
    plt.ylabel("Valeur moyenne")
    plt.title(f"Moyenne des valeurs pour {label}")
    plt.legend()

    return common_timestamps, average_values

# Exemple d'utilisation :
files = ['/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/li_stairsd_2/cpu/teastore-webui/teastore-webui-68f6c488b6-7ckvz.json',
         '/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/li_stairsd_2/cpu/teastore-webui/teastore-webui-68f6c488b6-tp2wd.json',
         '/home/erods-chouette/Documents/synchronizeExperimentation/locust/advanced/nantes/hyperthreading/128/linear/3nodes/linear/mean_calculation/li_stairsd_2/cpu/teastore-webui/teastore-webui-68f6c488b6-wwv8x.json'
         ]
# Remplacez par vos fichiers JSON
plot_multiple_jsons(files, 'cpu')

# Afficher le graphique
plt.show()
