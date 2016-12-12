import flask
import flask_restful
import time
import os

app = flask.Flask(__name__)

arrived_macs = {}
aggregated_value = 0
publish_address = "http://baprof.net"

@app.route('/api/lab_agent/<mac>/', methods=['POST','PUT'])
def post(mac):
        global arrived_macs
        arrived_macs[mac] = time.time()
        print("mac arrived\t" + str(mac))
        post_update()
        return "200"
        
def post_update():
        global arrived_macs
        global aggregated_value
        import time #wtf
        current_time = time.time()
        remove_keys = []
        currently_aggregated_value = 0
        for mac, time in arrived_macs.items():
            if (time + 10 > current_time):
                currently_aggregated_value += 1
            else:
                remove_keys.append(mac)
        print("Currently Aggregated = " + str(currently_aggregated_value) + "\tLast aggregated = " + str(aggregated_value)) 
        if(currently_aggregated_value != aggregated_value):
            aggregated_value = currently_aggregated_value
            postToAggregator(aggregated_value)

def postToAggregator(aggregated_value):
        try:
            global publish_address
            # Prepare the data
            values = {'agent' : 'LaboratoryAgentAggregator', 'attendance' : str(aggregated_value)}
            data = urllib.parse.urlencode(values)

            # Send HTTP POST request
            req = urllib.request.Request(pubAddress, data.encode('UTF-8'))
            response = urllib.request.urlopen(req)

            html = response.read()

            # Print the result
            print(html)
        except Exception as ex:
            print(ex)
    



if __name__ == '__main__':
    if 'VCAP_SERVICES' in os.environ:
        PORT = int(os.getenv('VCAP_APP_PORT'))
        HOST = str(os.getenv('VCAP_APP_HOST'))
    else:
        PORT = 8080
        HOST = '127.0.0.1'
    print('Starting flask service on {}:{}'.format(HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True)
