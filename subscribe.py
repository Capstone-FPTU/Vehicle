# from object.noti_object import NoteNoti
from paho.mqtt import client as mqtt
from object import *
import json
import requests
import getmac
import main

CODE = "VH001"
USERNAME = "vehicle_1"
PASSWORD = "Aa123456789"
HOST = "96cd623ad07c45fb886782e9f77079d2.s1.eu.hivemq.cloud"
PORT = 8883

API_ENDPOINT = "http://localhost:8080"
URI_SEND_NOTI = "/api/vehicle/send-noti"
HEADERS = {'Content-Type': 'application/json'}

def connect() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            mac_address = json.dumps(Login(getmac.get_mac_address()).__dict__)
            print(USERNAME+" Connected successfully")
#             note_noti = NoteNoti("Vehicle connected successfully", "Mac-Address: "+mac_address,{"mac_address": mac_address})
            # r = requests.post(url = API_ENDPOINT + URI_SEND_NOTI, headers=HEADERS, data = json.dumps(note_noti.__dict__))
#             print(r.status_code)
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(HOST, PORT)
    return client

def on_message(client, userdata, msg):
    array = {}

    
#     print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    messages = msg.payload.decode("utf-8")
    if((msg.topic == "sc-mavr/vehicle/check-connect") and (messages == "MASTER")):
        client.publish("sc-mavr/server/check-connect",CODE)
        
    if(msg.topic == "sc-mavr/vehicle/order"):
        data = json.loads(messages)
        if(data["code"] == CODE):
            for key, value in data["theWay"].items():
                if not key[1].isdigit():
                    array[key.upper()] = value.upper()
            
#             print(data["theWay"])
            main.run(array)
            
def start():
    client = connect()
    client.subscribe("sc-mavr/vehicle/check-connect")
    client.subscribe("sc-mavr/vehicle/order")
    client.on_message = on_message
    client.loop_forever()

    
    

