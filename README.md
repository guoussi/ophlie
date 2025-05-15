# Quarto Mastermind IA

**Propriétaire : Guoussi Atatang Ophlie**  
**Matricule : 22318**  
**Date de dernière mise à jour : 15 mai 2025**

Bienvenue sur le projet d’IA Quarto développé par Guoussi Atatang Ophlie (matricule 22318).

Ce projet propose une intelligence artificielle avancée pour le jeu Quarto, capable de rivaliser avec des joueurs humains expérimentés et d’autres IA.

---

## Fonctionnalités principales
- **Client asynchrone** : communication fluide avec un serveur Quarto via JSON.
- **IA stratégique** : Minimax profondeur 3, anticipation des pièges, préférence pour le centre et les coins, évite de donner des pièces gagnantes à l’adversaire.
- **Script de lancement** : démarrage simple et rapide de l’IA.
- **Tests unitaires** : couverture sérieuse pour garantir la fiabilité.
- **Documentation claire** : README, .gitignore, et exemples de configuration.

---

## Lancer l’IA
1. **Prérequis** : Python 3.10 ou supérieur.
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurer vos informations dans `players.json`** (voir exemple ci-dessous).
4. **Démarrer l’IA** :
   ```bash
   python start_player.py
   ```

---

## Exemple de configuration `players.json`
```json
[
  {
    "host": "127.0.0.1",
    "port_server": 3000,
    "port_client": 9001,
    "name": "Guoussi Atatang Ophlie",
    "matricules": ["22318"]
  }
]
```

---

## Structure du projet
- `mastermind_client.py` : client de communication avec le serveur
- `mastermind_ai.py` : logique de l’IA Quarto
- `core_protocol.py` : gestion du protocole JSON
- `run_mastermind.py` : exemple de lancement
- `players.json` : configuration des joueurs
- `test_mastermind_ai.py` : tests unitaires
- `.gitignore`, `requirements.txt`, `README.md` : gestion et documentation

---

## Lancer les tests
Pour vérifier le bon fonctionnement du projet :
```bash
python -m unittest discover -v
```

---

## Auteur
- **Nom** : Guoussi Atatang Ophlie
- **Matricule** : 22318
- **Contact** : [github.com/guoussi](https://github.com/guoussi)

## Licence
Projet original, toute ressemblance avec un autre projet Quarto IA serait fortuite.
