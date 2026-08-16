#!/usr/bin/env python3
# 测试前端API调用，模拟前端通过Vite代理访问后端

import requests
import json

# 测试前端代理的API调用
url = "http://localhost:3001/api/chat"
headers = {"Content-Type": "application/json"}
data = {"message": "解释一下什么是 JVM 内存模型？"}

response = requests.post(url, headers=headers, data=json.dumps(data))
print("Status code:", response.status_code)
print("Response:", response.json())

# 测试健康检查接口
health_url = "http://localhost:3001/api/health"
health_response = requests.get(health_url)
print("\nHealth check status code:", health_response.status_code)
print("Health check response:", health_response.json())