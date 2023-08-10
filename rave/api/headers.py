from typing import Union

from .utils import timestamp, request_hash

token = None
firebaseToken = None


class Headers:
    def __init__(self, body: Union[dict, str] = None, **kwargs):
        api = kwargs.get("api_version")
        version = kwargs.get("client_version") if kwargs.get("client_version") else "5.5.9"
        ts = timestamp()

        self.headers = {
            "client-version": version,
            "request-hash": request_hash(ts, token, len(body) if body else 0),
            "request-ts": str(ts),
            "wemesh-api-version": api if api else "4.0",
            "wemesh-platform": "android",
            "content-type": "application/json; charset=UTF-8",
            "Host": "api.red.wemesh.ca",
            "user-agent": "Rave/1450 (5.5.9) (Android 9; SM-J701F; samsung j7velte; en)",
            "accept-encoding": "gzip, deflate"
        }

        self.mojo = {
            "x-api-key": "45af6a2e-4c1c-45a5-9874-df1eb3a22fe2"
        }

        self.soboro = {
            "x-parse-app-build-version": "1450",
            "x-parse-app-display-version": version,
            "x-parse-application-id": "83a03c48-0f97-4f01-8a80-f603ea2a2270",
            "x-parse-installation-id": "67f181a4-6714-4859-a1f1-02cb8c3541d1",
            "x-parse-os-version": "9",
            "content-type": "application/json"

        }

        self.agent = {
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
            )
        }

        if token:
            self.headers["authorization"] = f"Bearer {token}"
