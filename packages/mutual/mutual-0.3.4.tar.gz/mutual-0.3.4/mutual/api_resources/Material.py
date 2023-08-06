import requests
import json
import mutual

default_material_object_response = {
    "material_id": None,
    "MATERIAL_MEMORIES_PER_QUERY": 0,
    "MATERIAL_JEOPARDY_MEMORIES_PER_QUERY": 0,
    "MATERIAL_QA_MEMORIES_PER_QUERY": 0,
    "MATERIAL_AQ_MEMORIES_PER_QUERY": 0,
    "MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY": 0,
    "created_by": None,
    "details": "Successful!"
}

def get_materials(limit=20, offset=0):
    url = f"{mutual.endpoint}/materials?limit={limit}&offset={offset}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_material_object_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_material_object_response

def get_material(material_id):
    url = f"{mutual.endpoint}/materials/{str(material_id)}"
    headers = {
        "Authorization": f"Bearer {mutual.api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_material_object_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_material_object_response

def create_material(
        material_id,
        MATERIAL_MEMORIES_PER_QUERY = None,
        MATERIAL_JEOPARDY_MEMORIES_PER_QUERY = None,
        MATERIAL_QA_MEMORIES_PER_QUERY = None,
        MATERIAL_AQ_MEMORIES_PER_QUERY = None,
        MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY = None
    ):
    url = f"{mutual.endpoint}/materials"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }
    data = {
        "material_id": material_id,
        "MATERIAL_MEMORIES_PER_QUERY": MATERIAL_MEMORIES_PER_QUERY,
        "MATERIAL_JEOPARDY_MEMORIES_PER_QUERY": MATERIAL_JEOPARDY_MEMORIES_PER_QUERY,
        "MATERIAL_QA_MEMORIES_PER_QUERY": MATERIAL_QA_MEMORIES_PER_QUERY,
        "MATERIAL_AQ_MEMORIES_PER_QUERY": MATERIAL_AQ_MEMORIES_PER_QUERY,
        "MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY": MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY,
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_material_object_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {response.text}"
        return default_material_object_response

def update_material(
        material_id,
        MATERIAL_MEMORIES_PER_QUERY = None,
        MATERIAL_JEOPARDY_MEMORIES_PER_QUERY = None,
        MATERIAL_QA_MEMORIES_PER_QUERY = None,
        MATERIAL_AQ_MEMORIES_PER_QUERY = None,
        MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY = None
    ):

    url = f"{mutual.endpoint}/materials/{str(material_id)}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mutual.api_key}"
    }

    data = {
        "material_id": material_id,
        "MATERIAL_MEMORIES_PER_QUERY": MATERIAL_MEMORIES_PER_QUERY,
        "MATERIAL_JEOPARDY_MEMORIES_PER_QUERY": MATERIAL_JEOPARDY_MEMORIES_PER_QUERY,
        "MATERIAL_QA_MEMORIES_PER_QUERY": MATERIAL_QA_MEMORIES_PER_QUERY,
        "MATERIAL_AQ_MEMORIES_PER_QUERY": MATERIAL_AQ_MEMORIES_PER_QUERY,
        "MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY": MATERIAL_PARAPHRASE_MEMORIES_PER_QUERY,
    }

    # remove keys with None value
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code < 300:
        return response.json()
    else:
        default_material_object_response["details"] = f"Request failed with status code {response.status_code}, with an Error Message: {json.loads(response.text)['detail'] or response.text}"
        return default_material_object_response
