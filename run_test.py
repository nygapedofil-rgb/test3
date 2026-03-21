import subprocess


def start_tunel():
    proces = subprocess.Popen(
        ['ngrok', 'http', '8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in proces.stdout:
        print(line.strip())
        if "https://" in line:
            return line.strip().split()[-1]


value = start_tunel()
print(value)