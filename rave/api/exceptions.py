class APIError(Exception):
    ...


class Unknown(APIError):
    ...


class SlowDown(APIError):
    ...


class InvalidEmailAddress(APIError):
    ...


def handle_exception(data: dict = None):
    code = data.get("error", {}).get("code", 666) if "code" not in list(data.keys()) else data.get("code", 666)
    raise {
        2015: SlowDown,
        900: InvalidEmailAddress
    }.get(code, Unknown)(data)
