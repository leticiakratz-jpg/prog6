from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def get_mysql_url() -> str:
    mysql_url = os.getenv("MYSQL_URL")
    if not mysql_url:
        raise ValueError(
            "MYSQL_URL não foi definida. Exemplo: mysql+pymysql://usuario:senha@localhost:3306/festa_ifc"
        )
    return mysql_url


def get_database_url() -> str:
    app_env = os.getenv("APP_ENV", "local").lower()
    if app_env == "production":
        return get_mysql_url()

    sqlite_path = DATA_DIR / "festival_ifc.db"
    return f"sqlite:///{sqlite_path}"
