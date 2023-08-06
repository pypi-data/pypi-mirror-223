# mutual

A python package to interact with the Mutuai API.

## Installation

Run `pip install mutual` in the project root directory.

### Usage

```python
import mutual
import json

# to get the api_key
print(mutual.api_key)
# to set the api_key
mutual.api_key = "your_api_key"

# CHAT
mutual.api_key = "your_api_key"
for message in mutual.Chat.create("Hello", "seansbot", "Sean"):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)
# OR
for message in mutual.Chat.create("Hello", bot_name="seansbot", username="Sean", prompt="You are a customer assistant for mutual that provides helpful information"):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)

```
## Chat.create(parameters)
```python
# bot_name --> uniquely identifies the bot tied to the api_key account holder
# bot_id --> uniquely identifies the bot accross all bots
# username --> uniquely identifies person interacting with bot

## OPTIONALS
# prompt (str)--> used to add prompts to bot
# prompt_id (str)--> used to add prompts that are available on the database, prompt overrides this
# judge_id (str)--> used to identify judge prompts. leave for default
# judge_message_id (str)--> used to identiy judge messages. leave for default
# material_id (str) ---> used to change material settings
# error_logs (bool) --> False by default, hides error messages
# multiplayer_memory (bool) --> True by default, allows mulitplayer 
# context_window (int) --> determines context, default 2
```

```python
# CHAT DEMO
for message in mutual.Chat.create_demo("Hello"):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)

# BOT Instance

# uses bot name
alexbot = mutual.create_bot("bot_name") # THIS WILL CREATE A NEW BOT AND IF BOT WITH BOT NAME EXIST WILL RETURN THAT BOT
for message in alexbot.chat("Hey there", "username"):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)

# can create bot instance passing in these values
alexbot = mutual.create_bot(bot_name="alexbot", prompt="You are a customer assistant for mutual that provides helpful information") 

# bot id
alexbot = mutual.fetch_bot("bot_id or bot_name") # THIS WILL LOOK UP FOR A EXISTING BOT AND GENERATE AN INSTANCE OF THAT BOT
for message in alexbot.chat("Hey there", "Sean"):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)

# update using bot instance
alexbot.update_bot(bot_name='new_bot_name', prompt='You are a window cleaner')

# feed bot data
response = alexbot.feed(source="file_path")
print(response)
# view fed bot data
response = alexbot.view()
print(response)

# view bot instance data
print(alexbot.api_key) # prints the api_key
print(alexbot.bot_id) # prints the bot id
print(alexbot.bot_name) # prints the bot name
print(alexbot.prompt_id) # prints the prompt id
print(alexbot.judge_id) # prints the judge_id
print(alexbot.judge_message_id) # prints the judge_message_id

# BOT
# using functions
print(mutual.Bot.get_bots())
print(mutual.Bot.get_bots(limit=100, offset=20))
print(mutual.Bot.get_bot("bot_id or bot_name"))
print(mutual.Bot.create_bot("bot_name", "prompt"))
print(mutual.Bot.create_bot("bot_name", "prompt"))
print(mutual.Bot.update_bot(bot_id="bot_id", bot_name="bot_name", prompt_id="prompt_id", judge_id="judge_id", judge_message_id="judge_message_id"))

# you can also set the bot_id like this so you dont need to pass it in chat
mutual.bot_id = "bot_id"

# to print the bot_id
print(mutual.bot_id)

# PROMPT

# to see sample prompt
print(mutual.sample_prompt)

print(mutual.Prompt.get_prompts())
print(mutual.Prompt.get_prompt("prompt_id"))
print(mutual.Prompt.create_prompt("prompt_id", "prompt"))
# OR
print(mutual.Prompt.create_prompt(prompt_id="prompt_id", prompt="prompt"))
print(mutual.Prompt.update_prompt("prompt_id", prompt="You are an assistant named Hercules."))

# JUDGE

# too see sample judge
print(mutual.sample_judge)

print(mutual.Judge.get_judges())
print(mutual.Judge.get_judge("judge_id"))
print(mutual.Judge.create_judge("judge_id",
    world_prompt="judges world",
    action_prompt="the judges action",
    judge_convo_aware="judges awareness with the conversation",
    judge="default judge",
    judgement_lens="how the judge will judge"
))
print(mutual.Judge.update_judge("judge_id",
    world_prompt=None,
    action_prompt=None,
    judge_convo_aware=None,
    judge=None,
    judgement_lens=None
))

# JUDGEMESSAGE

# to see sample judge message
print(mutual.sample_judge_messages)

print(mutual.JudgeMessage.get_judge_messages())
print(mutual.JudgeMessage.get_judge_message("judge_message_id"))
print(mutual.JudgeMessage.create_judge_message("judge_message_id",
    default_message="how judge will respond",
    unnatural_lang_message="how judge will respond to a langunage not undestood",
    manipulation_message="how judge will respond to being manipulated"))
print(mutual.JudgeMessage.update_judge_message("judge_message_id",
    default_message=None,
    unnatural_lang_message=None,
    manipulation_message=None))

# Material
print(mutual.Material.get_materials())
print(mutual.Material.get_material("material_id"))
print(mutual.Material.create_material("material_id",
    MATERIAL_MEMORIES_PER_QUERY = 0,
    MATERIAL_JEOPARDY_MEMORIES_PER_QUERY = 0,
    MATERIAL_QA_MEMORIES_PER_QUERY = 0,
    MATERIAL_AQ_MEMORIES_PER_QUERY = 0,
    MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY = 0))
print(mutual.Material.update_material("material_id",
    MATERIAL_MEMORIES_PER_QUERY = None,
    MATERIAL_JEOPARDY_MEMORIES_PER_QUERY = None,
    MATERIAL_QA_MEMORIES_PER_QUERY = None,
    MATERIAL_AQ_MEMORIES_PER_QUERY = None,
    MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY = None))

# Memory
print(mutual.Memory.feed("bot_id or bot_name", source="file_path"))
print(mutual.Memory.get_memory_file_data("grid_fs_id")) --> can be found in files, and returns the data that was contained in the file
print(mutual.Memory.get_memory_files()) --> returns a list of files which contain the grid_fs_id
print(mutual.Memory.view("bot_id or bot_name"))
# DEV
response = mutual.Dev.clear("bot_id") # clears memories

# APIKey naming
response = mutual.APIKey.update_api_key("new_api_key_name")
print(response.get("prev_api_key_name", None))
print(response.get("new_api_key_name", None))
print(response.get("api_key", None))

# you can import the functions directly like so
from mutual import Bot, Chat, Dev, Prompt, Judge, JudgeMessage, APIKey, Memory, Material
```

