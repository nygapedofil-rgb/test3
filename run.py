import time
import requests
import subprocess
import json
import argparse
import threading

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

def start_tunel():
    proces = subprocess.Popen(
        ['lt', '--port', '8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in proces.stdout:
        print(line.strip())
        if "https://" in line:
            return line.strip().split()[-1]

    return None

def main():
    parser = argparse.ArgumentParser(description='Simple CLI')
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password')
    args = parser.parse_args()

    thread = threading.Thread(target=start_serwer,daemon=True)
    thread.start()
    time.sleep(10)

    while True:
        value = start_tunel()
        if value:
            print(value)
            break
        else:
            time.sleep(5)
            continue

    username = args.username
    password = args.password

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