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


#Registrem els valors de la declinació, l'ascensió recta i l'elevació i azimut del Sol per cada día. ...
#... Realment només ens interessa la declinació i elevació, però trobem l'ascensió ...
#... recta i azimut per completitud
ra_values = []
dec_values = []
alt_values = []
az_values = []

for day in days:
    observer.date = ephem.Date(day + timedelta(hours=12))
    sun = ephem.Sun(observer)
    ra_values.append(sun.ra)
    dec_values.append(sun.dec)
    alt_values.append(sun.alt)
    az_values.append(sun.az)


#Fem les conversions d'unitats necessàries
ra_deg = np.array(ra_values) * 180 / np.pi  #Radians a graus
dec_deg = np.array(dec_values) * 180 / np.pi  #Radians a graus
alt_deg = np.array(alt_values) * 180 / np.pi  #Radians a graus
az_deg = np.array(az_values) * 180 / np.pi  #Radians a graus
ra_hours = ra_deg * 24 / 360  #Graus a hores
dec_hours = dec_deg * 24 / 360  #Graus a hores
alt_hours = alt_deg * 24 / 360  #Graus a hores
az_hours = az_deg * 24 / 360  #Graus a hores


#Trobem els valors de la diferència horària entre el temps solar aparent...
#... i el temps mitjà a cada día emprant la fórmula de la equació del temps. ...
#... Aprofitem a enregistrar els valors de D(d) per completitud
D_aux = []
time_dif = []

for d in range(len(days)):
    D_aux.append(163.3155293 + 0.01720197 * d)
    time_dif.append(( -7.659 * np.sin(D_aux[-1]) + 9.863 * np.sin(2 * D_aux[-1] + 3.5932) ) * 360 / (24*60))


#Dibuixem l'analema del Sol dec(\Delta t) a l'any 2025. 
plt.style.use('classic')
plt.figure(figsize=(8,8), facecolor='white')
plt.plot(time_dif, dec_hours, label= r"$dec(\Delta t)$", color='r')
plt.xlabel( r"$T_{aparent} - T_{mitjà}$ [$\degree$]")
plt.ylabel("$Declinatció$ [$h$]")
plt.title("Analema del Sol (2025)")
ax = plt.gca()
ax.axhline(y=0, color='black', linewidth=1)
ax.axvline(x=0, color='black', linewidth=1)
for spine in ax.spines.values():
    spine.set_visible(True)
plt.grid(True)
plt.legend()
plt.savefig("informe/images/analema_dec.png", dpi=300, bbox_inches='tight')
plt.show()

#Dibuixem l'analema del Sol alt(\Delta t) a Bellaterra per a l'any 2025. 
plt.style.use('classic')
plt.figure(figsize=(8,8), facecolor='white')
plt.plot(time_dif, alt_deg, label=r"$alt(\Delta t)$", color='r')
plt.xlabel( r"$T_{aparent} - T_{mitjà}$ [$\degree$]")
plt.ylabel("$Elevació$ [$\degree$]")
plt.title("Analema del Sol en Bellaterra (2025)")
ax = plt.gca()
ax.axhline(y=0, color='black', linewidth=1)
ax.axvline(x=0, color='black', linewidth=1)
for spine in ax.spines.values():
    spine.set_visible(True)
plt.grid(True)
plt.legend()
plt.savefig("informe/images/analema_alt.png", dpi=300, bbox_inches='tight')
plt.show()