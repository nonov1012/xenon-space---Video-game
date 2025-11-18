from blazyck import *

def calcul_vie(ratio: float) -> int:
    """
    Calcule les points de vie (pv_max) d'un vaisseau selon une constante totale et un ratio.
    
    ratio : rapport entre vie et portée.
            - Si ratio > 1, le vaisseau privilégie la vie.
            - Si ratio < 1, il privilégie la vitesse.
    """
    return int((CSTE * ratio) / (1 + ratio))


def calcul_portee(ratio: float) -> int:
    """
    Calcule la portée (ou vitesse) d'un vaisseau selon une constante totale et un ratio.
    
    ratio : rapport entre vie et portée.
    """
    return int(CSTE / ((1 + ratio) * 10))

def attributs(value, weight):
    return value * weight

# parametre.py
SHIP_STATS = {
    "Lourd": {
        "pv_max": attributs(8, 100),
        "attaque": 200,
        "port_attaque": 10,
        "port_deplacement": attributs(3, 1),
        "cout": 4000,
        "taille": (3, 4),
        "peut_miner": False,
        "peut_transporter": False
    },
    "Moyen": {
        "pv_max": attributs(4, 100),
        "attaque": 100,
        "port_attaque": 5,
        "port_deplacement": attributs(6, 1),
        "cout": 1000,
        "taille": (2, 2),
        "peut_miner": False,
        "peut_transporter": False
    },
    "Petit": {
        "pv_max": attributs(4, 25),
        "attaque": 50,
        "port_attaque": 3,
        "port_deplacement": attributs(40, 1),
        "cout": 250,
        "taille": (1, 1),
        "peut_miner": False,
        "peut_transporter": False
    },
    "Foreuse": {
        "pv_max": attributs(4, 50),
        "port_deplacement": attributs(6, 0.5),
        "cout": 700,
        "taille": (1, 1),
        "peut_miner": True,
        "peut_transporter": False
    },
    "Transport": {
        "pv_max": attributs(4, 150),
        "attaque": 100,
        "port_attaque": 3,
        "port_deplacement": attributs(6, 1.7),
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
            "gain": 400
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
            "gain": 500
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
            "gain": 600
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
    "pv_max": {"min": 10, "max": 2000},
    "attaque": {"min": 0, "max": 500},
    "port_attaque": {"min": 0, "max": 20},
    "port_deplacement": {"min": 0, "max": 15},
    "cout": {"min": 100, "max": 10000},
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
        
def appliquer_modifications_sliders():
    """
    Applique les modifications de vaisseaux_sliders vers SHIP_STATS.
    Convertit taille_largeur et taille_hauteur en tuple taille.
    """
    global SHIP_STATS
    
    for ship_name, params in vaisseaux_sliders.items():
        if ship_name == "MotherShip":
            # Pour MotherShip, parcourir chaque tier
            for tier, tier_params in params.items():
                for key, value in tier_params.items():
                    SHIP_STATS[ship_name][tier][key] = value
        else:
            # Pour les autres vaisseaux
            # Copier tous les paramètres sauf taille_largeur et taille_hauteur
            for key, value in params.items():
                if key == "taille_largeur":
                    # On le traite avec taille_hauteur
                    continue
                elif key == "taille_hauteur":
                    # Reconstruire le tuple taille
                    largeur = params.get("taille_largeur", 1)
                    hauteur = value
                    SHIP_STATS[ship_name]["taille"] = (largeur, hauteur)
                else:
                    SHIP_STATS[ship_name][key] = value
    
    print("✅ Stats des vaisseaux mises à jour depuis vaisseaux_sliders")
    # Debug: afficher les nouvelles stats
    for ship_name, stats in SHIP_STATS.items():
        if ship_name == "MotherShip":
            print(f"  {ship_name}:")
            for tier, tier_stats in stats.items():
                print(f"    Tier {tier}: {tier_stats}")
        else:
            print(f"  {ship_name}: {stats}")