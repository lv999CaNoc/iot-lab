import Simulator
import paho.mqtt.client as mqtt_client
import time, json

broker = "0661a98ef5224ee5980218c5b4f368fe.s1.eu.hivemq.cloud"
port = 8883
username = 'at170310'
password = 'at170310'

def connect_broker():
    client = mqtt_client.Client(protocol=mqtt_client.MQTTv5)
    client.tls_set(tls_version=mqtt_client.ssl.PROTOCOL_TLS)
    client.username_pw_set(username, password)
    result = client.connect(broker, port)
    return client
 
def main():
    publisher = connect_broker()
    publisher.loop_start()

    try:
        while True:
            temperature = Simulator.simulate_temperature_sensor()
            humidity = Simulator.simulate_humidity_sensor()
            smoke = Simulator.simulate_smoke_sensor()
            gas = Simulator.simulate_gas_sensor()
            light = Simulator.simulate_light_sensor()

            current_time = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime())
            
            house_data = {
                "room_data": {
                    "temperature": {
                        "value": temperature,
                        "unit": "°C"
                    },
                    "humidity": {
                        "value": humidity,
                        "unit": "%"
                    },
                    "smoke": {
                        "value": smoke,
                        "unit": "V"
                    },
                    "gas": {
                        "value": gas,
                        "unit": "ppm"
                    }
                },
                "outdoor_data": {
                    "light": {
                        "value": light,
                        "unit": "V"
                    }
                },
                "timestamp": current_time
            }

            house_payload = json.dumps(house_data)
            publisher.publish("house", house_payload)
            print("[", current_time,"] Published: house data to topic house!")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("Publisher interrupted by user")
    finally:
        publisher.loop_stop()
        publisher.disconnect()
        print("Disconnected publisher from broker safely")

if __name__ == "__main__":
    main()