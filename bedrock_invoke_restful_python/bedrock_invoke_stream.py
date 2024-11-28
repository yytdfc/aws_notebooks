import base64
import json

import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials


# 获取凭证
credentials = Credentials(
    access_key='YOUR_ACCESS_KEY',
    secret_key='YOUR_SECRET_KEY'
)
service_name = "bedrock"  # 使用 Bedrock 服务
region_name = "us-west-2"
model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

# API 端点 URL
url = f"https://bedrock-runtime.{region_name}.amazonaws.com/model/{model_id}/invoke-with-response-stream"

# 请求体
payload = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 2048,
    "messages": [{"role": "user", "content": "hello, write a sort code in python"}],
    "system": "you are a helpful assistant",
}

# 创建 AWS 请求对象
aws_request = AWSRequest(method="POST", url=url, data=json.dumps(payload))

# 使用 SigV4Auth 对请求进行签名
SigV4Auth(credentials, service_name, region_name).add_auth(aws_request)


def parse_eventstream(data):
    try:
        json_start = data.find(b'{"')
        json_end = data.rfind(b'"}') + 2
        json_data = data[json_start:json_end]
        message_dict = json.loads(json_data)
        base64_content = message_dict["bytes"]
        decoded_content = base64.b64decode(base64_content)
        result = json.loads(decoded_content)["delta"]["text"]
        return result
    except Exception:
        return None


response = requests.post(
    url=url, 
    headers=dict(aws_request.headers), 
    data=aws_request.body,
    stream=True,
)

for line in response.iter_lines():
    if line:
        result = parse_eventstream(line)
        if result:
            print(result, end="", flush=True)
print()
