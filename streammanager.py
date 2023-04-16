"""
Events

    Types: users, match

"""

import asyncio
import websockets
import json
import logging

logging.basicConfig()

USERS = set()
MATCH = ""

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

def match_event():
    return json.dumps({'type': 'match', 'value': MATCH})

async def stream_overlay(websocket):
    global USERS, MATCH
    try:
        # register and announce user
        USERS.add(websocket)
        websockets.broadcast(USERS, users_event())

        # send current state to user, currently a placeholder
        await websocket.send(match_event())

        # manage state changes
        async for message in websocket:
            event = json.loads(message)
            if event['type'] == 'match':
                MATCH = event['value']
                print(MATCH)
                websockets.broadcast(USERS, match_event())
            else:
                logging.error(f"unsupported event type: {event}")
    
    finally:
        # unregister user
        USERS.remove(websocket)
        websockets.broadcast(USERS, users_event())

async def main():
    async with websockets.serve(stream_overlay, '0.0.0.0', 8001):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())