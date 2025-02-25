import machine
import time
import network
import dht
import urequests

# WiFi Credentials (Gantilah dengan cara yang lebih aman)
WIFI_SSID = "jawir"
WIFI_PASSWORD = "jancoktenan"

# API Endpoint
API_URL = "http://192.168.0.117:5000/save"  # Flask API
UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/algebra/"

# Ubidots Token (Gantilah dengan lebih aman)
UBIDOTS_TOKEN = "BBUS-DXUb2KGD3lH8hkKyfJyQgwqXaMlX2M"

# Inisialisasi WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to WiFi", end="")
    timeout = 10  # Batas waktu koneksi dalam detik
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("\nWLAN is connected!")
        print(f"IP Address: {wlan.ifconfig()[0]}")
    else:
        print("\nFailed to connect to WiFi!")
        return False
    return True

# Periksa apakah WiFi tersambung
if not connect_wifi():
    print("Restarting...")
    machine.reset()  # Restart perangkat jika WiFi gagal tersambung

# Inisialisasi Sensor DHT11 di GPIO22
sensor = dht.DHT11(machine.Pin(22))

# Fungsi untuk mengirim data ke Flask dan Ubidots
def send_data():
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print(f"Temperature: {temp}°C")
        print(f"Humidity: {hum}%")

        data = {
            "temperature": temp,
            "humidity": hum
        }

        headers = {"Content-Type": "application/json"}
        
        # Kirim ke Flask API
        try:
            response = urequests.post(API_URL, json=data, headers=headers)
            print(f"Flask Response: {response.status_code} {response.text}")
            response.close()
        except Exception as e:
            print(f"Error sending to Flask: {e}")

        # Kirim ke Ubidots
        ubidot_headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": UBIDOTS_TOKEN
        }
        try:
            response = urequests.post(UBIDOTS_URL, json=data, headers=ubidot_headers)
            print(f"Ubidots Response: {response.status_code} {response.text}")
            response.close()
        except Exception as e:
            print(f"Error sending to Ubidots: {e}")

    except Exception as e:
        print(f"Sensor Error: {e}")

# Loop utama
while True:
    if not network.WLAN(network.STA_IF).isconnected():
        print("WiFi disconnected, reconnecting...")
        connect_wifi()
    send_data()
    time.sleep(10)
