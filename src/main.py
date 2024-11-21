import hashlib
import json
import random
import secrets
import string
import time
import httpx


class Client:
    def __init__(self):
        self.__session = httpx.Client(base_url="https://iapi.twitcasting.tv")
        self.device_id = secrets.token_hex(16)
        self._headers: dict[str, str] = {
            "Host": "iapi.twitcasting.tv",
            "User-Agent": self.user_agent,
            "X-Device-Name": self.device_name,
            "X-System-Version": self.system_version,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Version": "3",
            "App-Version": self.app_version,
            "Appid": self.app_version,
        }

    @property
    def app_id(self) -> str:
        return "TCViewerAndroid"

    @property
    def app_version(self) -> str:
        return "5.369"

    @property
    def device_type(self) -> str:
        return "android"

    @property
    def device_name(self) -> str:
        return "Google Pixel7"

    @property
    def system_version(self) -> str:
        return "14"

    @property
    def system_language(self) -> str:
        return "en"

    @property
    def user_agent(self) -> str:
        return f"{self.app_id}/{self.app_version} ({self.device_type}; {self.system_version}; {self.device_name}) Mobile"

    @staticmethod
    def _calculate_authorize(
        http_method: str,
        endpoint: str,
        session_key: str = "",
        payload: dict | None = None,
    ) -> str:
        timestamp = str(int(time.time()))
        data = "#&a@0z1.!" + timestamp + http_method.upper() + endpoint + session_key
        if payload is not None:
            data += json.dumps(payload)

        return timestamp + "." + hashlib.md5(data.encode()).hexdigest()

    @staticmethod
    def _calculate_tc_ss(device_salt: str, session_key: str) -> str:
        return (
            "dev-"
            + hashlib.md5((device_salt + session_key + "#$!.3a%").encode()).hexdigest()
        )

    def register(
        self, email_address: str, password: str, user_id: str
    ) -> dict[str, bool | str]:
        json_data = {
            "user_id": user_id,
            "email": email_address,
            "name": user_id,
            "password": password,
            "lang": self.system_language,
            "app_id": self.app_id,
            "device_type": self.device_type,
            "app_version": self.app_version,
            "device_id": self.device_id,
        }
        self._headers["X-Authorizekey"] = self._calculate_authorize(
            http_method="post", endpoint="/users/casaccount", payload=json_data
        )

        response = self.__session.post(
            "/users/casaccount",
            headers=self._headers,
            json=json_data,
        )

        if response.status_code == 200 and response.json()["status_code"] == 201:
            return {
                "success": True,
                "userId": user_id,
                "emailAddress": email_address,
                "password": password,
                "deviceSalt": response.json()["data"]["auth"]["device_salt"],
                "sessionKey": response.json()["data"]["auth"]["session_id"],
            }
        else:
            return {"success": False}

    def agree_privacy_policy(self, user_id: str, session_key: str) -> dict[str, bool]:
        self._headers["Userid"] = f"c:{user_id}"
        self._headers["Sessionkey"] = session_key
        self._headers["X-Authorizekey"] = self._calculate_authorize(
            http_method="post",
            endpoint="/privacy_policy/agree",
            session_key=session_key,
        )
        response = self.__session.post("/privacy_policy/agree", headers=self._headers)

        if response.status_code == 200 and response.json()["status_code"] == 200:
            return {"success": True}
        else:
            return {"success": False}

    def verify_age(self, session_key: str) -> dict[str, bool]:
        self._headers["X-Authorizekey"] = self._calculate_authorize(
            http_method="post",
            endpoint="/verify_age",
            session_key=session_key,
            payload={"over20": True},
        )

        response = self.__session.post(
            "/verify_age",
            headers=self._headers,
            json={"over20": True},
        )

        if response.status_code == 200 and response.json()["status_code"] == 200:
            return {"success": True}
        else:
            return {"success": False}


def main():
    client = Client()
    email_address = "cat@example.com"
    password = "".join(
        secrets.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits + "%&$#()"
        )
        for _ in range(20)
    )
    user_id = "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(15)
    )

    result_register = client.register(email_address, password, user_id)
    print(result_register)

    result_agree_privacy_policy = client.agree_privacy_policy(
        user_id, result_register["sessionKey"]
    )
    print(result_agree_privacy_policy)

    result_verify_age = client.verify_age(result_register["sessionKey"])
    print(result_verify_age)


if __name__ == "__main__":
    main()
