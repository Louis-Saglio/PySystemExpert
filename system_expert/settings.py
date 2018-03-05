import string

import os

DATA_BASE_FILE = os.path.join(os.path.dirname(__file__))

INSTANCE_ID_LENGTH = 16
INSTANCE_ID_CHARS_POOL = string.ascii_letters + string.digits
