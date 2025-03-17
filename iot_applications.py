import random
import time
import json
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

devices = {
    "light": {"status": "off", "brightness": 0},
    "thermostat": {"temperature": 22, "mode": "auto"},
    "security_camera": {"status": "off", "last_motion": None}
}

# Simulated device actions
def light_control(action, brightness=0):
    if action == "on":
        devices["light"]["status"] = "on"
        devices["light"]["brightness"] = brightness
    elif action == "off":
        devices["light"]["status"] = "off"
        devices["light"]["brightness"] = 0
    return devices["light"]

def thermostat_control(mode, temperature=None):
    if mode in ["auto", "manual"]:
        devices["thermostat"]["mode"] = mode
        if mode == "manual" and temperature is not None:
            devices["thermostat"]["temperature"] = temperature
    return devices["thermostat"]

def camera_control(action):
    if action not in ["on", "off"]:
        return {"error": "Invalid action"}
    devices["security_camera"]["status"] = action
    if action == "on":
        devices["security_camera"]["last_motion"] = None
    return devices["security_camera"]

@app.route('/api/devices', methods=['GET'])
def get_devices():
    return jsonify(devices)

@app.route('/api/light', methods=['POST'])
def update_light():
    data = request.json
    action = data.get('action')
    brightness = data.get('brightness', 0)
    result = light_control(action, brightness)
    return jsonify(result)

@app.route('/api/thermostat', methods=['POST'])
def update_thermostat():
    data = request.json
    mode = data.get('mode')
    temperature = data.get('temperature', None)
    result = thermostat_control(mode, temperature)
    return jsonify(result)

@app.route('/api/camera', methods=['POST'])
def update_camera():
    data = request.json
    action = data.get('action')
    result = camera_control(action)
    return jsonify(result)

@app.route('/api/report', methods=['GET'])
def get_report():
    report = {
        "timestamp": datetime.now().isoformat(),
        "devices": devices,
        "random_metrics": {
            "humidity": random.uniform(30, 70),
            "air_quality": random.choice(["Good", "Moderate", "Unhealthy"])
        }
    }
    return jsonify(report)

def simulate_motion_detection():
    while True:
        time.sleep(random.randint(5, 15))
        if devices["security_camera"]["status"] == "on":
            devices["security_camera"]["last_motion"] = datetime.now().isoformat()

if __name__ == '__main__':
    import threading
    motion_thread = threading.Thread(target=simulate_motion_detection)
    motion_thread.start()
    app.run(host='0.0.0.0', port=5000)