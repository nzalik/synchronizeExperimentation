import configparser
import json
import os
import requests

line_styles = ["solid", "dotted", "dashed", "dashdot"]

plot_limit = 301
cpu_limit_max = 1.2
load_max = 475
memory_limit = 5
pod_limit = 2

colors_table = [
    "#FF5733",  # Rouge orangé
    "#33FF57",  # Vert Lime
    "#3357FF"  # Bleu Foncé
]


def normalization(value):
    return value / (1000 ** 3)


def get_color_for_service(service_name):
    service_name = service_name.lower()

    # Récupérer le nom de base du service (sans le numéro ni le hachage)
    base_name = '-'.join(service_name.split('-')[:-2])

    # Récupérer le numéro du service (s'il y en a un)
    try:
        instance_number = int(service_name.split('-')[-2])
    except ValueError:
        instance_number = 1

    # Définir les couleurs de base pour chaque service
    color_map = {
        'teastore-webui': '#8ECAE6',
        'teastore-persistence': '#219EBC',
        'teastore-db': '#126782',
        'teastore-registry': '#023047',
        'teastore-auth': '#FFB703',
        'teastore-image': '#FD9E02',
        'teastore-recommender': '#FB8500'
    }

    # Choisir la couleur en fonction du numéro d'instance
    base_color = color_map.get(base_name, 'black')
    if instance_number > 1:
        hue = (instance_number - 1) * 60  # Décalage de la teinte de 60 degrés par instance
        color = f'hsl({hue}, 100%, 50%)'
    else:
        color = base_color

    return color, base_name


def smooth(values, w_size=5):
    new_values = []
    for i in range(len(values)):
        window = values[max(0, i - (w_size - 1) // 2):min(i + w_size // 2 + 1, len(values))]
        new_values.append(sum(window) / len(window))
    return new_values


def open_file(file_name):
    with open(file_name, 'r') as file:
        json_data = json.load(file)
        return json_data


def read_parameters_from_json(file_path):
    with open(file_path, 'r') as file:
        parameters = json.load(file)
    return parameters


def sort_legend(legend_objects, legend_labels):
    """
    Trie les objets de légende et leurs labels par ordre alphabétique.

    Parameters:
    - legend_objects: Liste des objets de légende.
    - legend_labels: Liste des labels de légende.

    Returns:
    - Objects et labels triés.
    """
    # Créer des paires d'objets et de labels
    legend_pairs = list(zip(legend_objects, legend_labels))

    # Trier les paires par labels
    legend_pairs_sorted = sorted(legend_pairs, key=lambda x: x[1])

    # Séparer les objets et les labels après le tri
    legend_objects_sorted, legend_labels_sorted = zip(*legend_pairs_sorted)

    return legend_objects_sorted, legend_labels_sorted


def get_color_for_service_init(service_name):
    return '#9c23c2'
