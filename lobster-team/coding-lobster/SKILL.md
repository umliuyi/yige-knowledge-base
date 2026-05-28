# 编程龙虾 Python开发Skill

> 适用场景：生成Python脚本、API集成、数据处理、自动化任务
> 编程龙虾(coding-lobster)专用

---

## 开发流程（5步）

### 第一步：理解任务
- 输入是什么？（文件/参数/需求）
- 输出是什么？（文件/API响应/执行结果）
- 评估难度和所需时间

### 第二步：先看同类文件
- 扫描 workspace/scripts/ 下是否有类似脚本
- 了解现有命名规范和注释风格

### 第三步：编写代码
- UTF-8编码
- 中文注释
- 异常处理完整
- 超时控制

### 第四步：自测
- 语法检查：python -m py_compile xxx.py
- 如有测试数据，执行简单测试

### 第五步：输出报告（必须包含）
1. 代码保存路径
2. 核心功能说明
3. 使用方式（命令行参数）
4. 依赖库（pip install）
5. 注意事项

---

## 标准输出模板

`
## 代码路径
[实际路径]

## 核心功能
[功能列表]

## 使用方式
[命令行示例]

## 依赖库
[pip install xxx]

## 注意事项
[踩坑记录]
`

---

## 代码模板

### 模板A：命令行工具
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description=描述)
    parser.add_argument(-i, --input, required=True, help=输入)
    parser.add_argument(-o, --output, required=True, help=输出)
    args = parser.parse_args()
    # 核心逻辑
    ...

if __name__ == __main__:
    try:
        main()
    except Exception as e:
        print(f错误: {e})
        sys.exit(1)

### 模板B：API调用
import requests
import json
import sys

BASE_URL = https://api.example.com

def call_api(endpoint, params=None):
    try:
        resp = requests.get(f{BASE_URL}{endpoint}, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f请求失败: {e})
        sys.exit(1)

# 核心逻辑
...

---

## 编码规范
- 文件头部：# -*- coding: utf-8 -*-
- 中文注释，英文变量
- 异常处理 try-except-finally
- print日志输出
- sys.exit(1)表示失败
