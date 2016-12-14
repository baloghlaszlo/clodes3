import asyncio
import websockets
import urllib
import urllib.request

## Global constans for the server
ip = '127.0.0.1'
port = 5678

pubAddress = "http://baprof.net"

## Currently alive websocket connections
connected = set()

## A counter for optimizing the amount of the REST connections
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
    try:
        # Prepare the data
        values = {'agent' : 'HTML5PortalAgent', 'attendance' : str(len(connected))}
        data = urllib.parse.urlencode(values)

        # Send HTTP POST request
        req = urllib.request.Request(pubAddress, data.encode('UTF-8'))
        response = urllib.request.urlopen(req)

        html = response.read()

        # Print the result
        print(html)
    except Exception as ex:
        print(ex)


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



if __name__ == "__main__":
	#Start the server
	print("starting the server...")
	start_server = websockets.serve(handler, ip, port)
	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()
