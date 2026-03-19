import time
import requests
import subprocess
import argparse
import threading
import sys

def send(username, password, file_data: dict, base_url):
    try:
        response = requests.post(
            f"{base_url}/api/update_file",
            json={
                "username": username,
                "password": password,
                "file_data": file_data
            },
            timeout=5
        )
        print("[SEND]", response.status_code, response.text)
        return response.status_code
    except requests.RequestException as e:
        print("[SEND] Request error:", e)
        return None

def run_process(name, command, stop_event=None, capture_url=False):
    url_found = None
    try:
        proces = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in iter(proces.stdout.readline, ''):
            if line:
                line = line.strip()
                print(f"[{name}]", line)
                if capture_url and "https://" in line and url_found is None:
                    url_found = line.split()[-1]

            if stop_event and stop_event.is_set():
                proces.terminate()
                break

        proces.stdout.close()
        proces.wait()
    except Exception as e:
        print(f"[{name}] Exception:", e)

    return url_found

def start_serwer(stop_event):
    return run_process(
        "SERVER",
        ['daphne', '-b', '0.0.0.0', '-p', '8000', 'mywebsite.asgi:application'],
        stop_event=stop_event
    )

def start_tunel(stop_event):
    return run_process(
        "TUNNEL",
        ['lt', '--port', '8000'],
        stop_event=stop_event,
        capture_url=True
    )

def main():
    parser = argparse.ArgumentParser(description='Simple CLI')
    parser.add_argument('-u', '--username', required=True, help='username')
    parser.add_argument('-p', '--password', required=True, help='password')
    args = parser.parse_args()

    username = args.username
    password = args.password

    stop_event = threading.Event()

    # Start serwera w wątku
    server_thread = threading.Thread(target=start_serwer, args=(stop_event,), daemon=True)
    server_thread.start()
    time.sleep(5)  # daj serwerowi czas na start

    # Start tunelu i pobranie URL
    tunnel_url = None
    while tunnel_url is None:
        tunnel_url = start_tunel(stop_event)
        if tunnel_url is None:
            print("[MAIN] Tunel nie wystartował, ponawiam w 5s...")
            time.sleep(5)

    print("[MAIN] Tunel URL:", tunnel_url)

    # Serwer docelowy, do którego wysyłamy URL tunelu
    base_url = "http://192.168.50.143:8000"

    # Wysyłka URL tunelu do serwera
    while True:
        print("[MAIN] Wysyłanie URL tunelu do serwera docelowego")
        status = send(username, password, {'url': tunnel_url}, base_url=base_url)
        if status == 200:
            print("[MAIN] URL tunelu wysłany pomyślnie")
            break
        else:
            print(f"[MAIN] Błąd wysyłki: {status}, retry za 5s...")
            time.sleep(5)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("[MAIN] Zatrzymywanie procesów...")
        stop_event.set()
        server_thread.join()
        sys.exit(0)

if __name__ == '__main__':
    main()