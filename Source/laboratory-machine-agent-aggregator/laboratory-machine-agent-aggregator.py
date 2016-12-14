import flask #pip install flask
import time
import os
import requests #pip install requests
import threading

app = flask.Flask(__name__)

arrived_macs = {}
aggregated_value = 0
publish_address = "https://attendance-aggregator.mybluemix.net/attendance"

@app.route('/api/lab_agent/<mac>/', methods=['POST','PUT'])
def post(mac):
	global arrived_macs
	arrived_macs[mac] = time.time()
	print("mac arrived\t" + str(mac))
	post_update()
	return '201'
        
def post_update():
	global arrived_macs
	global aggregated_value
	import time
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
		print("Sending started")
		r = requests.put(publish_address, data = {'source':'laboratory-machine-agent-aggregator', 'attendance':aggregated_value})
		print("Sending finished")
		
def post_update_every_sec():
    while True:
        time.sleep(1)
        post_update()
		
if __name__ == '__main__':
    if 'VCAP_SERVICES' in os.environ:
        PORT = int(os.getenv('VCAP_APP_PORT'))
        HOST = str(os.getenv('VCAP_APP_HOST'))
    else:
        PORT = 8080
        HOST = '127.0.0.1'
    print('Starting daemon thread for checking the msgs')
    t = threading.Thread(target=post_update_every_sec)
    t.start()
    print('Starting flask service on {}:{}'.format(HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True)
