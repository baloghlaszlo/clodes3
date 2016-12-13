import requests #pip install requests
from uuid import getnode as get_mac
import time

testid = '1' 

publish_address = "http://127.0.0.1:8080/api/lab_agent/" + testid + "/"
print(publish_address)

if __name__ == "__main__":
    while True:
        try:
            r = requests.put(publish_address)
            print(r)
            print("Post sent")
        except Exception as ex:
            print(ex)
            raise
        time.sleep(1)
