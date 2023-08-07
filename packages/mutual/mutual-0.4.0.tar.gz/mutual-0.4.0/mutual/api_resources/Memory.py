import requests
import json
import mutual
import io
from typing import List, Union, Tuple

def feed(self, source: Union[str, List[str], Tuple[str, bytes]] = None):
    url = f"{mutual.endpoint}/memories/{self.bot_id}"
    url_text = f"{mutual.endpoint}/memories/{self.bot_id}/text"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    # Check if the source is a file or a list of strings
    if isinstance(source, str):  # Source is a file path
        # Open the file in binary mode
        with open(source, 'rb') as file:
            # Prepare the data payload
            data = {
                'file': file
            }
            # Send the POST request
            response = requests.post(url, files=data, headers=headers)

    elif isinstance(source, list):  # Source is a list of strings
        # Prepare the data payload
        data = {
            'data': source
        }
        # Convert data to json format
        data = json.dumps(data)
        # Send the POST request
        response = requests.post(url_text, data=data, headers=headers)

    elif isinstance(source, tuple):  # Source is (filename, file content)
        filename, file_content = source
        # Prepare the data payload
        data = {
            'file': (filename, io.BytesIO(file_content))  # Create a tuple (filename, file-like object)
        }
        # Send the POST request
        response = requests.post(url, files=data, headers=headers)

    else:
        return "The source type is not supported"

    # Check the response status code and return the appropriate message
    if response.status_code < 300:
        return response.json()
    else:
        return f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"


def get_memory_file_data(grid_fs_id: str):
    url = f"{mutual.endpoint}/memories/{grid_fs_id}/file"

    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code < 300:
        return response.text
    else:
        return f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"

def get_memory_files():
    url = f"{mutual.endpoint}/memories/retrieve_files"

    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code < 300:
        return response.json()
    else:
        return f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"

def view(bot_arg: str):
    url = f"{mutual.endpoint}/memories/{bot_arg}"

    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code < 300:
        return response.json()
    else:
        return f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"