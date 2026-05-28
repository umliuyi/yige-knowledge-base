# API开发Skill

> 适用场景：调用外部API、数据接口集成、第三方服务对接
> 编程龙虾专用

---

## 开发流程（5步）

### 第一步：理解API
- 明确API的用途
- 确认Base URL、认证方式（Token/Key/Bearer）
- 确认请求方法（GET/POST/PUT/DELETE）
- 确认请求和响应的数据格式（JSON/XML）

### 第二步：查阅文档
- 通过Brave Search搜索官方API文档
- 通过Web Fetch抓取API文档页面
- 了解速率限制、错误码

### 第三步：编写代码
- 使用requests库
- 添加超时（timeout=30）
- 添加异常处理
- 添加日志输出

### 第四步：测试
- 用测试数据运行API调用
- 验证返回数据格式
- 检查错误处理

### 第五步：输出报告

---

## 标准输出模板

## API名称
[API名称]

## 端点
[Base URL]

## 认证方式
[Token/Key/Bearer等]

## 核心功能
[功能列表]

## 使用方式
[python调用示例]

## 依赖库
[需要安装的pip包]

## 注意事项
[速率限制、错误处理等]

---

## 代码模板

import requests
import json
import sys

BASE_URL = 'https://api.example.com'
HEADERS = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
}

def call_api(endpoint, method='GET', params=None, data=None):
    url = f'{BASE_URL}{endpoint}'
    try:
        if method == 'GET':
            resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        elif method == 'POST':
            resp = requests.post(url, headers=HEADERS, json=data, timeout=30)
        elif method == 'PUT':
            resp = requests.put(url, headers=HEADERS, json=data, timeout=30)
        elif method == 'DELETE':
            resp = requests.delete(url, headers=HEADERS, timeout=30)
        else:
            print(f'不支持的请求方法: {method}')
            sys.exit(1)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f'请求失败: {e}')
        sys.exit(1)

# 示例调用
if __name__ == '__main__':
    result = call_api('/endpoint', 'GET', params={'key': 'value'})
    print(json.dumps(result, ensure_ascii=False, indent=2))

---

## 常用API调用模式

### 模式1：GET查询
result = call_api('/users/123', 'GET')

### 模式2：POST创建
result = call_api('/users', 'POST', data={'name': 'test'})

### 模式3：带分页
page = 1
while True:
    result = call_api('/users', 'GET', params={'page': page, 'limit': 100})
    if not result.get('data'):
        break
    for item in result['data']:
        print(item)
    page += 1

---

## 错误处理规范
- 网络错误：捕获requests.RequestException
- HTTP错误：resp.raise_for_status()
- 业务错误：检查返回的code/status字段
- 超时：设置timeout=30秒

## 日志输出
print(f'[API] 调用 {method} {url}')
print(f'[API] 响应: {status_code}')
