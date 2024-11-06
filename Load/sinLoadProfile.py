import math
import csv
import os
from datetime import datetime


def sin_f_auto(t, duration):
    """
    Génère une valeur sinusoïdale automatiquement basée sur la durée uniquement.

    :param t: Le pas de temps actuel.
    :param duration: La durée totale de la série.
    :return: La valeur sinusoïdale pour le pas de temps 't'.
    """
    # Valeurs par défaut pour le plafond et le plancher
    floor = 10
    ceil = 25

    # Nombre de pics par défaut (ici on utilise 4 pics sur toute la durée)
    peak_nb = 2

    # Calcul automatique de la fréquence angulaire
    f = peak_nb / duration  # Fréquence du sinus en fonction de la durée et du nombre de pics
    fun_freq = 2 * math.pi * f  # Fréquence angulaire

    # Amplitude et décalage pour osciller entre ceil et floor
    amplitude = (ceil - floor) / 2  # Amplitude de l'onde
    v_offset = amplitude + floor  # Décalage vertical pour centrer l'onde entre ceil et floor

    # Calcul de la valeur sinusoïdale pour le temps donné
    value = amplitude * math.sin(fun_freq * t) + v_offset

    return value

now = datetime.now()
dir_name = f"profiles_{now.strftime('%Y-%m-%d')}"
if not os.path.exists(dir_name):
    os.makedirs(dir_name, exist_ok=True)

# Paramètres pour la génération
duration = 300  # Durée en secondes
step_size = 10  # Intervalle de temps entre chaque point de la série
file_name = "sin_auto_profile.csv"
file_path = os.path.join(dir_name, file_name)

with open(file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['timestamp', 'requests'])

    # Génération des valeurs sinusoïdales automatiquement basées sur la durée
    for t in range(1, int(duration + step_size), int(step_size)):
        value = sin_f_auto(t, duration)
        writer.writerow([t, int(max(value, 1))])  # Arrondir et s'assurer que la valeur est au moins de 1

    print(f"Profil de charge sinusoïdal généré: {file_name}")
    print(file_path)