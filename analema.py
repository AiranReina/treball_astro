import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jn

# Constants i paràmetres necesàris per la simulació
e = 0.0167
eps_deg = 23.44
eps = np.radians(eps_deg)
varphi_deg = 102.937348 + 180
varphi = np.radians(varphi_deg)
N_terms = 20
tau = 1.07
days = np.linspace(0, 365.25, 1000)

# Calculem l'EoT per la terra
M = 2 * np.pi * (days - tau) / 365.25
E_series = M.copy()
for n in range(1, N_terms + 1):
    E_series += (2 / n) * jn(n, n * e) * np.sin(n * M)
nu = np.arctan2(np.sqrt(1 - e**2) * np.sin(E_series), np.cos(E_series) - e)
lambda_sun_earth = (nu + varphi) % (2 * np.pi)

alpha = np.unwrap(np.arctan2(np.cos(eps) * np.sin(lambda_sun_earth), np.cos(lambda_sun_earth)))
EOT_rad = M - alpha
EOT_min = EOT_rad * (1440 / (2 * np.pi))
EOT_min -= np.mean(EOT_min)

delta = np.arcsin(np.sin(eps) * np.sin(lambda_sun_earth))

x = EOT_min / 4
y = np.degrees(delta)


# Grafiquem l'analema solar en declinació (EoT)
plt.style.use('classic')
plt.figure(figsize=(8, 8), facecolor='white')
sc = plt.scatter(x, y, c=days, cmap='jet', label='Analema solar', s=100, edgecolors='none')
cbar = plt.colorbar(sc)
cbar.set_label('Dia del cicle')
plt.xlabel(r'$t_{aparent}-t_{mitjà}$ [$\degree$]')
plt.ylabel(r'Dec [$\degree$]')
plt.title('Analema solar a la Terra')
plt.grid(True)
plt.tick_params(direction='in', top=True, right=True)
plt.yticks(np.arange(-25, 26, 5))
plt.xticks(np.arange(-5, 6, 1))
plt.tight_layout()
plt.savefig("informe/images/analema_dec_eot.png", dpi=300, bbox_inches='tight')
plt.show()

# Grafiquem l'analema solar en Alt(Az)
lat = np.radians(41.499340)
local_time = 16
H_deg = 15 * (local_time + EOT_min / 60 - 12)
H_rad = np.radians(H_deg)

alt = np.degrees(np.arcsin(np.sin(lat) * np.sin(delta) + np.cos(lat) * np.cos(delta) * np.cos(H_rad)))
az = np.degrees(np.arctan2(
    -np.sin(H_rad),
    -np.cos(H_rad)*np.sin(lat) + np.tan(delta)*np.cos(lat)
))
az = (az) % 360

plt.figure(figsize=(8, 8), facecolor='white')
sc = plt.scatter(az, alt, c=days, cmap='jet', label='Analema solar', s=100, edgecolors='none')
cbar = plt.colorbar(sc)
cbar.set_label('Dia del cicle')
plt.xlabel(r'Az [$\degree$]')
plt.ylabel(r'Alt [$\degree$]')
plt.title(f'Analema solar a Bellaterra (Inici: 01/01/2025 a {local_time}h)')
plt.grid(True)
plt.tick_params(direction='in', top=True, right=True)
plt.tight_layout()
plt.savefig("informe/images/analema_alt_az.png", dpi=300, bbox_inches='tight')
plt.show()

# Grafiquem l'analema solar de la porta de la UAB
hours = [10,11,12,13,14,15,16,17]
plt.figure(figsize=(8, 8), facecolor='white')
for hour in hours:
    local_time = hour
    H_deg = 15 * (local_time + EOT_min / 60 - 12)
    H_rad = np.radians(H_deg)

    alt = np.degrees(np.arcsin(np.sin(lat) * np.sin(delta) + np.cos(lat) * np.cos(delta) * np.cos(H_rad)))
    az = np.degrees(np.arctan2(
        -np.sin(H_rad),
        -np.cos(H_rad)*np.sin(lat) + np.tan(delta)*np.cos(lat)
    ))
    az = (az) % 360
    
    sc = plt.scatter(az, alt, c=days, cmap='jet', s=25, edgecolors='none')
    plt.text(x=az[-1], y=alt[-1]-5, s=f'{hour}h')

plt.xlabel(r'Az [$\degree$]')
plt.ylabel(r'Alt [$\degree$]')
plt.xticks([])
plt.yticks([])
plt.title(f'Analemes solars a Bellaterra de {hours[0]}h a {hours[-1]}h')
plt.grid(True)
plt.tick_params(direction='in', top=True, right=True)
plt.tight_layout()
plt.savefig("informe/images/analema_simUAB.png", dpi=300, bbox_inches='tight')
plt.show()

# Grafiquem l'analema solar de la porta de la UAB invertit
hours = [10,11,12,13,14,15,16,17]
plt.figure(figsize=(10, 8), facecolor='white')
for hour in hours:
    local_time = hour
    H_deg = 15 * (local_time + EOT_min / 60 - 12)
    H_rad = np.radians(H_deg)

    alt = np.degrees(np.arcsin(np.sin(lat) * np.sin(delta) + np.cos(lat) * np.cos(delta) * np.cos(H_rad)))
    az = np.degrees(np.arctan2(
        -np.sin(H_rad),
        -np.cos(H_rad)*np.sin(lat) + np.tan(delta)*np.cos(lat)
    ))
    az = (az) % 360
    
    sc = plt.scatter(az, alt, c=days, cmap='jet', s=25, edgecolors='none')
    plt.text(x=az[-1], y=alt[-1]-3, s=f'{hour}h')

plt.gca().invert_yaxis() #Important! Invertim el eix y!
cbar = plt.colorbar(sc)
cbar.set_label('Dia del cicle')
plt.xlabel(r'Az [$\degree$]')
plt.ylabel(r'Alt [$\degree$]')
plt.xticks([])
plt.yticks([])
plt.title(f'Analemes solars a Bellaterra de {hours[0]}h a {hours[-1]}h (Invertit)')
plt.grid(True)
plt.tick_params(direction='in', top=True, right=True)
plt.tight_layout()
plt.savefig("informe/images/analema_simUAB_invert.png", dpi=300, bbox_inches='tight')
plt.show()