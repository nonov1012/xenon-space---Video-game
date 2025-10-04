# parametre.py
vaisseaux = {
    "Lourd": {
        "prix": 5000,
        "distance_deplacement": 3,
        "distance_attaque": 5,
        "degats": 50
    },
    "Moyen": {
        "prix": 3000,
        "distance_deplacement": 5,
        "distance_attaque": 3,
        "degats": 30
    },
    "Petit": {
        "prix": 1000,
        "distance_deplacement": 8,
        "distance_attaque": 1,
        "degats": 10
    },
    "Foreuse": {
        "prix": 4000,
        "distance_deplacement": 4,
        "rapport_argent": 50
    },
    "Transport": {
        "prix": 2000,
        "distance_deplacement": 6,
        "nb_vaisseaux": 3
    }
}

# Limites min/max pour chaque type de paramètre
limites_params = {
    "prix": {"min": 500, "max": 10000},
    "distance_deplacement": {"min": 1, "max": 15},
    "distance_attaque": {"min": 1, "max": 100},
    "degats": {"min": 5, "max": 100},
    "rapport_argent": {"min": 10, "max": 200},
    "nb_vaisseaux": {"min": 1, "max": 10}
}

# Copie des vaisseaux pour les sliders (valeurs modifiables)
vaisseaux_sliders = {name: params.copy() for name, params in vaisseaux.items()}