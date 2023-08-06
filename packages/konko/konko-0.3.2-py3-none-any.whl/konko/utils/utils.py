import os
from fastapi import HTTPException

def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise HTTPException(status_code=400, detail=f"{name} must be set")
    return value

def get_konko_url() -> str:
    konko_url = get_env_variable("KONKO_URL")
    konko_url += "/" if not konko_url.endswith("/") else ""
    return konko_url