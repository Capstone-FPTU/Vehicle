from paho.mqtt import client as mqtt
from common import *
from main import run
import json
import requests
import getmac
import time
from button_start_vehicle import start_button

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
    data = json.loads(msg.payload.decode("utf-8"))
    turn_value = ''
    if(data["code"] == CODE):
        if(msg.topic == "sc-mavr/vehicle/order"):
            for key, value in data["theWay"].items():
                if key == "HOME":
                    turn_value = value.upper()
            run(data["theWay"], turn_value)
        if(msg.topic == "sc-mavr/vehicle/new-order"):
            print("button")
            start_button()
            
def start():
    client = connect()
    client.subscribe("sc-mavr/vehicle/check-connect")
    client.subscribe("sc-mavr/vehicle/order")
    client.subscribe("sc-mavr/vehicle/new-order")
    client.on_message = on_message
    client.loop_forever()

# START
start()
time.sleep(0.5)

