import datetime

# Le timestamp à convertir
timestamp = 1732667699.0

# Conversion en date lisible avec heure locale
converted_time_local = datetime.datetime.fromtimestamp(timestamp)

# Affichage de la date et heure locale
print("Date et heure locale:", converted_time_local.strftime('%Y-%m-%d %H:%M:%S'))