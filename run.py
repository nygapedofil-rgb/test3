import time

import requests
import subprocess
import json
import argparse
import threading

def send(username,password,file_data:dict):
    url = "http://127.0.0.1:8000/api/login"
    url1 = "http://192.168.50.143:8000/api/update_file"



    response = requests.post(url1, json={"username": str(username), "password": str(password), 'file_data': file_data},timeout=5)
    print(response.status_code)
    print(response.text)
    return response.status_code

def start_serwer():
    try:
        proces = subprocess.Popen(['daphne','-b','0.0.0.0','-p',' 8000','mywebsite.asgi:application'],stdout=None,stderr=None,text=True)
        time.sleep(5)
        if proces.poll() is not None:
            print("Serwer się wywalił")
            print(proces.stderr.read())
        else:
            print('done')
    except Exception as e:
        print(e)
        print('exception')

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
    thread = threading.Thread(target=start_serwer)
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
    args = parser.parse_args()
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
        print('waiting')
        time.sleep(5)

if __name__ == '__main__':
    main()
