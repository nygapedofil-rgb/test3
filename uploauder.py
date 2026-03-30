import argparse
import sys

import requests



url = "http://192.168.50.143:9000/upload/"
url1 = "http://192.168.50.143:9000/download/"






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download or upload')
    parser.add_argument('-d', '--download', help='file for download')
    parser.add_argument('-u', '--upload', help='file for upload')
    args = parser.parse_args()

    download = args.download
    upload = args.upload
    if download:
        try:
            with requests.post(url1, stream=True, headers={'user-Agent': 'mozilla'}, json={"filename": f'{download}'}) as response:
                response.raise_for_status()  # sprawdza błędy HTTP
                with open(f'{download}', "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # filtr pustych chunków
                            f.write(chunk)
        except Exception as e:
            print(f'unexpected critical error: {e}')
            sys.exit(1)
        print('everything is done')
        sys.exit(0)
    elif upload:
        try:
            with open(f'{upload}', "rb") as f:
                files = {
                    "file": (f'{upload}', f, "text/plain")
                }
                response = requests.post(url, files=files)
            print(response.status_code)
            print(response.text)
        except Exception as e:
            print(f'unexpected critical error: {e}')
            sys.exit(1)
        print('everything is done')
        sys.exit(0)
    else:
        print('no file specified')
        sys.exit(1)



