import os
import csv
from datetime import datetime
import math

def generate_sinusoidal_profile(duration, amplitude, frequency):
    """
    Génère un profil de charge sinusoïdal.

    Args:
        duration (float): Durée totale du profil de charge (en secondes).
        amplitude (float): Amplitude de la variation des requêtes.
        frequency (float): Fréquence des cycles sinusoïdaux.
    """

    now = datetime.now()
    dir_name = f"profiles_{now.strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)

    file_name = f"sinusoidal_{amplitude}_requests_per_sec.csv"
    file_path = os.path.join(dir_name, file_name)

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['timestamp', 'requests'])

        current_timestamp = 0

        while current_timestamp <= duration:
            # Calcul de la valeur sinusoïdale (amplitude * sin(fréquence * temps))
            current_value = amplitude * math.sin(2 * math.pi * frequency * current_timestamp / duration) + amplitude
            writer.writerow([current_timestamp, current_value])
            current_timestamp += 1

    print(f"Profil de charge sinusoïdal généré : {file_path}")

# Paramètres de configuration
DURATION = 600  # Durée totale (en secondes)
AMPLITUDE = 200  # Amplitude du nombre de requêtes
FREQUENCY = 1  # Fréquence des cycles sinusoïdaux

generate_sinusoidal_profile(DURATION, AMPLITUDE, FREQUENCY)
