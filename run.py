#! /bin/python
import signal
import time
from os import chdir, remove
from subprocess import Popen, DEVNULL

from run.config import *

chdir(SRC_ROOT_DIR)
gunicorn = Popen(
    f"gunicorn -b {WSGI_SERVER_ADDRESS}:{WSGI_SERVER_PORT} {HTTP_APP_MODULE}:{WSGI_API_VARIABLE_NAME}".split(),
    stdout=DEVNULL,
    stderr=DEVNULL
)
chdir(PROJECT_ROOT_DIR)

with open("Caddyfile", 'w') as f:
    with open(f"{RUN_ROOT_DIR}/Caddyfile.template", "r") as t:
        f.write(t.read()
                .replace('http_port', HTTP_SERVER_PORT)
                .replace('wsgi_port', WSGI_SERVER_PORT)
                .replace('http_addr', HTTP_SERVER_ADDRESS)
                .replace('wsgi_addr', WSGI_SERVER_ADDRESS)
                )


caddy = Popen(["caddy"], stdout=DEVNULL, stderr=DEVNULL)


# noinspection PyUnusedLocal
def stop(sig, frame):
    caddy.terminate()
    gunicorn.terminate()
    remove("Caddyfile")
    exit(0)


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
print("Hit CTRL + C to stop the server")
time.sleep(1)  # Time to boot gunicorn and Caddy. Caused a harmful issue in test
print(f"Listening at http(s)://{HTTP_SERVER_ADDRESS}:{HTTP_SERVER_PORT}")
while True:
    time.sleep(1000000)
