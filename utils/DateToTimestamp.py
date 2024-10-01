import datetime

# La date à convertir (format : 'YYYY-MM-DD HH:MM:SS')
date_str = "2024-10-01 10:14:57"

# Conversion de la chaîne de caractères en objet datetime
date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

# Conversion de l'objet datetime en timestamp
timestamp = int(date_obj.timestamp())

# Affichage du timestamp
print("Timestamp:", timestamp)
