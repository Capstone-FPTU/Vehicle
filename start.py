from paho.mqtt import client as mqtt
from common import *
from main import run
import json
import requests
import getmac
import time


def connect() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            mac_address = getmac.get_mac_address()
            print(mac_address)
            print(USERNAME+" Connected successfully")
            x = requests.get(API_ENDPOINT + URI_SEND_NOTI+"?vehicle_code=" + CODE + "&mac_address="+mac_address)
            print(x.status_code)
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(HOST, PORT)
    return client

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    messages = msg.payload.decode("utf-8")
    if((msg.topic == "sc-mavr/vehicle/check-connect") and (messages == "MASTER")):
        client.publish("sc-mavr/server/check-connect",CODE)
    turn_value = ''
    if(msg.topic == "sc-mavr/vehicle/order"):
        data = json.loads(messages)
        if(data["code"] == CODE):
            for key, value in data["theWay"].items():
                if key == "HOME":
                    turn_value = value.upper()
            print(turn_value)
            run(data["theWay"], turn_value)
def start():
    client = connect()
    client.subscribe("sc-mavr/vehicle/check-connect")
    client.subscribe("sc-mavr/vehicle/order")
    client.on_message = on_message
    client.loop_forever()

# START
start()
time.sleep(0.5)

