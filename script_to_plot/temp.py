import matplotlib.pyplot as plt

# Données exemples
x = [1, 2, 3, 4]
y1 = [10, 20, 30, 40]      # Grande échelle
y2 = [1, 2, 3, 4]          # Petite échelle

# Configuration du subplot
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# Sous-plot 1 avec une échelle normale
ax1.plot(x, y1, label="Courbe 1")
ax1.set_ylim(0, 50)
ax1.set_ylabel("Valeurs d'origine")

# Sous-plot 2 avec un facteur d'échelle
scale_factor = 10
ax2.plot(x, [val * scale_factor for val in y2], label="Courbe 2 (x10)")
ax2.set_ylim(0, 50)
ax2.set_ylabel(f"Valeurs (x{scale_factor})")

# Ajouter des légendes
ax1.legend()
ax2.legend()

plt.xlabel("x")
plt.show()