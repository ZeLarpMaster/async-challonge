import aiohttp
import json
import functools

import dateutil.parser


# TODO: Move into a utilities file
def sanitize_boolean_params(params: dict):
    return {k: (1 if v is True else v) for k, v in params.items()}


# TODO: Move into a utilities file
def prepare_prefixed_params(prefix: str, params: dict):
    result = {}
    for k, v in params.items():
        result["{}[{}]".format(prefix, k)] = v
    return result


# TODO: Move into a utilities file
def flatten_array_params(prefix: str, params: list):
    result = []
    for obj in params:
        for k, v in obj.items():
            result.append(("{}[][{}]".format(prefix, k), v))
    return result


# TODO: Move into a utilities file
def response_object_hook(obj):
    for k, v in obj.items():
        if v is not None:
            if k.endswith("_at"):
                try:
                    parsed = dateutil.parser.parse(v)
                except ValueError:
                    pass
                else:
                    obj[k] = parsed
            if type(v) == str:
                try:
                    parsed = float(v)
                except (ValueError, TypeError):
                    pass
                else:
                    obj[k] = parsed
    return obj

# TODO: Move into a utilities file
response_parser = functools.partial(json.loads, object_hook=response_object_hook)


class ChallongeException(Exception):
    pass


class Unauthorized(ChallongeException):
    def __init__(self):
        self.args = ("Unauthorized (Invalid API key or insufficient permissions)",)


class NotFound(ChallongeException):
    def __init__(self):
        self.args = ("Object not found within your account scope",)


class FormatNotSupported(ChallongeException):
    def __init__(self):
        self.args = ("Requested format is not supported - request JSON or XML only",)


class ValidationError(ChallongeException):
    def __init__(self, response):
        self.args = ("Validation error(s) for create or update method", response)


class ServerError(ChallongeException):
    def __init__(self):
        self.args = ("Something went wrong on our end. If you continually receive this, please contact us.",)


class Challonge:
    def __init__(self, username, api_key):
        self.base_url = "https://api.challonge.com/v1/{{}}.json".format(user=username, key=api_key)
        self.session = aiohttp.ClientSession(auth=aiohttp.BasicAuth(username, api_key))

    async def fetch(self, method, endpoint, params=None):
        """Execute an api call and receive its response"""
        async with self.session.request(method, self.base_url.format(endpoint), params=params) as response:
            if response.status != 200:
                self.raise_exception(response.status, await response.json())
            else:
                return await response.json(loads=response_parser)

    def raise_exception(self, status_code, response_text):
        if status_code == 401:
            raise Unauthorized()
        elif status_code == 404:
            raise NotFound()
        elif status_code == 406:
            raise FormatNotSupported()
        elif status_code == 422:
            raise ValidationError(response_text)
        elif status_code == 500:
            raise ServerError()
        else:
            raise ChallongeException()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.session.close()
