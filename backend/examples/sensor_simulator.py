#!/usr/bin/env python3
"""
Simple sensor simulator that sends mock data to the platform.
Useful for testing without physical sensors.
"""

import requests
import time
import random
from datetime import datetime
import uuid

API_URL = "http://localhost:8000/api"
DEVICE_ID = str(uuid.uuid4())

def create_device(token):
    """Register a sensor device"""
    response = requests.post(
        f"{API_URL}/indoor/devices",
        json={
            "label": "Demo Living Room Sensor",
            "location_lat": 40.7128,
            "location_lon": -74.0060,
            "indoor": True,
            "firmware_version": "1.0.0"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error creating device: {response.text}")
        return None

def send_reading(device_id):
    """Send a simulated sensor reading"""
    reading = {
        "device_id": device_id,
        "ts": datetime.utcnow().isoformat() + "Z",
        "pm25": round(random.uniform(8.0, 25.0), 2),
        "pm10": round(random.uniform(15.0, 40.0), 2),
        "co2": round(random.uniform(400, 1200), 1),
        "voc_index": round(random.uniform(80, 150), 1),
        "temp": round(random.uniform(20.0, 26.0), 1),
        "humidity": round(random.uniform(40.0, 65.0), 1)
    }
    
    response = requests.post(
        f"{API_URL}/indoor/readings",
        json=reading
    )
    
    if response.status_code == 200:
        print(f"✓ Sent reading: PM2.5={reading['pm25']}, CO2={reading['co2']}, Temp={reading['temp']}°C")
    else:
        print(f"✗ Error sending reading: {response.text}")

def main():
    print("Sensor Simulator")
    print("================")
    
    # Get authentication token
    email = input("Enter your email (or press Enter to use test@example.com): ").strip()
    if not email:
        email = "test@example.com"
    
    password = input("Enter password (or press Enter to use 'password'): ").strip()
    if not password:
        password = "password"
    
    # Try to login
    print("\nAttempting login...")
    response = requests.post(
        f"{API_URL}/auth/login",
        data={"username": email, "password": password}
    )
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        print("You may need to register first at http://localhost:3000")
        return
    
    token = response.json()["access_token"]
    print("✓ Login successful")
    
    # Create or use existing device
    device_id_input = input("\nEnter device UUID (or press Enter to create new): ").strip()
    if device_id_input:
        device_id = device_id_input
        print(f"Using device: {device_id}")
    else:
        print("Creating new device...")
        device_id = create_device(token)
        if not device_id:
            return
        print(f"✓ Created device: {device_id}")
    
    # Send readings periodically
    print(f"\nSending readings every 60 seconds (Ctrl+C to stop)...")
    try:
        while True:
            send_reading(device_id)
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n\nStopped sensor simulator")

if __name__ == "__main__":
    main()
