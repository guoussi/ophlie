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

def coups_possibles(plateau):
    return [i for i,v in enumerate(plateau) if v is None]

def pieces_disponibles(plateau, en_attente):
    deja = set(p for p in plateau if p)
    if en_attente:
        deja.add(en_attente)
    return [p for p in toutes_pieces() if p not in deja]

def simule(plateau, pos, piece):
    nouv = list(plateau)
    nouv[pos] = piece
    return nouv

def coup_gagnant(plateau, piece):
    for pos in coups_possibles(plateau):
        if victoire(simule(plateau, pos, piece)):
            return pos
    return None

def piece_dangereuse(plateau, pieces):
    # Retourne les pièces qui permettent à l'adversaire de gagner immédiatement
    dangereuses = set()
    for p in pieces:
        for pos in coups_possibles(plateau):
            if victoire(simule(plateau, pos, p)):
                dangereuses.add(p)
                break
    return list(dangereuses)

def eval_board(plateau):
    # Simple : +1000 si victoire, -1000 si défaite imminente, +10 alignement 3, +5 centre, +2 coin
    if victoire(plateau):
        return 1000
    score = 0
    center = [5, 6, 9, 10]
    corners = [0, 3, 12, 15]
    for c in center:
        if plateau[c]:
            score += 5
    for c in corners:
        if plateau[c]:
            score += 2
    for ligne in lignes_plateau(plateau):
        attrs = [[p[i] for p in ligne if p] for i in range(4)]
        for attr in attrs:
            if len(attr) == 3 and len(set(attr)) == 1:
                score += 10
    return score

def minimax(plateau, en_attente, profondeur=2, maximizing=True):
    if profondeur == 0 or all(v is not None for v in plateau):
        return eval_board(plateau), None, None
    coups = coups_possibles(plateau)
    pieces = pieces_disponibles(plateau, en_attente)
    best_score = float('-inf') if maximizing else float('inf')
    best_move = (None, None)
    for pos in coups:
        plat2 = simule(plateau, pos, en_attente)
        if victoire(plat2):
            score = 1000 if maximizing else -1000
            if maximizing and score > best_score:
                best_score = score
                best_move = (pos, random.choice(pieces))
            elif not maximizing and score < best_score:
                best_score = score
                best_move = (pos, random.choice(pieces))
            continue
        for p2 in pieces:
            score, _, _ = minimax(plat2, p2, profondeur-1, not maximizing)
            if maximizing:
                if score > best_score:
                    best_score = score
                    best_move = (pos, p2)
            else:
                if score < best_score:
                    best_score = score
                    best_move = (pos, p2)
    return best_score, best_move[0], best_move[1]

def choose_move(state):
    plateau = state['board']
    en_attente = state.get('piece')
    if en_attente is None:
        # Premier coup : donner une pièce au hasard
        dispo = pieces_disponibles(plateau, None)
        return {'pos': None, 'piece': random.choice(dispo)}
    # Coup gagnant immédiat ?
    pos_gagne = coup_gagnant(plateau, en_attente)
    if pos_gagne is not None:
        dispo = pieces_disponibles(simule(plateau, pos_gagne, en_attente), None)
        dangereuses = piece_dangereuse(simule(plateau, pos_gagne, en_attente), dispo)
        safe = [p for p in dispo if p not in dangereuses]
        piece = random.choice(safe) if safe else random.choice(dispo)
        return {'pos': pos_gagne, 'piece': piece}
    # Sinon, minimax profondeur 2
    _, pos, piece = minimax(plateau, en_attente, profondeur=2, maximizing=True)
    if pos is None or piece is None:
        coups = coups_possibles(plateau)
        dispo = pieces_disponibles(plateau, en_attente)
        pos = random.choice(coups)
        piece = random.choice(dispo)
    return {'pos': pos, 'piece': piece}
