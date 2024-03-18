import httpx
import string
import random
import secrets

from utils import calculate_authorize


def main(email_address: str,
         password: str = "".join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + "%&$#()") for _ in range(20)),
         user_id: str = random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
         ) -> tuple:
    json_data = {"user_id": user_id, "email": email_address, "name": user_id, "password": password, "lang": "en", "app_id": "TCViewerAndroid", "device_type": "android", "app_version": "5.639", "device_id": secrets.token_hex(16)}
    headers = {
        "Host": "iapi.twitcasting.tv",
        "User-Agent": "TCViewerAndroid/5.639 (android; 14; Google Pixel7) Mobile",
        "X-Device-Name": "Google Pixel7",
        "X-System-Version": "14",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Version": "3",
        "X-Authorizekey": calculate_authorize(http_method="POST", endpoint="/users/casaccount", payload=json_data),
        "App-Version": "5.639",
        "Appid": "TCViewerAndroid"}
    
    response = httpx.post(
        url="https://iapi.twitcasting.tv/users/casaccount",
        headers=headers,
        json=json_data)
    print(response.status_code)
    
    device_salt, session_key = response.json()["data"]["auth"]["device_salt"], response.json()["data"]["auth"]["session_id"]
    print(device_salt, session_key)
    
    headers["Userid"] = f"c:{user_id}"
    headers["Sessionkey"] = session_key
    headers["X-Authorizekey"] = calculate_authorize(http_method="POST", endpoint="/privacy_policy/agree", session_key=session_key)
    response_agree = httpx.post(
        url="https://iapi.twitcasting.tv/privacy_policy/agree",
        headers=headers)
    print(response_agree.status_code)
    
    headers["X-Authorizekey"] = calculate_authorize(http_method="POST", endpoint="/verify_age", payload={"over20": True}, session_key=session_key)
    response_verify_age = httpx.post(
        url="https://iapi.twitcasting.tv/verify_age",
        headers=headers,
        json={"over20": True})
    print(response_verify_age.status_code)
    return user_id, email_address, password


if __name__ == "__main__":
    main(email_address="cat@example.com")
