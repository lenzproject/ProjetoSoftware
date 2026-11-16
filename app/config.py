import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("Defina SECRET_KEY no arquivo .env")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "0") == "1"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    DB_HOST = "cmwioq2ap03o401msdikbv3n0-addon-mysql"
    DB_PORT = "3306"
    DB_NAME = "ethiodeploy"
    DB_USER = "ethiodeploy"
    DB_PASSWORD = "06a8410568563a7a71e6f3a46957e23d506a7a38930564f1"