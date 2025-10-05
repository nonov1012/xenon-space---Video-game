# =======================
# Fonction A*
# =======================

from heapq import heappush, heappop

def a_star(start, goal, grille, largeur, hauteur, port_max, cout_case, ignore_self_fn):
    """
    A* pour un vaisseau.
    - start, goal : (ligne, colonne)
    - grille : la grille
    - largeur, hauteur : taille du vaisseau
    - port_max : portée max (coût total)
    - cout_case : dict {Type: coût}
    - ignore_self_fn : fonction (y, x) -> bool pour ignorer collisions
    """
    open_set = []
    heappush(open_set, (0 + manhattan(start, goal), 0, start, [start]))
    visited = {}

    while open_set:
        f_score, g_score, (l, c), path = heappop(open_set)
        if (l, c) in visited and visited[(l, c)] <= g_score:
            continue
        visited[(l, c)] = g_score

        if (l, c) == goal:
            return path, g_score  # chemin et coût

        for dl, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nl, nc = l + dl, c + dc
            if 0 <= nl <= len(grille) - hauteur and 0 <= nc <= len(grille[0]) - largeur:
                # Vérifier collision avec la fonction externe
                if not ignore_self_fn(nl, nc):
                    continue

                max_cost = 0
                valide = True
                for yy in range(nl, nl + hauteur):
                    for xx in range(nc, nc + largeur):
                        t = grille[yy][xx].type
                        if t in cout_case:
                            max_cost = max(max_cost, cout_case[t])
                        elif ignore_self_fn(yy, xx):
                            continue
                        else:
                            valide = False
                            break
                    if not valide:
                        break

                if valide:
                    g_new = g_score + max_cost
                    if g_new <= port_max:
                        f_new = g_new + manhattan((nl, nc), goal)
                        heappush(open_set, (f_new, g_new, (nl, nc), path + [(nl, nc)]))

    return None, float('inf')  # pas de chemin

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])