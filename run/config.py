import string

PROJECT_ROOT_DIR = '/'.join(__file__.split('/')[:-2])  # todo : use os.path.split()
SRC_ROOT_DIR = "system_expert"
RUN_ROOT_DIR = "run"

HTTP_APP_MODULE = "restful_api"
WSGI_API_VARIABLE_NAME = "api"

WSGI_SERVER_PORT = "8888"
HTTP_SERVER_PORT = "8000"

WSGI_SERVER_ADDRESS = "127.0.0.1"
HTTP_SERVER_ADDRESS = "127.0.0.1"

DATA_DIR = "data"
DATA_BASE_FILE = "database.sqlite3"
CREATE_DATA_BASE_SCRIPT = "create_db.sql"

USER_UUID_LENGTH = 16
USER_UUID_CHARS = string.ascii_letters + string.digits
