import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import EarthLocation, AltAz, get_body
from astropy.time import Time
import astropy.units as u

# Temps d'inici. El día en el que hi ha lluna plena en juny del 2025
time = Time('2025-06-11T23:59:59')

# Localitzem Cerdanyola
location = EarthLocation(lon=41.5 * u.deg, lat=-2 * u.deg, height=600 * u.m)

# Inicialitzem les llistes per guardar les coordenades
altitudes = []
azimuths = []

# Calcular les posicions de la lluna cada día lunar (24.84h) durant una volta...
#... dencera de la lluna al voltant de la terra (28 díes)
for i in range(28):
    moon = get_body('moon', time, location)
    altaz = AltAz(obstime=time, location=location)
    moon_altaz = moon.transform_to(altaz)

    altitudes.append(moon_altaz.alt.deg)
    azimuths.append(moon_altaz.az.deg)

    time += 24.8411996828 * u.hour

# Grafiquem els resultats
plt.style.use('classic')
plt.figure(figsize=(8, 8), facecolor='white')
sc = plt.scatter(azimuths, altitudes, c=range(28), s=100, cmap='jet', label='Analema lunar',edgecolors='none')
#plt.xlim(0, 360)
#plt.ylim(0, 90)
plt.colorbar(sc, label='Día del cicle')
plt.xlabel(r'Az [$\degree$]')
plt.ylabel(r'Alt [$\degree$]')
plt.title('Analema lunar a Bellaterra (Inici: 11/06/2025 a 23:59:59h)')
plt.grid(True)
plt.tight_layout()
plt.savefig("informe/images/analema_lluna.png", dpi=300, bbox_inches='tight')
plt.show()