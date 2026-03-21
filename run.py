import time
import requests
import subprocess
import json
import argparse
import threading
proces = ""

class Zyd():
    def __init__(self,username,password,proces):
        self.init_time = time.time()
        self.username = username
        self.password = password
        self.proces =proces

    def send(self,username, password, file_data: dict):
        url1 = "http://192.168.50.143:8000/api/update_file"
        try:
            response = requests.post(url1, json={"username": str(username), "password": str(password),
                                                 'file_data': file_data}, timeout=5)
            print(response.status_code)
            print(response.text)
        except requests.RequestException as e:
            print("Request error:", e)

    def setup(self,proces):
        self.proces = proces


    def __del__(self):
        self.send(self.username, self.password, {'url':''})
        self.proces.kill()
        self.proces.terminate()
        now = time.time()
        print('running time:', now - self.init_time)

def send(username,password,file_data:dict):
    url1 = "http://192.168.50.143:8000/api/update_file"
    try:
        response = requests.post(url1, json={"username": str(username), "password": str(password), 'file_data': file_data}, timeout=5)
        print(response.status_code)
        print(response.text)
        return response.status_code
    except requests.RequestException as e:
        print("Request error:", e)
        return None

def start_serwer():
    global proces
    try:
        proces = subprocess.Popen(
            ['daphne','-b','0.0.0.0','-p','8000','mywebsite.asgi:application'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Czytanie logów w czasie rzeczywistym
        for line in iter(proces.stdout.readline, ''):
            if line:
                print("[SERVER]", line.strip())

        proces.stdout.close()
        proces.wait()
        if proces.returncode != 0:
            print("Serwer zakończył działanie z błędem:", proces.returncode)
        else:
            print("Serwer zakończył działanie poprawnie")
    except Exception as e:
        print("Exception in start_serwer:", e)

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

    return None

def main():
    global proces
    parser = argparse.ArgumentParser(description='Simple CLI')
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password')
    args = parser.parse_args()
    username = args.username
    password = args.password
    runer = Zyd(username,password,'')

    thread = threading.Thread(target=start_serwer,daemon=True)
    thread.start()
    time.sleep(10)
    runer.setup(proces)
    while True:
        value = start_tunnel()
        if value:
            print(value)
            break
        else:
            time.sleep(5)
            continue



    while True:
        data = send(str(username),str(password),{'url':value})
        if data != 200:
            print(data)
            continue
        else:
            print('done')
            break

    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()