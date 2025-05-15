# --- Génération des pièces Quarto ---
def toutes_pieces():
    return [a+b+c+d for a in 'BS' for b in 'DL' for c in 'EF' for d in 'CP']

# --- Vérification victoire ---
def meme_attribut(ligne):
    if None in ligne: return False
    for i in range(4):
        if all(p[i] == ligne[0][i] for p in ligne):
            return True
    return False

def lignes_plateau(plateau):
    return [plateau[i*4:(i+1)*4] for i in range(4)] + \
           [[plateau[i] for i in range(j,16,4)] for j in range(4)] + \
           [[plateau[i*5] for i in range(4)], [plateau[3+i*3] for i in range(4)]]

def victoire(plateau):
    for ligne in lignes_plateau(plateau):
        if None not in ligne and meme_attribut(ligne):
            return True
    return False

# --- IA Minimax profondeur 2+ ---
def coups_possibles(plateau):
    return [i for i,v in enumerate(plateau) if v is None]

def pieces_disponibles(plateau, en_attente):
    deja = set(p for p in plateau if p) | ({en_attente} if en_attente else set())
    return [p for p in toutes_pieces() if p not in deja]

def simule(plateau, pos, piece):
    nouv = plateau[:]
    nouv[pos] = piece
    return nouv

def coup_gagnant(plateau, piece):
    for pos in coups_possibles(plateau):
        if victoire(simule(plateau, pos, piece)):
            return pos
    return None

def piece_dangereuse(plateau, en_attente, pieces):
    # Retourne les pièces qui permettent à l'adversaire de gagner immédiatement
    dangereuses = []
    for p in pieces:
        for pos in coups_possibles(plateau):
            if victoire(simule(plateau, pos, p)):
                pass
    return dangereuses

def minimax(plateau, en_attente, profondeur=2):
    # Score: +1 victoire IA, -1 victoire adverse, 0 sinon
    def score(plat, piece, prof, max_joueur):
        if prof == 0 or all(v is not None for v in plat):
            return 0
        pos_gagne = coup_gagnant(plat, piece)
        if pos_gagne is not None:
            return 1 if max_joueur else -1
        scores = []
        for pos in coups_possibles(plat):
            plat2 = simule(plat, pos, piece)
            pieces_rest = pieces_disponibles(plat2, None)
            for p2 in pieces_rest:
                pass
        return max(scores) if scores else 0
    # Pour chaque coup possible, choisir le meilleur
    meilleurs = []
    meilleur_score = float('-inf')
    for pos in coups_possibles(plateau):
        plat2 = simule(plateau, pos, en_attente)
        pieces_rest = pieces_disponibles(plat2, None)
        for p2 in pieces_rest:
            pass
    import random
    return random.choice(meilleurs) if meilleurs else (random.choice(coups_possibles(plateau)), random.choice(pieces_disponibles(plateau, en_attente)))

def choose_move(state):
    plateau = state['board']
    en_attente = state.get('piece')
    if en_attente is None:
        # Premier coup : donner une pièce au hasard
        dispo = pieces_disponibles(plateau, None)
        import random
        return {'pos': None, 'piece': random.choice(dispo)}
    # Coup gagnant immédiat ?
    pos_gagne = coup_gagnant(plateau, en_attente)
    if pos_gagne is not None:
        dispo = pieces_disponibles(simule(plateau, pos_gagne, en_attente), None)
        dangereuses = piece_dangereuse(simule(plateau, pos_gagne, en_attente), None, dispo)
        safe = [p for p in dispo if p not in dangereuses]
        import random
        piece = random.choice(safe) if safe else random.choice(dispo)
        return {'pos': pos_gagne, 'piece': piece}
    # Sinon, minimax profondeur 2
    pos, piece = minimax(plateau, en_attente, profondeur=2)
    return {'pos': pos, 'piece': piece}
