#! /bin/python

from os import chdir, system, remove
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


try:
    input("Hit enter or CTRL + C to stop the server\n")
except KeyboardInterrupt:
    pass
finally:
    system(f"kill {gunicorn.pid} {caddy.pid}")
    remove("Caddyfile")
