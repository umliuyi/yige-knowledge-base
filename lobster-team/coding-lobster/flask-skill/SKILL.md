# Flask Web开发Skill

> 适用场景：快速构建内部工具、数据展示页面、API服务、爬虫管理后台
> 编程龙虾专用

---

## Flask核心结构（最小模板）

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/api/data')
def api_data():
    return jsonify({'data': 'value'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

---

## 常用路由模式

### GET请求
@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = {'id': user_id, 'name': '张三'}
    return jsonify(user)

### POST请求
@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json()
    return jsonify({'received': data, 'status': 'ok'})

### URL参数
@app.route('/search')
def search():
    q = request.args.get('q', '')
    return jsonify({'query': q, 'results': []})

### 页面模板
@app.route('/page')
def page():
    return render_template('page.html', title='标题', data=data)

---

## 模板文件（templates/）

templates/index.html:
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ data }}</p>
</body>
</html>

---

## 静态文件（static/）

static/
  style.css
  app.js

app = Flask(__name__, static_folder='static', template_folder='templates')

---

## 数据存储

### SQLite（最简单）
import sqlite3

def get_db():
    return sqlite3.connect('app.db')

@app.route('/users')
def users():
    db = get_db()
    cur = db.execute('SELECT * FROM users')
    return jsonify([dict(row) for row in cur.fetchall()])

---

## API返回格式

def api_response(data, code=200):
    return jsonify({'code': code, 'data': data})

def api_error(msg, code=400):
    return jsonify({'code': code, 'error': msg}), code

---

## 运行与部署

# 开发环境
app.run(debug=True, port=5000)

# 生产环境（Gunicorn）
# gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 依赖
# pip install flask gunicorn

---

## 编程龙虾输出规范

1. 用途说明
2. 文件结构（app.py + templates/）
3. 访问地址（http://localhost:5000）
4. 依赖库（pip install）
5. 运行命令

---

## 注意事项
- debug=True只在开发环境用
- 生产环境用gunicorn
- 敏感配置用环境变量
- CORS问题用flask-cors库
