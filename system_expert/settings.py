import string

import os

DATA_BASE_FILE = os.path.join(os.path.dirname(__file__))

USER_UUID_LENGTH = 16
USER_UUID_CHARS_POOL = string.ascii_letters + string.digits
