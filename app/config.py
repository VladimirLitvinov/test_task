import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT"))

PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"

ALGORITHM = os.environ.get("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
