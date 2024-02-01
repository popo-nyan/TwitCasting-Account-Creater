import httpx
import string
import secrets
from util import authorizekey_calculating, tc_ss_calculating


def main() -> None:
    user_id = "nyan"
    email_address = "hoge@example.net"
    password = "".join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + "%&$#()") for _ in range(20))
    json_data = {"user_id": user_id, "email": email_address, "name": user_id, "password": password, "lang": "en", "app_id": "TCViewerAndroid", "device_type": "android", "app_version": "5.639", "device_id": secrets.token_hex(16)}
    response = httpx.post(
        url="https://iapi.twitcasting.tv/users/casaccount",
        headers={
            "Host": "iapi.twitcasting.tv",
            "User-Agent": "TCViewerAndroid/5.639 (android; 14; Google Pixel7) Mobile",
            "X-Device-Name": "Google Pixel7",
            "X-System-Version": "14",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Version": "3",
            "X-Authorizekey": authorizekey_calculating(http_method="POST", endpoint="/users/casaccount", payload=json_data),
            "App-Version": "5.639",
            "Appid": "TCViewerAndroid"},
        json=json_data)
    print(response, response.json())
    device_salt, session_key = response.json()["data"]["auth"]["device_salt"], response.json()["data"]["auth"]["session_id"]
    print(device_salt, session_key)
    print(tc_ss_calculating(device_salt=device_salt, session_key=session_key))


if __name__ == "__main__":
    main()
