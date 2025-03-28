import requests
import configparser
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

def get_room_temperature():
    try:
        url = config.get("temperature", "ubi_temp_url")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Parse the stringified JSON in "last_values"
        raw_values = data.get("channel", {}).get("last_values")
        if isinstance(raw_values, str):
            last_values = json.loads(raw_values)
        elif isinstance(raw_values, dict):
            last_values = raw_values
        else:
            print("null")
            return

        field1 = last_values.get("field1", {})
        temp = field1.get("value")

        if temp is not None:
            print(float(temp))
        else:
            print("null")

    except Exception as e:
        print(f"❌ Error fetching room temperature: {e}")

if __name__ == "__main__":
    get_room_temperature()

