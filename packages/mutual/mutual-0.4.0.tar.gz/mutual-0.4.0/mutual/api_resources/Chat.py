import requests
import json
import mutual

default_stream_response = {
                        "error": None,
                        "status": "processing",
                        "content": None,
                        "data" : {
                            "bot_data": {
                                "bot_id": None,
                                "new_bot": False,
                                "new_bot_message": "Not a new bot.", 
                                "new_bot_user": False,
                                "new_bot_user_message": "Not a new bot_user.",
                                "material_id": None
                            },
                            "prompt_data": {
                                "prompt_id": None,
                                "judge_id": None,
                                "judge_message_id": None,
                            },
                            "user_data": {
                                "username": None,
                                "tokens_used" : None
                            }
                        },
                    }

def create(content, bot_name=None, username=None, prompt=None, bot_id=None, prompt_id=None,
            judge_id=None, judge_message_id=None, material_id=None,
            error_logs=False, multiplayer_memory = True, judge = False, stream = True,
            recommendations=False,
            context_window = 2):
    
    if bot_id is None:
        bot_id = mutual.bot_id
    if bot_id is None and bot_name is None:
        raise ValueError("bot_id or bot_name must be provided either as argument or set in config")

    url = f"{mutual.endpoint}/chat"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "content": content,
        "bot_id": str(bot_id),
        "bot_name": bot_name,
        "prompt": prompt,
        "username": username,
        "prompt_id": prompt_id,
        "judge_id": judge_id,
        "judge_message_id": judge_message_id,
        "material_id": material_id,
        "multiplayer": multiplayer_memory,
        "context_window": context_window,
        "judge": judge,
        "stream": stream
    }

    if stream:
        return _create_stream(url=url, data=data, headers=headers,error_logs=error_logs)
    else:
        return _create_response(url=url, data=data, headers=headers)

def _create_stream(url=None, data=None, headers=None, error_logs = False):
    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

    if response.status_code < 300:
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                yield line
    else:
        # raise Exception(f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail']}")
        default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_stream_response
    
def _create_response(url=None, data=None, headers=None):
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code < 300:
        return response.json()
    else:
        # raise Exception(f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail']}")
        default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_stream_response


def create_demo(content, prompt=None, error_logs=False, multiplayer_memory = True, context_window = 2):

    url = f"{mutual.endpoint}/test_chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "content": content,
        "prompt": prompt,
        "multiplayer": multiplayer_memory,
        "context_window": context_window
    }

    response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)

    if response.status_code < 300:
        for line in response.iter_lines():
            if line:  # filter out keep-alive new lines
                json_data = json.loads(line)
                if json_data['error'] is not None and not error_logs:
                    continue
                if json_data['content'] =='[close]':
                    continue
                yield json_data
    else:
        # raise Exception(f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail']}")
        default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_stream_response
