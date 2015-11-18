import os
##### SERVER SETTINGS #####
SECRET_KEY = os.urandom(64)
CHALLENGE_NAME = "using_your_head"
PORT = 80
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = "/tmp/flask_session"
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = 604800 # 7 days in seconds
