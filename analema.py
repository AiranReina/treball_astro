import numpy as np
import matplotlib.pyplot as plt
import ephem
from datetime import datetime, timedelta

###########################################################################

#Primer, definim les coordenades de Bellaterra
latitude = '41.505789'
longitude = '2.089509'


#Creem un objecte Observer d'ephem per a Bellaterra, així ens facilitarem ...
#... el càlcul de la posició del Sol
observer = ephem.Observer()
observer.lat = latitude
observer.lon = longitude


#Creem una llista de dates per a tot l'any 2025. De nou, utilitzant ephem,...
#... ens simplificarà el programa
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]


#Registrem els valors de la declinació i l'ascensió recta del Sol per cada día. ...
#... Realment només ens interessa la declinació, però trobem l'ascensió ...
#... recta per completitud
ra_values = []
dec_values = []

for day in days:
    observer.date = ephem.Date(day)
    sun = ephem.Sun(observer)
    ra_values.append(sun.ra)
    dec_values.append(sun.dec)


#Fem les conversions d'unitats necessàries
ra_deg = np.array(ra_values) * 180 / np.pi  #Radians a graus
dec_deg = np.array(dec_values) * 180 / np.pi  #Radians a grays
ra_hours = ra_deg * 24 / 360  #Graus a hores
dec_hours = dec_deg * 24 / 360  #Graus a hores


#Trobem els valors de la diferència horària entre el temps solar aparent...
#... i el temps mitjà a cada día emprant la fórmula de la equació del temps. ...
#... Aprofitem a enregistrar els valors de D(d) per completitud
D_aux = []
time_dif = []

for d in range(len(days)):
    D_aux.append(163.3155293 + 0.01720197 * d)
    time_dif.append(( -7.659 * np.sin(D_aux[-1]) + 9.863 * np.sin(2 * D_aux[-1] + 3.5932) ))


#Dibuixem l'analema del Sol a Bellaterra per a l'any 2025. 
plt.style.use('classic')
plt.figure(figsize=(8,8), facecolor='white')
plt.plot(time_dif, dec_hours, label="Analemma of the Sun (2025)", color='r')
plt.xlabel(r"$T_{aparent} - T_{mitjà}$ [$\degree$]")
plt.ylabel("$Declinatció$ [$h$]")
plt.title("Analema del Sol en Bellaterra (2025)")
ax = plt.gca()
ax.axhline(y=0, color='black', linewidth=1)
ax.axvline(x=0, color='black', linewidth=1)
for spine in ax.spines.values():
    spine.set_visible(True)
plt.grid(True)
plt.savefig("informe/images/analema_codi.png", dpi=300, bbox_inches='tight')
plt.show()