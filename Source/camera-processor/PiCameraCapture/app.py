import io
import sys
import time
import picamera
import requests

import asyncio

WIDTH = 3328
HEIGHT = 2464
SHRINK_FAC = 2

# api_url = 'https://cbaa-clodes3.eu-gb.mybluemix.net/api/frames'
api_url = 'http://192.168.1.143:8080/api/frames'
camera_id = 0

camera = picamera.PiCamera()
stream = io.BytesIO()
capture = camera.capture_continuous(stream, format='jpeg')

loop = asyncio.get_event_loop()

def sendImage():
    loop.call_later(10, sendImage)

    next(capture)
    stream.truncate()
    stream.seek(0)

    msg = {
        'camera_id': camera_id,
        'camera_timestamp': int(time.time())
    }
    files = {
        'picture': str(stream.read())
    }
    try:
        requests.post(api_url, json=msg, files=files)
    except requests.exceptions.ConnectionError as error:
        print(error)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print('Camera image sent')

loop.call_soon(sendImage)
loop.run_forever()