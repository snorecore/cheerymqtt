import paho.mqtt.client as mqtt

MQTT_SERVER = "iot.eclipse.org"
MQTT_PORT = 1883

MQTT_NAME_TOPIC = "spooplights"
MQTT_HEX_TOPIC = MQTT_NAME_TOPIC + "RGB"

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
    client.loop_forever()

if __name__ == '__main__':
    main()
