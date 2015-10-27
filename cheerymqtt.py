import paho.mqtt.client as mqtt
import requests
import time
import re

URL_NAMES = "http://api.thingspeak.com/channels/1417/field/1/last.txt"
URL_RGB = "http://api.thingspeak.com/channels/1417/field/2/last.txt"

MQTT_SERVER = "iot.eclipse.org"
MQTT_PORT = 1883

MQTT_NAME_TOPIC = "spooplights"
MQTT_HEX_TOPIC = MQTT_NAME_TOPIC + "RGB"

LEGAL_NAMES = set(["red", "green", "blue", "cyan", "white", "warmwhite",
               "oldlace", "purple", "magenta", "yellow", "orange",
               "pink"])

POLL_RATE = 5

def get_name():
    request = requests.get(URL_NAMES)

    # Check the colour was received and is a legal colour.
    if request.status_code == requests.codes.ok:
        colour = request.text.lower().strip()
        if colour in LEGAL_NAMES:
            return colour
    return "black"

def get_hex():
    request = requests.get(URL_RGB)

    # Check the colour was received and is a legal colour.
    if request.status_code == requests.codes.ok:
        colour = request.text.upper().strip()
        if re.match(r'^#[0-9A-F]{6,6}$', colour):
            return colour
    return "#000000"

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_NAME_TOPIC)
    client.subscribe(MQTT_HEX_TOPIC)

def on_message(client, userdata, msg):
	print(msg.topic+" "+msg.payload.decode(encoding='UTF-8'))

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    client.loop_start()

    last_name = None
    last_hex = None
    check_time = 0
    while True:
        if time.time() - check_time > POLL_RATE:
            next_name = get_name()
            next_hex = get_hex()

            if next_name != last_name:
                client.publish(MQTT_NAME_TOPIC, next_name)
                last_name = next_name

            if next_hex != last_hex:
                client.publish(MQTT_HEX_TOPIC, next_hex)
                last_hex = next_hex
            check_time = time.time()

    client.loop_stop(force=False)

if __name__ == '__main__':
    main()
