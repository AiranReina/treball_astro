# 📘 Guia del repositori: *LLIURAMENT D'INTRODUCCIÓ A L'ASTROFÍSICA — UNDERSTANDING ANALEMMAS*

Aquest repositori conté tot el material generat per al lliurament de l’assignatura **Introducció a l’Astrofísica** (2025), elaborat per l’alumne **Airan Reina Delgado** (NIU: 1670808). Està estructurat en tres parts principals: els scripts de Python per generar analemes, les imatges utilitzades a l’informe, i els arxius per compilar l’informe en LaTeX.

---

## 📁 Estructura del repositori

- `analema.py`: Script en Python que calcula la posició del Sol al llarg de l’any, vist des de la Terra, i genera l'analemma solar. Inclou també el codi necessari per comparar els analemes amb els que es poden observar a l’entrada de la Facultat de Ciències de la UAB.

- `analema_planetes.py`: Extensió del codi anterior per generar analemes vistos des de diferents planetes del sistema solar, considerant l’excentricitat, l’obliqüitat i el període orbital de cada cas.

- `moon.py`: Versió adaptada per generar l’analema lunar, tal com s’observa des de la Terra.

- `informe/images/`: Carpeta que conté totes les imatges generades pels scripts Python, així com altres gràfics utilitzats a l’informe escrit.

- `informe/build/`: Arxius necessaris per a la compilació del document LaTeX que constitueix l’informe final.

---

## 📌 Nota per al corrector

Aquest repositori ha estat dissenyat per facilitar la revisió del treball. Es recomana començar pels scripts `analema.py`, `analema_planetes.py` i `moon.py`, i després consultar les imatges generades a `informe/images/`.