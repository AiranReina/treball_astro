import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.special import jn

# Inicialitzem els paràmetres órbitals dels planetes
planets_test = {
    'Earth': {
        'e': 0.0167,
        'varpi_deg': 102.937348 + 180,
        'eps_deg': 23.44
    },
    'Mercury': {
        'e': 0.2056,
        'varpi_deg': 77.456 + 180,
        'eps_deg': 0.03
    },
    'Mars': {
        'e': 0.0934,
        'varpi_deg': 336.04084 + 180,
        'eps_deg': 25.19
    },
    'Jupiter': {
        'e': 0.0489,
        'varpi_deg': 14.75385 + 180,
        'eps_deg': 3.13
    },
    'Saturn': {
        'e': 0.0565,
        'varpi_deg': 92.43194 + 180,
        'eps_deg': 26.73
    }
}


# Inicialitzem les constants necesàries pel programa
T_orbital_earth = 365.25
tau_test = 1.07
N_terms = 20
days_common = np.linspace(0, T_orbital_earth, 1000)
lat_rad = np.radians(40)
hora_local_p = 12

# Grafiquem els analemes per tots els planetes
plt.style.use('classic')
percent = np.linspace(0, 100, 1000)
fig, axes = plt.subplots(1, 5, figsize=(30, 8), sharey=True, facecolor='white')
eot_dict = {}
radec_dict = {}
for i, (planet, params) in enumerate(planets_test.items()):
    e = params['e']
    varpi = np.radians(params['varpi_deg'])
    eps = np.radians(params['eps_deg'])

    M = 2 * np.pi * (days_common - tau_test) / T_orbital_earth
    E = M.copy()
    for n in range(1, N_terms + 1):
        E += (2 / n) * jn(n, n * e) * np.sin(n * M)

    nu = np.arctan2(np.sqrt(1 - e**2) * np.sin(E), np.cos(E) - e)
    lamb = (nu + varpi) % (2 * np.pi)

    alpha = np.unwrap(np.arctan2(np.cos(eps) * np.sin(lamb), np.cos(lamb)))
    delta = np.arcsin(np.sin(eps) * np.sin(lamb))

    alpha_deg = np.degrees(alpha) % 360
    delta_deg = np.degrees(delta)
    radec_dict[planet] = (alpha_deg, delta_deg)

    EOT_rad = M - alpha
    EOT_min = EOT_rad * (1440 / (2 * np.pi))
    EOT_min -= np.mean(EOT_min)
    eot_dict[planet] = EOT_min.copy()

    H_deg = 15 * (hora_local_p + EOT_min / 60 - 12)
    H_rad = np.radians(H_deg)

    elev = np.degrees(np.arcsin(
        np.sin(lat_rad) * np.sin(delta) +
        np.cos(lat_rad) * np.cos(delta) * np.cos(H_rad)
    ))
    azim = np.degrees(np.arctan2(
        -np.sin(H_rad),
        -np.cos(H_rad) * np.sin(lat_rad) + np.tan(delta) * np.cos(lat_rad)
    )) % 360

    ax = axes[i]
    sc = ax.scatter(azim, elev, c=percent, cmap='jet', s=100, edgecolors='none')
    ax.set_title(planet)
    ax.set_xlabel(r'Az [$\degree$]')
    ax.grid(True)
    if i == 0:
        ax.set_ylabel(r'Alt [$\degree$]')

fig.suptitle(f"Analema Solar per Planeta a Latitud {np.degrees(lat_rad):.1f}° (Inici: 01/01/2025 a {hora_local_p}h)", fontsize=16)
cbar = plt.colorbar(sc, label='Percentatge del any')
cbar.set_ticks([0, 100])
plt.tight_layout()
plt.savefig("informe/images/analema_Planetes.png", dpi=300, bbox_inches='tight')
plt.show()