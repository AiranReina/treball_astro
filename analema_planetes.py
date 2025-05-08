import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jn
from astropy.time import Time
from astropy.coordinates import get_body, AltAz, EarthLocation
import astropy.units as u

# Definim els paràmetres de l'observador
lat_deg = 41.5
hour = 12
lat_rad = np.radians(lat_deg)
N = 20


########################################
#---------------- MART ----------------#
########################################


# Definim els paràmetres de Mart
tau_mars = 16.5
mars_period = 686.98
days = np.linspace(0, mars_period, 1000)
e_mars = 0.0934
obliquity_mars = np.radians(25.19)
perihelion_long_mars = np.radians(286.502)

# Realitzem els càlculs necesàris
M_mars = 2 * np.pi * (days - tau_mars) / mars_period
E_series = M_mars.copy()
for n in range(1, N + 1):
    E_series += (2 / n) * jn(n, n * e_mars) * np.sin(n * M_mars)

nu = np.arctan2(np.sqrt(1 - e_mars**2) * np.sin(E_series), np.cos(E_series) - e_mars)
lambda_sun = (nu + perihelion_long_mars) % (2 * np.pi)
alpha = np.unwrap(np.arctan2(np.cos(obliquity_mars) * np.sin(lambda_sun), np.cos(lambda_sun)))
delta = np.arcsin(np.sin(obliquity_mars) * np.sin(lambda_sun))

EOT_rad = M_mars - alpha
EOT_min = EOT_rad * (1440 / (2 * np.pi))
EOT_min -= np.mean(EOT_min)

# Grafiquem l'analema vist des de Mart
H_deg = 15 * (hour + EOT_min / 60 - 12)
H_rad = np.radians(H_deg)
alt = np.degrees(np.arcsin(np.sin(lat_rad) * np.sin(delta) + np.cos(lat_rad) * np.cos(delta) * np.cos(H_rad)))
az = np.degrees(np.arctan2(-np.sin(H_rad), -np.cos(H_rad)*np.sin(lat_rad) + np.tan(delta)*np.cos(lat_rad))) % 360

plt.style.use('classic')
plt.figure(figsize=(10, 8),facecolor='white')
sc = plt.scatter(az, alt, c=days, cmap='jet', s=100, label='Mart', edgecolors='none')
cbar = plt.colorbar(sc, label='Día del any a Mart')
plt.xlabel(r'Az [$\degree$]')
plt.ylabel(r'Alt [$\degree$]')
plt.title(f"Analema Solar a Mart a la Latitud {np.degrees(lat_rad):.1f}° (12h)", fontsize=16)
plt.grid(True)
plt.tight_layout()
plt.savefig("informe/images/analema_Mart.png", dpi=300, bbox_inches='tight')
plt.show()


########################################
#---------- JÚPITER I SATURN ----------#
########################################


# Definim els paràmetres de Júpiter i Saturn
planets = {
    'Júpiter': {'e': 0.0485, 'varpi_deg': 14.75385 + 180, 'eps_deg': 3.13, 'tau': 14.0, 'period': 4332.59},
    'Saturn':  {'e': 0.0565, 'varpi_deg': 92.43194 + 180, 'eps_deg': 26.73, 'tau': 27.0, 'period': 10759.22},
}

for planet, param in planets.items():
    
    # Realitzem els càlculs necesàris
    e = param['e']
    varpi = np.radians(param['varpi_deg'])
    eps = np.radians(param['eps_deg'])
    tau = param['tau']
    T = param['period']
    days = np.linspace(0, T, 1000)

    M = 2 * np.pi * (days - tau) / T
    E = M.copy()
    for n in range(1, N + 1):
        E += (2 / n) * jn(n, n * e) * np.sin(n * M)

    nu = np.arctan2(np.sqrt(1 - e**2) * np.sin(E), np.cos(E) - e)
    lamb = (nu + varpi) % (2 * np.pi)
    alpha = np.unwrap(np.arctan2(np.cos(eps) * np.sin(lamb), np.cos(lamb)))
    delta = np.arcsin(np.sin(eps) * np.sin(lamb))

    EOT = (M - alpha) * (1440 / (2 * np.pi))
    EOT -= np.mean(EOT)

    # Grafiquem l'analema vist des de Júpiter i Saturn
    H_deg = 15 * (hour + EOT / 60 - 12)
    H_rad = np.radians(H_deg)
    alt = np.degrees(np.arcsin(np.sin(lat_rad) * np.sin(delta) + np.cos(lat_rad) * np.cos(delta) * np.cos(H_rad)))
    az = np.degrees(np.arctan2(-np.sin(H_rad),-np.cos(H_rad)*np.sin(lat_rad) + np.tan(delta)*np.cos(lat_rad))) % 360

    plt.figure(figsize=(10, 8),facecolor='white')
    sc = plt.scatter(az, alt, c=days, cmap='jet', s=100, label='Mart', edgecolors='none')
    cbar = plt.colorbar(sc, label=f'Día del any a {planet}')
    plt.xlabel(r'Az [$\degree$]')
    plt.ylabel(r'Alt [$\degree$]')
    plt.title(f"Analema Solar a {planet} a la Latitud {np.degrees(lat_rad):.1f}° (12h)", fontsize=16)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"informe/images/analema_{planet}.png", dpi=300, bbox_inches='tight')
    plt.show()