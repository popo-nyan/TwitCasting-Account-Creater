import json
import time
import hashlib


def calculate_authorize(http_method: str,
                        endpoint: str,
                        session_key: str = "",
                        payload: dict = None) -> str:
    timestamp = str(int(time.time()))
    if payload is None:
        return timestamp + "." + hashlib.md5(str("#&a@0z1.!" + timestamp + http_method + endpoint + session_key).encode()).hexdigest()
    return timestamp + "." + hashlib.md5(str("#&a@0z1.!" + timestamp + http_method + endpoint + session_key + json.dumps(payload)).encode()).hexdigest()


def calculate_tc_ss(device_salt: str,
                    session_key: str) -> str:
    return "dev-" + hashlib.md5(str(device_salt + session_key + "#$!.3a%").encode()).hexdigest()
