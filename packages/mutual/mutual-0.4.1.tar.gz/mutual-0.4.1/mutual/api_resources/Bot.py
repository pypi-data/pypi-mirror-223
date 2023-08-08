import requests
import json
import mutual
import io
from typing import List, Union, Tuple

bot_default_response = {
            "bot_id": None,
            "bot_name": None,
            "bot_chat_index": None,
            "prompt_id": None,
            "judge_id": None,
            "judge_message_id": None,
            "material_id": None,
            "details": None
        }

def get_bots(limit=20, offset=0):
    url = f"{mutual.endpoint}/bots?limit={limit}&offset={offset}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def get_bot(bot_arg):
    url = f"{mutual.endpoint}/bots/{str(bot_arg)}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    # response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def create_bot(bot_name=None, prompt=None, prompt_id = "default", judge_id="default", 
            judge_message_id="default", materiald_id="default", template=None, subject=None):
    
    url = f"{mutual.endpoint}/bots"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "bot_name": bot_name,
        "prompt": prompt,
        "prompt_id": prompt_id or "default",
        "judge_id": judge_id or "default",
        "judge_message_id": judge_message_id or "default",
        "material_id": materiald_id or "default",
        "template": template,
        "subject": subject
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response

def update_bot(bot_id=None, bot_name=None, prompt_id=None, judge_id=None, 
               judge_message_id=None, material_id=None, subject=None):
    
    url = f"{mutual.endpoint}/bots/{str(bot_id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "bot_name": bot_name,
        "prompt_id": prompt_id,
        "judge_id": judge_id,
        "judge_message_id": judge_message_id,
        "material_id": material_id,
        "subject": subject
    }
    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        bot_default_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return bot_default_response


class Bot:
    def __init__(self, api_key, bot_id=None, bot_name=None, prompt_id = "default", 
                 judge_id="default", judge_message_id="default", material_id="default"):
        
        self.api_key = api_key
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.prompt_id = prompt_id
        self.judge_id = judge_id
        self.judge_message_id = judge_message_id
        self.material_id = material_id

        self.flow = False

        self.default_stream_response = {
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
                                "judge_message_id": None
                            },
                            "user_data": {
                                "username": None,
                                "tokens_used" : None
                            }
                        },
                    }

    def update_bot(self,  bot_name=None, prompt=None, prompt_id=None, judge_id=None, judge_message_id=None, material_id=None, subject=None):
        url = f"{mutual.endpoint}/bots/{str(self.bot_id)}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "bot_name": bot_name,
            "prompt": prompt,
            "prompt_id": prompt_id,
            "judge_id" : judge_id,
            "judge_message_id" : judge_message_id,
            "material_id": material_id,
            "subject": subject
        }
        # remove keys with None value
        data = {k: v for k, v in data.items() if v is not None}
        response = requests.patch(url, data=json.dumps(data), headers=headers)
        if response.status_code < 300:
            return response.json()
        else:
            self.default_stream_response["content"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
            return self.default_stream_response

    def chat(self, content=None, username=None, prompt=None, multiplayer_memory = True, context_window = 2, 
            flow=False, error_logs=False, stream=True, judge=True, recommendations=False):
        
        url = f"{mutual.endpoint}/chat"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "content": content,
            "bot_id": str(self.bot_id),
            "bot_name": self.bot_name,
            "prompt": prompt,
            "username": username,
            "prompt_id": self.prompt_id,
            "judge_id": self.judge_id,
            "judge_message_id": self.judge_message_id,
            "material_id": self.material_id,
            "multiplayer": multiplayer_memory,
            "context_window": context_window,
            "recommendations": recommendations,
            "stream": stream,
            "judge": judge,
        }
        
        if flow or stream:
            return self._chat_stream(content=content, username=username, prompt=prompt, multiplayer_memory=multiplayer_memory,
                                     context_window=context_window,flow=flow,error_logs=error_logs,
                                     url=url, headers=headers, data=data, stream = stream, recommendations=recommendations)
        else:
            return self._chat_response(content=content, flow=flow, url=url, headers=headers, data=data)
        
    def _chat_stream(self, content=None, username=None, prompt=None, multiplayer_memory = True, context_window = 2, 
            flow=False, error_logs=False, url = None, headers = None, data = None, stream= True, recommendations=False):
        
        if not content:
            print("Please add a message to the content.")
            print("\n\n", end="", flush=True)
            if flow or self.flow:
                new_content = input("Please enter a new response or type exit to exit: ")
                if new_content.strip().lower() == "exit":
                    return
                for msg in self.chat(content=new_content, username=username, prompt=prompt, multiplayer_memory=multiplayer_memory,
                                    context_window=context_window, flow=flow, stream=stream, recommendations=recommendations):
                    yield msg
            return self.default_stream_response
        
        data['stream'] = True
        response = requests.post(url, data=json.dumps(data), headers=headers, stream=stream)

        if response.status_code < 300:
            # add the newly created bot to the bot class
            for line in response.iter_lines():
                if line:  # filter out keep-alive new lines
                    yield line
            
            if flow or self.flow:
                print("\n\n", end="", flush=True)
                new_content = input("Please enter a new response or type exit to exit: ")
                if new_content.strip().lower() == "exit":
                    return
                for msg in self.chat(content=new_content, username=username, prompt=prompt, 
                                     multiplayer_memory=multiplayer_memory, context_window=context_window, 
                                     flow=flow, stream=stream, recommendations=recommendations):
                    yield msg
        else:
            self.default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
            print(f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}")
            return self.default_stream_response

    def _chat_response(self, content=None, flow=False, url = None, headers = None, data = None):

        if not content:
            print("Please add a message to the content.")
            print("\n\n", end="", flush=True)
            if flow or self.flow:
                print('Cant use flow with stream off.')
                print('\n', end="", flush=True)
            return self.default_stream_response
        
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code < 300:
            if flow or self.flow:
                print("Cant use flow with stream off.")
                print('\n', end="", flush=True)
            return response.json()
        else:
            self.default_stream_response['content'] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
            print(f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}")
            return self.default_stream_response

    def view(self):
        url = f"{mutual.endpoint}/memories/{self.bot_id}"

        headers = {
            "Authorization": f"Bearer {mutual.api_key}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code < 300:
            return response.json()
        else:
            return f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"

    def feed(self, source: Union[str, List[str], Tuple[str, bytes]] = None, subject=None):
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
                    'file': file,
                    'subject': subject
                }
                # Send the POST request
                response = requests.post(url, files=data, headers=headers)

        elif isinstance(source, list):  # Source is a list of strings
            # Prepare the data payload
            data = {
                'data': source,
                'subject': subject
            }
            # Convert data to json format
            data = json.dumps(data)
            # Send the POST request
            response = requests.post(url_text, data=data, headers=headers)

        elif isinstance(source, tuple):  # Source is (filename, file content)
            filename, file_content = source
            # Prepare the data payload
            data = {
                'file': (filename, io.BytesIO(file_content)),  # Create a tuple (filename, file-like object)
                'subject': subject
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
        
    def clear_conversations(self, username=None):
        url = f"{mutual.endpoint}/bots_user/{str(self.bot_id)}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "username": username
        }
        
        response = requests.delete(url, data=json.dumps(data), headers=headers)
        if response.status_code < 300:
            return response.json()
        else:
            self.default_stream_response["content"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
            return self.default_stream_response