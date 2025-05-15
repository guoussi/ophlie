import random
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
                dangereuses.append(p)
                break
    return dangereuses

def eval_board(plateau):
    # Score simple : +10 pour chaque alignement de 3, +20 pour centre occupé, +5 pour coin
    score = 0
    center = [5, 6, 9, 10]
    corners = [0, 3, 12, 15]
    for ligne in lignes_plateau(plateau):
        if ligne.count(None) == 1:
            # 3 pièces alignées partageant un attribut
            for i in range(4):
                if ligne[0] and all(p and p[i] == ligne[0][i] for p in ligne if p):
                    score += 10
    for c in center:
        if plateau[c]:
            score += 5
    for c in corners:
        if plateau[c]:
            score += 2
    return score

def minimax(plateau, en_attente, profondeur=3, maximizing=True):
    if profondeur == 0 or all(v is not None for v in plateau):
        return eval_board(plateau), None, None
    coups = coups_possibles(plateau)
    pieces = pieces_disponibles(plateau, en_attente)
    best_score = float('-inf') if maximizing else float('inf')
    best_move = (None, None)
    for pos in coups:
        plat2 = simule(plateau, pos, en_attente)
        for p2 in pieces:
            if maximizing:
                score, _, _ = minimax(plat2, p2, profondeur-1, False)
                if score > best_score:
                    best_score = score
                    best_move = (pos, p2)
            else:
                score, _, _ = minimax(plat2, p2, profondeur-1, True)
                if score < best_score:
                    best_score = score
                    best_move = (pos, p2)
    return best_score, best_move[0], best_move[1]

def choose_move(state):
    plateau = state['board']
    en_attente = state.get('piece')
    if en_attente is None:
        # Premier coup : donner une pièce centrale ou coin si possible
        dispo = pieces_disponibles(plateau, None)
        return {'pos': None, 'piece': random.choice(dispo)}
    # Coup gagnant immédiat ?
    pos_gagne = coup_gagnant(plateau, en_attente)
    if pos_gagne is not None:
        dispo = pieces_disponibles(simule(plateau, pos_gagne, en_attente), None)
        dangereuses = piece_dangereuse(simule(plateau, pos_gagne, en_attente), None, dispo)
        safe = [p for p in dispo if p not in dangereuses]
        piece = random.choice(safe) if safe else random.choice(dispo)
        return {'pos': pos_gagne, 'piece': piece}
    # Sinon, minimax profondeur 3
    _, pos, piece = minimax(plateau, en_attente, profondeur=3, maximizing=True)
    if pos is None or piece is None:
        # fallback
        coups = coups_possibles(plateau)
        dispo = pieces_disponibles(plateau, en_attente)
        pos = random.choice(coups)
        piece = random.choice(dispo)
    return {'pos': pos, 'piece': piece}
