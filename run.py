import time

import requests
import subprocess
import json
import argparse
import threading

def send(username,password,file_data:dict):
    url = "http://127.0.0.1:8000/api/login"
    url1 = "http://192.168.50.143:8000/api/update_file"


    response = requests.post(url1, json={"username": str(username), "password": str(password), 'file_data': file_data})
    print(response.status_code)
    print(response.text)
    return response.status_code

def start_serwer():
    try:
        proces = subprocess.Popen(['daphne','-b 0.0.0.0','mywebsite.asgi:application'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,universal_newlines=True)
        print(proces.stdout.read())
        print('done')
    except Exception as e:
        print(e)
        print('exception')

def start_tunel():
    try:
        proces = subprocess.Popen(['lt','--port 8000'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,universal_newlines=True)
        print(proces.stdout.read())
        return proces.stdout.read()
    except Exception as e:
        return None

def main():
    parser = argparse.ArgumentParser(description='Simple CLI')
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password')
    thread = threading.Thread(target=start_serwer)
    thread.start()
    thread.join()
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
        value = send(str(username),str(password),{'url':value})
        if value != 200:
            print(value)
            continue
        else:
            print('done')
            break

    while True:
        print('waiting')
        time.sleep(5)

if __name__ == '__main__':
    main()
