from starlette.applications import Starlette    #adaugarea bibliotecii Starlettee utilizata in realizarea conexiunii WebSockets 
from starlette.websockets import WebSocketDisconnect
import json #utilizat in trasferul de date intre conexiunile de retea
import logging
import uvicorn #utilizat in implementarea web server

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Starlette()

websockets = { # o conexiune websocket va fi realizata intre web si desktop
    'web': {},
    'desktop': {},
}


async def receive_json(websocket):
    message = await websocket.receive_text()
    return json.loads(message)


@app.websocket_route('/ws')
async def websocket_endpoint(websocket):
    await websocket.accept()

    # mesaj de autentificare print-un client id
    message = await receive_json(websocket)
    client_mode = message['client_mode']
    client_id = message['client_id']
    websockets[client_mode][client_id] = websocket

    # obtinerea modului oglinda pentru a trasmite mesaje catre client
    mirror_mode = 'web' if client_mode == 'desktop' else 'desktop'

    client_string = f'{client_id}[{client_mode}]'
    logger.info(f'Client conectat: {client_string}')

    while (True):
        try:
            # asteapta un mesaj de la client
            message = await receive_json(websocket)
            logger.debug(f'Mesaj primit de la {client_string}: {message}')

            try:
                # trasmitere catre mirror client
                await websockets[mirror_mode][client_id].send_text(
                    json.dumps(message)
                )
            except KeyError:
                logger.debug(
                    f'Client {client_id}[{mirror_mode}] neconectat'
                )
        except WebSocketDisconnect:
            break

    del websockets[client_mode][client_id]
    await websocket.close()
    logger.info(f'Client deconectat: {client_string}')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
