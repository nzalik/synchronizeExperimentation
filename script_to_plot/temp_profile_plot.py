import pandas as pd
import matplotlib.pyplot as plt

# Charger les données depuis un fichier CSV
# Remplace 'data.csv' par le nom de ton fichier
df = pd.read_csv('/home/erods-chouette/Documents/synchronizeExperimentation/workload_generators/intensity-to-csv/intensity_profiles/li_const_2.csv', header=None, names=['x', 'y'])

# Création du plot
plt.figure(figsize=(10, 5))
plt.plot(df['x'], df['y'], marker='o', linestyle='-', color='b', label="Data Points")

# Ajout de titres et labels
plt.title("Plot of Data from CSV")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()

# Afficher le graphique
#plt.grid(True)
plt.show()