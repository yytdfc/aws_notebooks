import json
import requests


payload = {
    "messages": [
        {
            "role": "user",
            "content": [{"text": "Write a short story"}]
        }
    ]
}


headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}

model_id = "global.anthropic.claude-haiku-4-5-20251001-v1:0"

stream = True

def parse_eventstream(data):
    try:
        json_start = data.find(b'{"')
        json_end = data.rfind(b'}') + 1
        json_data = data[json_start:json_end]
        return json_data
    except Exception as e:
        return None

if stream:
    url = f"https://bedrock-runtime.us-east-1.amazonaws.com/model/{model_id}/converse-stream"
    response = requests.request("POST", url, json=payload, headers=headers, stream=True)
    for line in response.iter_lines():
        if line:
            result = parse_eventstream(line)
            if result:
                try:
                    result = json.loads(result.decode("utf-8"))
                    if "delta" in result:
                        print(result["delta"]["text"], end="", flush=True)
                    elif "usage" in result:
                        print("\n\nUsage:", result["usage"], flush=True)
                except Exception as e:
                    pass
    print()

else:
    url = f"https://bedrock-runtime.us-east-1.amazonaws.com/model/{model_id}/converse"
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)

