import os
import json
import configparser
import subprocess
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

hostname = config.get("miner", "hostname")
root_password = config.get("miner", "root_password")
temp_to_power_mapping = json.loads(config.get("temperature", "temp_to_power_mapping"))

CACHE_FILE = os.path.join(script_dir, "last_power_target.json")

def determine_power_target(current_temperature, mapping):
    sorted_map = sorted(mapping.items(), key=lambda x: float(x[0]))
    for threshold, watts in sorted_map:
        if current_temperature <= float(threshold):
            return watts
    return sorted_map[-1][1]

def load_last_power_target():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f).get("last_power_target")
    return None

def save_last_power_target(power_target):
    with open(CACHE_FILE, "w") as f:
        json.dump({"last_power_target": power_target}, f)

def adjust_power_target(host, password, target, last):
    if target == last:
        print(f"✅ Power already at {target}W. No change.")
        return
    print(f"🔧 Setting power target to {target}W...")
    command = (
        f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no root@{host} "
        f"\"busybox sed -i '/\\[autotuning\\]/,/\\[/{{s/power_target = .*/power_target = {target}/}}' /etc/bosminer.toml && "
        f"busybox killall -HUP bosminer\""
    )
    subprocess.run(command, shell=True, check=True)
    save_last_power_target(target)
    print(f"✅ Power target updated.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python thermohash.py <temperature>")
        return

    try:
        temperature = float(sys.argv[1])
    except ValueError:
        print("Invalid temperature.")
        return

    power_target = determine_power_target(temperature, temp_to_power_mapping)
    last_power_target = load_last_power_target()

    print(f"🌡️ Temp: {temperature}°C → ⚡ Target: {power_target}W")
    adjust_power_target(hostname, root_password, power_target, last_power_target)

if __name__ == "__main__":
    main()

