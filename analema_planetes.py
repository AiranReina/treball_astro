import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jn

#Paràmetres necessaris
N_terms = 20
days = np.linspace(0, 365.25, 1000)

#Inicialitzem els paràmetres dels planetes
planets = {
    'Mercuri': {'e': 0.2056, 'varpi_deg': 77.456 + 180, 'eps_deg': 0.03, 'tau': 0.0},
    'Terra': {'e': 0.0167, 'varpi_deg': 102.937348 + 180, 'eps_deg': 23.44, 'tau': 1.07},
    'Mart': {'e': 0.0934, 'varpi_deg': 336.04084 + 180, 'eps_deg': 25.19, 'tau': 16.5},
    'Júpiter': {'e': 0.0484, 'varpi_deg': 14.75385 + 180, 'eps_deg': 3.12, 'tau': 14.0},
    'Saturn': {'e': 0.0542, 'varpi_deg': 92.43194 + 180, 'eps_deg': 26.73, 'tau': 27.0},
}

#Trobem els valors de la declinació i \Delta t (Amb la EoT) per cada planeta ...
#... i després grafiquem l'analema solar allà.
for planet, params in planets.items():
    e_planet = params['e']
    varpi_planet = np.radians(params['varpi_deg'])
    eps_planet = np.radians(params['eps_deg'])
    tau_planet = params['tau']

    #Computem la anomalia mitjana del planeta
    M_planet = 2 * np.pi * (days - tau_planet) / 365.25

    #Computem la anomalia excèntrica del planeta emprant la sèrie de Fourier on ...
    #... els coeficients són funcions de Bessel. Ara ens trobem en una aproximació ...
    #... molt més exacta.
    E_series = M_planet.copy()
    for n in range(1, N_terms + 1):
        E_series += (2 / n) * jn(n, n * e_planet) * np.sin(n * M_planet)

    #Computem la anomalia veritable a partir de la anomalia excèntrica.
    nu = np.arctan2(np.sqrt(1 - e_planet**2) * np.sin(E_series), np.cos(E_series) - e_planet)

    #Trobem la longitud eclíptica i l'ascensió recta del sol per a cada planeta i emprem ...
    #... els valors per trobar la \Delta t (EoT) i la declinació del sol.
    lambda_sun = (nu + varpi_planet) % (2 * np.pi)
    alpha = np.unwrap(np.arctan2(np.cos(eps_planet) * np.sin(lambda_sun), np.cos(lambda_sun)))

    EOT_rad = M_planet - alpha
    EOT_min = EOT_rad * (1440 / (2 * np.pi))
    EOT_min -= np.mean(EOT_min)

    delta = np.arcsin(np.sin(eps_planet) * np.sin(lambda_sun))

    #Transformem les unitats de la declinació i EoT a graus per graficar-los.
    x = EOT_min * 360 / (24 * 60)
    y = np.degrees(delta)

    #Grafiquem l'analema solar a cada planeta.
    plt.style.use('classic')
    plt.figure(figsize=(8, 10), facecolor='white')
    plt.plot(x, y, color = 'r', label=f'Analema a {planet}')
    plt.xlabel(r"$T_{aparent} - T_{mitjà}$ [$\degree$]")
    plt.ylabel(r"$Declinatció$ [$\degree$]")
    plt.title(f'Analema solar a {planet} (2025)')
    ax = plt.gca()
    ax.axhline(y=0, color='black', linewidth=1)
    ax.axvline(x=0, color='black', linewidth=1)
    for spine in ax.spines.values():
        spine.set_visible(True)
    plt.grid(True)
    #plt.text(0.05, 0.95, f'$e = {e_planet:.4f}$\n$\\varepsilon = {np.degrees(eps_planet):.2f}^\\circ$',
         #transform=plt.gca().transAxes, fontsize=15, verticalalignment='top')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"informe/images/analema_{planet}.png", dpi=300, bbox_inches='tight')
    plt.show()
