import requests
import asyncio
import websockets
import time
import json
import sys

# Define colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Display Header
print(f"{CYAN} 𝐅 𝐎 𝐑 𝐄 𝐒 𝐓 𝐀 𝐑 𝐌 𝐘 ".center(50))
print(f"{GREEN} 🔗 Telegram: https://t.me/forestarmy   \n")

# Read auth token from data.txt
def get_auth_token():
    try:
        with open("data.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"{MAGENTA}Error: data.txt not found!{RESET}")
        exit(1)

AUTH_TOKEN = get_auth_token()

# API Details
PROFILE_URL = "https://api.gradient.network/api/user/profile"
STATUS_URL = "https://api.gradient.network/api/status"
MQTT_WS_URL = "wss://wss.gradient.network/mqtt"

HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome",
    "Origin": "chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo"
}

# 1️⃣ OPTIONS Preflight Request
def send_options_request():
    options_headers = {
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "authorization",
        "Origin": "chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo"
    }
    response = requests.options(STATUS_URL, headers=options_headers)
    print(f"OPTIONS Response: {response.status_code}, Headers: {response.headers}")

# 2️⃣ GET Request to Fetch API Status
def send_get_request():
    response = requests.get(STATUS_URL, headers=HEADERS)
    print(f"GET Response: {response.status_code}, Data: {response.json()}")

# 3️⃣ WebSocket Connection for MQTT
async def connect_mqtt():
    try:
        async with websockets.connect(MQTT_WS_URL, subprotocols=["mqtt"]) as ws:
            print("WebSocket Connected")
            await asyncio.sleep(2)  # Keep the connection open for testing
            await ws.close()
            print("WebSocket Closed")
    except Exception as e:
        print(f"WebSocket Error: {e}")

# Countdown Timer Function
async def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r{YELLOW}Next request in: {remaining // 60}m {remaining % 60}s...{RESET} ")
        sys.stdout.flush()
        await asyncio.sleep(1)
    print("\n")

# Function to run everything in a loop
async def main_loop():
    while True:
        send_options_request()
        send_get_request()
        await connect_mqtt()
        
        print(f"{CYAN}Waiting 10 minutes before the next request...{RESET}")
        await countdown_timer(600)  # 10-minute countdown

# Run the loop
if __name__ == "__main__":
    asyncio.run(main_loop())
