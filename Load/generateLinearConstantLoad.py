import csv
from datetime import datetime, timedelta, date
import os

def generate_linear_profile(duration, duration_linear, step_sizes, start_value):
    """
    Génère des profils de charge linéaires avec différentes progressions.

    Args:
        duration (float): Durée totale du profil de charge (en secondes).
        step_sizes (list): Liste des tailles de progression à utiliser.
        start_value (float): Valeur de départ.
    """

    now = datetime.now()
    dir_name = f"profiles_{now.strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)

    for step_size in step_sizes:
        file_name = f"const_linear_{step_size}requests_per_sec.csv"
        file_path = os.path.join(dir_name, file_name)

        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['timestamp', 'requests'])

            current_timestamp = start_value
            while current_timestamp <= duration_linear + start_value - 1:  # Première partie : progression linéaire jusqu'à 180 secondes
                value = step_size * ((current_timestamp - start_value + 1) / 180)
                if value < 1:
                    value = 1
                writer.writerow([current_timestamp, value])
                current_timestamp += 1

            while current_timestamp <= duration + start_value - 1:  # Deuxième partie : charge stable jusqu'à 600 secondes
                writer.writerow([current_timestamp, step_size])
                current_timestamp += 1

        print(f"Profil de charge linéaire généré : {file_path}")
# Paramètres de configuration
DURATION_LINEAR = 300  # Durée pour la charge linéaire
DURATION = 600  # Durée totale du profil de charge (en secondes)
STEP_SIZES = [20, 40, 60, 80]  # Tailles de progression à utiliser
START_VALUE = 0.5  # Valeur de départ

generate_linear_profile(DURATION, DURATION_LINEAR, STEP_SIZES, START_VALUE)