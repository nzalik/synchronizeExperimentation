import os
import csv
from datetime import datetime

def generate_parabolic_profile(duration, peak_value):
    """
    Génère un profil de charge parabolique (monte jusqu'à un pic puis redescend).

    Args:
        duration (float): Durée totale du profil de charge (en secondes).
        peak_value (float): Nombre maximal de requêtes par seconde au sommet du pic.
    """

    now = datetime.now()
    dir_name = f"profiles_{now.strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)

    file_name = f"parabolic_{peak_value}_requests_per_sec.csv"
    file_path = os.path.join(dir_name, file_name)

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['timestamp', 'requests'])

        half_duration = duration / 2
        current_timestamp = 0
        step = peak_value / half_duration  # Augmentation/diminution par seconde

        while current_timestamp <= duration:
            if current_timestamp <= half_duration:
                # Phase de montée
                current_value = step * current_timestamp
            else:
                # Phase de descente
                current_value = peak_value - step * (current_timestamp - half_duration)

            writer.writerow([current_timestamp, current_value])
            current_timestamp += 1

    print(f"Profil de charge parabolique généré : {file_path}")

# Paramètres de configuration
DURATION = 600  # Durée totale (en secondes)
PEAK_VALUE = 400  # Valeur maximale au sommet du pic

generate_parabolic_profile(DURATION, PEAK_VALUE)
