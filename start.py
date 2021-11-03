from paho.mqtt import client as mqtt
from common import *
from main import run
from button_start_vehicle import start_button
from urllib.request import urlopen
from scan_qr import open_box
import json
import requests
import getmac
import time


def connect() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            mac_address = getmac.get_mac_address()
            print(mac_address)
            print(USERNAME + " Connected successfully")
            x = requests.get(API_ENDPOINT + URI_SEND_NOTI + "?vehicle_code=" + CODE + "&mac_address=" + mac_address)
            print(x.status_code)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(HOST, PORT)
    return client


theWay = ''


def on_message(client, userdata, msg):
    global theWay
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    data = json.loads(msg.payload.decode("utf-8"))
    turn_value = ''
    if (data["code"] == CODE):
        if (msg.topic == "sc-mavr/vehicle/order"):
            theWay = data["theWay"]
            for key, value in theWay.items():
                if key == "HOME":
                    turn_value = value.upper()
            run(theWay, turn_value, CODE, data["turning"], '', data["fullWay"])
        if (msg.topic == "sc-mavr/vehicle/new-order"):
            print("button")
            start_button()
        if (msg.topic == "sc-mavr/vehicle/going-home"):
            for key, value in data["theWay"].items():
                turn_value = value.upper()
                break
            run(data["theWay"], '', CODE, data["turning"], turn_value, data["fullWay"])
        if (msg.topic == "sc-mavr/vehicle/open-box"):
            print('open box')
            value = open_box()
            if value == True:
                oldWay = []
                for key, _ in theWay.items():
                    oldWay.append(key)
                requests.get(API_ENDPOINT + URI_GO_TO_HOME + "?vehicle_code=" + CODE + "&before_node=" + oldWay[
                    len(oldWay) - 2] + "&start_node=" + oldWay[len(oldWay) - 1])


def start():
    client = connect()
    client.subscribe("sc-mavr/vehicle/check-connect")
    client.subscribe("sc-mavr/vehicle/order")
    client.subscribe("sc-mavr/vehicle/new-order")
    client.subscribe("sc-mavr/vehicle/open-box")
    client.subscribe("sc-mavr/vehicle/going-home")
    client.on_message = on_message
    client.loop_forever()


def internet_on():
    try:
        response = urlopen('https://www.google.com/', timeout=1)
        return True
    except:
        return False


# START
while True:
    if internet_on():
        break
start()
time.sleep(0.5)
