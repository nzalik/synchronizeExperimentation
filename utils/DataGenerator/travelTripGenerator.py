import uuid

# Liste des stations
stations = [
    "shanghai", "taiyuan", "nanjing", "wuxi", "suzhou",
    "shanghaihongqiao", "beijing", "shijiazhuang",
    "xuzhou", "jinan", "hangzhou", "jiaxingnan", "zhenjiang"
]

# Types de trains disponibles
train_types = ["GaoTieOne", "GaoTieTwo", "DongCheOne"]


# Génération des données
def generate_trips():
    trip_counter = 1
    result = []

    for start_station in stations:
        for terminal_station in stations:
            if start_station != terminal_station:
                trip_id = f"{trip_counter:05}"  # Trip ID sur 5 chiffres
                train_type = train_types[trip_counter % len(train_types)]  # Choix du type de train
                route_id = str(uuid.uuid4())  # ID unique pour chaque route
                start_time = f"2013-05-04 {8 + (trip_counter % 12):02}:00:00"  # Heure de départ
                end_time = f"2013-05-04 {10 + (trip_counter % 12):02}:00:00"  # Heure d'arrivée

                # Ajout des données formatées
                result.append(f"""
info.setTripId("{trip_id}");
info.setTrainTypeName("{train_type}");
info.setRouteId("{route_id}");
info.setStartStationName("{start_station}");
info.setStationsName("intermediatestation");
info.setTerminalStationName("{terminal_station}");
info.setStartTime("{start_time}"); //NOSONAR
info.setEndTime("{end_time}"); //NOSONAR
service.create(info, null);
""")
                trip_counter += 1

    return result


# Générer les données
trips = generate_trips()

# Écriture dans un fichier
with open("trips.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(trips))

print("Les données ont été écrites dans le fichier 'trips.txt' dans le répertoire courant.")
