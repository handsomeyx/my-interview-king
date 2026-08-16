#!/usr/bin/env python3
# 测试后端API接口

import requests
import json

# 测试聊天接口
url = "http://localhost:5000/chat"
headers = {"Content-Type": "application/json"}
data = {"message": "解释一下什么是 TCP/IP 协议？"}

response = requests.post(url, headers=headers, data=json.dumps(data))
print("Status code:", response.status_code)
print("Response:", response.json())

# 测试健康检查接口
health_url = "http://localhost:5000/health"
health_response = requests.get(health_url)
print("\nHealth check status code:", health_response.status_code)
print("Health check response:", health_response.json())