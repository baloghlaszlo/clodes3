import asyncio
import websockets
import requests
import os

publish_address = "https://attendance-aggregator.mybluemix.net/attendance"

## Currently alive websocket connections
connected = set()

## A counter for optimizing the amount of the REST messages
i = 0

async def sendConnectedNumber(websocket):
    global connected
    if(websocket in connected):
        try:
            await websocket.send(str(len(connected)))
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected\t" + str(websocket))
            #Unregister
            connected.remove(websocket)
        print("Currently connected: " + str(len(connected)))
        return

def postToAggregator():
    r = requests.put(publish_address, data = {'source':'html5-attendance-aggregator', 'attendance':len(connected)})


async def handler(websocket, path):
    global connected
    global i
    # Register.
    connected.add(websocket)
    print("New client connected\t" + str(websocket))
    while websocket in connected:
        await asyncio.ensure_future(sendConnectedNumber(websocket))
        await asyncio.sleep(1)
        i = i+1
        if(i == len(connected)):
            i = 0
            postToAggregator()
	
if __name__ == '__main__':
    if 'VCAP_SERVICES' in os.environ:
        PORT = int(os.getenv('VCAP_APP_PORT'))
        HOST = str(os.getenv('VCAP_APP_HOST'))
    else:
        PORT = 8080
        HOST = '127.0.0.1'
        #Start the server
        print("starting the server...")
        start_server = websockets.serve(handler, HOST, PORT)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
