# 调试/Bug排查Skill

> 适用场景：代码报错、运行异常、逻辑错误
> 编程龙虾专用

---

## 排查流程（4步）

### 第一步：读错误信息
- 完整复制错误信息
- 识别错误类型（SyntaxError/TypeError/Exception等）
- 定位错误文件和行号

### 第二步：搜索类似问题
- 用Brave Search搜索错误关键词
- 搜索StackOverflow相似问题
- 记录1-3个可行解决方案

### 第三步：定位根因
- 单独运行报错行
- print断点打印变量值
- 逐步注释代码定位问题

### 第四步：修复并验证
- 修复代码
- 重新运行
- 验证修复成功

---

## 常见错误与解决方案

### SyntaxError（语法错误）
- 缺少括号、引号、分号
- 缩进不一致
- 中文字符混入代码

### ImportError / ModuleNotFoundError
- pip install 缺失模块
- 检查模块名拼写

### TypeError
- 类型不匹配（字符串+数字）
- 解决：str() / int() 转换

### requests.exceptions.RequestException
- 网络问题：加timeout参数
- 认证失败：检查Headers/Token
- 404/403：检查URL是否正确

### JSONDecodeError
- 响应不是JSON格式
- 解决：resp.text 用 .text 而非 .json()

### FileNotFoundError
- 路径错误（相对vs绝对路径）
- 解决：用绝对路径或 os.path

### UnicodeEncodeError
- Windows中文编码问题
- 解决：PYTHONIOENCODING=utf-8

---

## Python调试命令

### 语法检查
python -m py_compile script.py

### 打印调试
print(f'DEBUG: var={var}')

### 完整回溯
python -v script.py 2>&1 | tail -50

### 交互式调试
python -i script.py
# 进入交互式shell，可检查变量

---

## 编程龙虾输出规范

1. 错误类型
2. 错误位置（文件:行号）
3. 可能原因
4. 搜索到的解决方案
5. 修复代码
6. 验证结果
