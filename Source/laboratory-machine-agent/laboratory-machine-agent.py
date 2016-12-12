import urllib
import urllib.request
from uuid import getnode as get_mac
import time

pubAddress = "http://baprof.net"

if __name__ == "__main__":
    while True:
        try:
            print(get_mac())
            # Prepare the data
            values = {'agent' : 'LaboratoryMachine', 'mac' : str(get_mac())}
            data = urllib.parse.urlencode(values)

            # Send HTTP POST request
            req = urllib.request.Request(pubAddress, data.encode('UTF-8'))
            response = urllib.request.urlopen(req)

            html = response.read()

            # Print the result
            print(html)
        except Exception as ex:
            print(ex)
        time.sleep(1)
