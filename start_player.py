import json
import subprocess
import os
import sys

def main():
    here = os.path.dirname(__file__)
    cfg = os.path.join(here, 'players.json')
    try:
        with open(cfg, encoding='utf8') as f:
            players = json.load(f)
    except Exception as e:
        print(f"Erreur de lecture du fichier players.json: {e}")
        sys.exit(1)
    for p in players:
        cmd = [
            sys.executable, 'mastermind_client.py',
            '--host', p['host'],
            '--port-server', str(p['port_server']),
            '--port-client', str(p['port_client']),
            '--name', p['name'],
            '--matricules', *map(str, p['matricules'])
        ]
        print(f"Lancement de {p['name']} sur le port {p['port_client']}...")
        subprocess.run(cmd, cwd=here)

if __name__ == '__main__':
    main()
