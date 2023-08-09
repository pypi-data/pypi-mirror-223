from typing import Union, List
from dataclasses import dataclass
import requests
import os


og_post = requests.post


def post(url, **kwargs):

    api_key = kwargs["data"]["api_key"]

    if api_key == '1e9bcd33784377bff8163eae54a613b5':
        return og_post(url, **kwargs)

    raise Exception(
        'API key invalid. Please vist https://bytez.com to request an api key.')


requests.post = post


@dataclass
class Model:
    # private, requires a mangled name
    def __inference(self, url: str, request_params: dict, api_key) -> bytes:
        files = {}
        data = {}

        for key, value in request_params.items():
            if value is None:
                continue

            if isinstance(value, list):
                # Convert list values to the appropriate format
                for item in value:
                    data.setdefault(key, []).append(str(item))
            elif hasattr(value, 'read') and callable(value.read):
                files[key] = value
            else:
                if not isinstance(value, str):
                    value = str(value)
                    continue

                data[key] = value

        if os.getenv("TEST"):
            url = "http://localhost:8080"

        if not api_key:
            raise Exception(
                'kwarg "api_key" not supplied. Remember to include api_key="your_api_key" when calling a model. To request an API key, please visit https://bytez.com')

        data["api_key"] = api_key

        response = requests.post(url, files=files, data=data)

        if not response.ok:
            raise Exception(f'Request failed with {response.status_code}')

        return response.content
