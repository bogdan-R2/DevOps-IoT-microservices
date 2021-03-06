import json
import socket
import time

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

from dotenv import load_dotenv
load_dotenv()

import os
DEBUG_DATA_FLOW = os.environ.get("DEBUG_DATA_FLOW")

influx_db_client = InfluxDBClient(host='sprc3_influxdb', port=8086, database = 'db1', timeout = 100)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("#")

def create_data_object(topic, payload):
    data_obj = {}
    data_obj['measurement'] = 'data'
    data_obj['tags'] = {}
    data_obj['tags']['location'] = topic[0: topic.find('/')]
    data_obj['tags']['station'] = topic[topic.find('/') + 1 :]
    data_obj['time'] = payload['timestamp']
    data_obj['fields'] = {}
    
    for key in payload:
        if key != 'timestamp' and not isinstance(payload[key], str):
            if DEBUG_DATA_FLOW == 'true':
                print(topic.replace('/', '.') + '.' + key, str(round(payload[key], 2)))
            data_obj['fields'][key] = float(payload[key])
    if DEBUG_DATA_FLOW == 'true':
        print("")
    return data_obj

def on_message(client, userdata, msg):
    # convert from bytes to str
    payload = msg.payload.decode()
    # convert from str to dict
    payload = json.loads(payload)
    if DEBUG_DATA_FLOW == 'true':
        print('Received a message by topic [' + msg.topic + ']')
        print('Data timestamp is: ' + payload['timestamp'])

    data = []
    data_obj = create_data_object(msg.topic, payload)
    data.append(data_obj)
    influx_db_client.write_points(data, database='db1', time_precision='s', protocol='json')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

is_reachable = False
pingcounter = 0
while is_reachable is False and pingcounter < 5:
    try:
        client.connect("sprc3_mosquitto", 1883, 60)
        is_reachable = True
    except socket.gaierror as e:
        time.sleep(5)
        pingcounter += 1

client.loop_forever()
