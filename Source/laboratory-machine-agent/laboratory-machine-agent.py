import requests #pip install requests
from uuid import getnode as get_mac
import time

publish_address = "http://127.0.0.1:8080/api/lab_agent/" + str(get_mac()) + "/"
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
