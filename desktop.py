import asyncio #utilizat pentru a trasmite informatii de la desktop
import json #utilizat in trasferul de date
import logging
import psutil #biblioteca pentru preluarea informatiilor despre procesele care ruleaza si utilizarea sistemului (CPU, memorie, retea, senzori) in Python.
import sys
import websockets

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def json_to_payload(message):
    return json.dumps(message)

# raporteaza catre web procentul de utilizare CPU, este folosita functia cpu_usage_reporter() continuta de biblioteca psutil
async def cpu_usage_reporter(websocket):
    psutil.cpu_percent()
    while (True):
        await asyncio.sleep(1)
        message = {
            'event': 'cpu',
            'value': psutil.cpu_percent(),
        }
        await websocket.send(json_to_payload(message))
        logger.debug(f'Transmite CPU usage catre server: {message}')

# raporteaza catre web procentul de utilizare RAM, este folosita functia virtual_memory() continuta de biblioteca psutil
async def ram_usage_reporter(websocket):
    psutil.virtual_memory()
    while (True):
        await asyncio.sleep(1)
        message = {
            'event': 'ram',
            'value': psutil.virtual_memory().percent,
        }
        await websocket.send(json_to_payload(message))
        logger.debug(f'Transmite RAM usage catre server: {message}')



async def consumer(message):
    json_message = json.loads(message)
    logger.debug(f'Mesaj server primit: {json_message}')

    if (json_message['event'] == 'beep'):
        print("\a")

# transmiterea unui mesaj beep pentru a confirma transmiterea mesajelor
async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)


async def handler(uri, client_id):
    async with websockets.connect(uri) as websocket:
        message = {
            'event': 'authentication',
            'client_id': client_id,
            'client_mode': 'desktop'
        }
        await websocket.send(json_to_payload(message))

        consumer_task = asyncio.ensure_future(
            consumer_handler(websocket))
        producer_task = asyncio.ensure_future(
            cpu_usage_reporter(websocket))
        producer_task2 = asyncio.ensure_future(
            ram_usage_reporter(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task, producer_task2],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        handler('ws://localhost:8000/ws', sys.argv[1])
    )
