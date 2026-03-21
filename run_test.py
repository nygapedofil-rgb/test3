import subprocess
import time
import requests


def start_tunnel():
    subprocess.Popen(
        ['ngrok', 'http', '8000'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )

    time.sleep(2)  # daj ngrokowi czas na start

    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    data = response.json()

    for tunnel in data['tunnels']:
        if tunnel['public_url'].startswith("https"):
            return tunnel['public_url']


url = start_tunnel()
print(url)