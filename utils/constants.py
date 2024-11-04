import json
from datetime import datetime

line_styles=["solid","dotted","dashed","dashdot"]

plot_limit = 301
cpu_limit_max=1.2
load_max=475
memory_limit=5
pod_limit=2
cpu_step = "2m"

def get_color_for_serviceInit(service_name):
    service_name = service_name.lower()

    # Switch case avec 7 cas différents
    match service_name:
        case 'teastore-webui':
            return '#8ECAE6'
        case 'teastore-persistence':
            return '#eb014f'
        case 'teastore-db':
            return '#126782'
        case 'teastore-registry':
            return '#023047'
        case 'teastore-auth':
            return '#FFB703'
        case 'teastore-image':
            return '#067d4a'
        case 'teastore-recommender':
            return '#9c23c2'
        case _:
            return '#295F98'

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
        #for file_name in files:
        #with open(file_name, 'r') as file:
        json_data = json.load(file)
        return json_data


def smooth(values, w_size=5):
    new_values = []
    for i in range(len(values)):
        window = values[max(0, i - (w_size - 1) // 2):min(i + w_size // 2 + 1, len(values))]
        new_values.append(sum(window) / len(window))
    return new_values

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

def plot_metrics(data, ax):
    global timestamps
    results = data['data']['result']

    for result in results:
        metric = result['metric']
        source_workload = metric.get('source_workload', 'unknown')
        destination = metric.get('destination_workload', elt)

        source_workload_txt = source_workload.split('-')[1] if '-' in source_workload else source_workload
        destination_txt = destination.split('-')[1]

        timestamps = np.arange(0, plot_limit)
        valuesInit = [0 if point[1] == "NaN" else float(point[1]) for point in
                      result['values'][:plot_limit]] + [0] * (
                             plot_limit - min(plot_limit, len(
                         result['values'])))  # Remplacer NaN par 0 et compléter avec des 0 si nécessaire

        multiplier_note = ''
        if harmonization and metric_to_plot == "latency":
            if destination != 'teastore-webui' and metric_to_plot == "latency":
                valuesInit = [x * 5 for x in valuesInit]  # Multiply values by a factor for non-webui destinations
                multiplier_note = ' (x5)'
            else:
                multiplier_note = ''


        values = smooth(valuesInit)
        heures = [datetime.fromtimestamp(ts).strftime('%M') for ts in timestamps]

        color = get_color_for_serviceInit(source_workload)
        ax.plot(timestamps, values, color=color,
                label=f'{source_workload_txt + str(position + 1)} → {destination_txt + str(position + 1)}{multiplier_note}',
                linestyle=line_styles[position])

    start_time = min(timestamps)
    end_time = max(timestamps)

    ticks = np.arange(start_time, end_time + 1, plot_window)
    ticks_seconds = [((ts - start_time) // plot_window) * plot_window for ts in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticks_seconds)

    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('rps (requests per second)')
    ax.set_title(f'Request volume')
    #ax.set_title(f'Requests volume send to {elt}')
    if metric_to_plot=="latency":
        ax.set_ylabel('Latency (ms)')
        ax.set_title(f'Request duration')
        #ax.set_title(f'Request duration to {elt}')

    ax.set_ylim(0, max_value)
    ax.legend(loc='upper left', frameon=False)
    return ticks
