import os
import csv
from datetime import datetime

def generate_spike_profile(duration, spike_value, spike_time):
    """
    Génère un profil de charge en pic (spike).

    Args:
        duration (float): Durée totale du profil de charge (en secondes).
        spike_value (float): Nombre de requêtes par seconde pendant le pic.
        spike_time (float): Temps où le pic se produit.
    """

    now = datetime.now()
    dir_name = f"profiles_{now.strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)

    file_name = f"spike_{spike_value}_requests_per_sec.csv"
    file_path = os.path.join(dir_name, file_name)

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['timestamp', 'requests'])

        current_timestamp = 0

        while current_timestamp <= duration:
            if current_timestamp == spike_time:
                current_value = spike_value
            else:
                current_value = 50  # Valeur de base en dehors du pic

            writer.writerow([current_timestamp, current_value])
            current_timestamp += 1

    print(f"Profil de charge en pic généré : {file_path}")

# Paramètres de configuration
DURATION = 600  # Durée totale (en secondes)
SPIKE_VALUE = 1000  # Valeur maximale pendant le pic
SPIKE_TIME = 300  # Moment du pic (en secondes)

generate_spike_profile(DURATION, SPIKE_VALUE, SPIKE_TIME)
