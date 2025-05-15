import argparse
import asyncio
import importlib
import sys
from core_protocol import read_json, write_json, handle_connection

async def check_server(host, port, timeout=2):
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except (ConnectionRefusedError, asyncio.TimeoutError):
        return False

async def subscribe(host, port_server, port_client, name, matricules):
    if not await check_server(host, port_server):
        print(f"[ERREUR] Serveur {host}:{port_server} injoignable.")
        return False
    try:
        reader, writer = await asyncio.open_connection(host, port_server)
        req = {
            'request': 'subscribe',
            'name': name,
            'port': port_client,
            'matricules': [str(m) for m in matricules]
        }
        await write_json(writer, req)
        resp = await read_json(reader)
        writer.close()
        await writer.wait_closed()
        return resp.get('response') == 'ok'
    except Exception as e:
        print(f"[ERREUR] Abonnement impossible: {e}")
        return False

async def main():
    parser = argparse.ArgumentParser(description='Quarto Mastermind Client')
    parser.add_argument('--host', required=True)
    parser.add_argument('--port-server', type=int, required=True)
    parser.add_argument('--port-client', type=int, required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--matricules', nargs='+', required=True)
    args = parser.parse_args()

    # Import de l'IA
    ai_module = importlib.import_module('mastermind_ai')

    if not await subscribe(args.host, args.port_server, args.port_client, args.name, args.matricules):
        print("[ERREUR] Abonnement au serveur échoué.")
        return

    async def handler(reader, writer):
        await handle_connection(reader, writer, ai_module)

    server = await asyncio.start_server(handler, '0.0.0.0', args.port_client)
    print(f"[OK] Client prêt sur le port {args.port_client}")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêté par l'utilisateur.")
