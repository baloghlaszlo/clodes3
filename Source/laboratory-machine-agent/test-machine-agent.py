import requests #pip install requests
from uuid import getnode as get_mac
import time
import random

testid = str(random.randint(1,10000))
print(testid)
publish_address = "http://laboratory-machine-agent-aggregator.mybluemix.net/api/lab_agent/" + testid + "/"
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
