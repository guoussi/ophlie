import json

async def read_json(reader):
    buffer = ''
    while True:
        chunk = await reader.read(1024)
        if not chunk:
            raise Exception('Connection closed')
        buffer += chunk.decode('utf8')
        try:
            return json.loads(buffer)
        except json.JSONDecodeError:
            continue

async def write_json(writer, obj):
    message = json.dumps(obj).encode('utf8')
    writer.write(message)
    await writer.drain()

async def handle_connection(reader, writer, ai_module):
    request = await read_json(reader)
    req_type = request.get('request')
    if req_type == 'ping':
        await write_json(writer, {'response': 'pong'})
    elif req_type == 'play':
        state = request.get('state')
        try:
            move = ai_module.choose_move(state)
            await write_json(writer, {'response': 'move', 'move': move})
        except Exception as e:
            await write_json(writer, {'response': 'error', 'error': str(e)})
    else:
        await write_json(writer, {'response': 'error', 'error': f"Unknown request '{req_type}'"})
    writer.close()
    await writer.wait_closed()
