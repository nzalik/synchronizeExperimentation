import csv
from datetime import datetime
import os
import numpy as np

def generate_linear_profile(duration, step_size, start_value, end_values):
    """Génère un profil de charge linéaire avec la progression donnée."""
    now = datetime.now()
    dir_name = f"profiles_{now.strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)

    for end_value in end_values:
        file_name = f"linear_{end_value}requests_max_per_sec.csv"
        file_path = os.path.join(dir_name, file_name)

        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['timestamp', 'requests'])

            for t in range(0, int(duration + step_size), int(step_size)):
                if t < (duration - (2 * step_size)):
                    value = start_value + (end_value - start_value) * t / duration
                    value = int(value) if value % 1 == 0 else int(value)
                    writer.writerow([t + 0.5, max(value, 1)])
                else:
                    writer.writerow([t + 0.5, end_value])

            print(f"Profil de charge linéaire généré: {file_name}")

def generate_sinusoidal_profile(duration, step_size, amplitude, num_peaks):
    """Génère un profil de charge sinusoïdal avec un nombre de pics spécifié."""
    now = datetime.now()
    dir_name = f"profiles_{now.strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)

    file_name = f"sinusoidal_profile_{num_peaks}_peaks.csv"
    file_path = os.path.join(dir_name, file_name)

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['timestamp', 'requests'])

        times = np.arange(0, duration + step_size, step_size)
        frequency = num_peaks / duration * 2 * np.pi  # Calcul de la fréquence
        requests = amplitude * (1 + np.sin(frequency * times))

        for t, r in zip(times, requests):
            writer.writerow([t + 0.5, int(max(r, 1))])

    print(f"Profil de charge sinusoïdal généré: {file_name}")

def generate_cosinusoidal_profile(duration, step_size, amplitude, num_peaks):
    """Génère un profil de charge cosinusoidal avec un nombre de pics spécifié."""
    now = datetime.now()
    dir_name = f"profiles_{now.strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)

    file_name = f"cosinusoidal_profile_{num_peaks}_peaks.csv"
    file_path = os.path.join(dir_name, file_name)

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['timestamp', 'requests'])

        times = np.arange(0, duration + step_size, step_size)
        frequency = num_peaks / duration * 2 * np.pi  # Calcul de la fréquence
        requests = amplitude * (1 + np.cos(frequency * times))

        for t, r in zip(times, requests):
            writer.writerow([t + 0.5, int(max(r, 1))])

    print(f"Profil de charge cosinusoidal généré: {file_name}")

# Paramètres de configuration
DURATION = 599.5  # Durée totale du profil de charge (en secondes)
STEP_SIZE = 1.0
START_VALUE = 1.0  # Valeur de départ
END_VALUES = [1500, 2000]  # Valeurs finales pour le profil linéaire
AMPLITUDE = 50  # Amplitude pour les profils sinusoïdal et cosinusoidal
NUM_PEAKS = 5  # Nombre de pics pour les profils sinusoïdal et cosinusoidal

# Génération des profils
generate_linear_profile(DURATION, STEP_SIZE, START_VALUE, END_VALUES)
generate_sinusoidal_profile(DURATION, STEP_SIZE, AMPLITUDE, NUM_PEAKS)
generate_cosinusoidal_profile(DURATION, STEP_SIZE, AMPLITUDE, NUM_PEAKS)