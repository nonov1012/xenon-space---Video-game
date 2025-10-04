# parametre.py
SHIP_STATS = {
    "Lourd": {
        "pv_max": 200,
        "attaque": 50,
        "port_attaque": 5,
        "port_deplacement": 3,
        "cout": 5000,
        "taille": (3, 3),
        "peut_miner": False,
        "peut_transporter": False
    },
    "Moyen": {
        "pv_max": 120,
        "attaque": 30,
        "port_attaque": 3,
        "port_deplacement": 5,
        "cout": 3000,
        "taille": (2, 2),
        "peut_miner": False,
        "peut_transporter": False
    },
    "Petit": {
        "pv_max": 60,
        "attaque": 10,
        "port_attaque": 1,
        "port_deplacement": 8,
        "cout": 1000,
        "taille": (1, 1),
        "peut_miner": False,
        "peut_transporter": False
    },
    "Foreuse": {
        "pv_max": 80,
        "attaque": 5,
        "port_attaque": 1,
        "port_deplacement": 4,
        "cout": 4000,
        "taille": (2, 2),
        "peut_miner": True,
        "peut_transporter": False
    },
    "Transport": {
        "pv_max": 100,
        "attaque": 5,
        "port_attaque": 1,
        "port_deplacement": 6,
        "cout": 2000,
        "taille": (2, 2),
        "peut_miner": False,
        "peut_transporter": True,
        "nb_vaisseaux": 3  # spécifique au transport
    },
    "MotherShip": {
        1: {
            "pv_max": 500,
            "attaque": 0,
            "port_attaque": 0,
            "port_deplacement": 0,
            "cout": 0,
            "taille": (4, 5),
            "peut_miner": False,
            "peut_transporter": False,
            "gain": 300
        },
        2: {
            "pv_max": 700,
            "attaque": 0,
            "port_attaque": 0,
            "port_deplacement": 0,
            "cout": 1000,
            "taille": (4, 5),
            "peut_miner": False,
            "peut_transporter": False,
            "gain": 350
        },
        3: {
            "pv_max": 1200,
            "attaque": 0,
            "port_attaque": 0,
            "port_deplacement": 0,
            "cout": 2000,
            "taille": (4, 5),
            "peut_miner": False,
            "peut_transporter": False,
            "gain": 400
        },
        4: {
            "pv_max": 1600,
            "attaque": 0,
            "port_attaque": 0,
            "port_deplacement": 0,
            "cout": 6000,
            "taille": (4, 5),
            "peut_miner": False,
            "peut_transporter": False,
            "gain": 450
        },
    }
}

# Noms d'affichage pour chaque paramètre (sans accents pour compatibilité police)
noms_affichage = {
    "pv_max": "Vie Max",
    "attaque": "Attaque",
    "port_attaque": "Portee Attaque",
    "port_deplacement": "Portee Deplacement",
    "cout": "Cout",
    "taille_largeur": "Largeur",
    "taille_hauteur": "Hauteur",
    "gain": "Gain",
    "nb_vaisseaux": "Nb Vaisseaux",
    "peut_miner": "Peut Miner",
    "peut_transporter": "Peut Transporter"
}

# Limites des paramètres modifiables pour les sliders
limites_params = {
    "pv_max": {"min": 10, "max": 10000},
    "attaque": {"min": 0, "max": 500},
    "port_attaque": {"min": 0, "max": 20},
    "port_deplacement": {"min": 0, "max": 15},
    "cout": {"min": 100, "max": 20000},
    "taille_largeur": {"min": 1, "max": 10},
    "taille_hauteur": {"min": 1, "max": 10},
    "gain": {"min": 1, "max": 10000},
    "nb_vaisseaux": {"min": 1, "max": 10}       # uniquement Transport
}

# Copie des vaisseaux pour les sliders (valeurs modifiables)
vaisseaux_sliders = {}

for name, params in SHIP_STATS.items():
    # Pour MotherShip, chaque index est un dictionnaire à part
    if name == "MotherShip":
        vaisseaux_sliders[name] = {tier: p.copy() for tier, p in params.items()}
    else:
        # Séparer taille en largeur et hauteur pour les sliders
        copy_params = params.copy()
        if "taille" in copy_params:
            largeur, hauteur = copy_params.pop("taille")
            copy_params["taille_largeur"] = largeur
            copy_params["taille_hauteur"] = hauteur
        vaisseaux_sliders[name] = copy_params