# SAMPLE TO PRINT ERRORS
```py
index = 0
for message in mutual.Chat.create_demo("Hello"):
    json_data = json.loads(message)
    if index == 0:
        print(json_data['data']['bot_data']['bot_id'], end='', flush=True)
        print(json_data['data']['user_data']['username'], end='', flush=True)
        print(json_data['data']['bot_data']['bot_name'], end='', flush=True)
    index += 1
    print(json_data['content'], end='', flush=True)
```

# SAMPLE TO PRINT DATA
```py
for message in mutual.Chat.create_demo("Hello"):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)

alexbot = mutual.create_bot("AlexBot")
for message in alexbot.chat("hello", username="Alex"):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)
```

# FLOW EXAMPLE
```py
alexbot = mutual.create_bot("AlexbBot2",prompt="You are a customer assistant for mutual that provides helpful information")
for message in alexbot.chat("hello", username="Alex", flow=True):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)
```

# FEED MEMORY EXAMPLE
```py
alexbot = mutual.fetch_bot("mutual-bot-1")

feed_response = alexbot.feed(source=f"/Users/alexbetita/Documents/Programming/api-agent-package/api-agent/package/agent_info_2_copy.txt")

or

feed_response = alexbot.feed(source=["Alex Betita is a full stack software engineer for Mutual.", "He is also full stack teacher for App Academy"])

print(feed_response)

response = alexbot.view()
for memory in response['memories']:
    print(memory)
```

# STREAM OFF EXAMPLE
```py

response = alexbot.chat("Hi!", username="Alex", stream=False)
json_data = json.loads(response)
print(json_data['content'])


for message in alexbot.chat("hello", username="Alex", flow=True, stream=False):
    json_data = json.loads(message)
    print(json_data['content'], end='', flush=True)

```