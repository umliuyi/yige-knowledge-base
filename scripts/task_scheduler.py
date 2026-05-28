"""
定时任务调度器
- 读取 YAML/JSON 配置文件
- 按设定时间自动执行任务（HTTP请求、Shell命令、Python函数）
- 记录执行日志
- 任务失败告警（打印错误信息）
"""

import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union

import schedule
import yaml

# ─────────────────────────────────────────────
# 配置区
# ─────────────────────────────────────────────
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "tasks_config.yaml")
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, f"scheduler_{datetime.now().strftime('%Y%m%d')}.log")

# 全局任务注册表（用于 python 类型任务）
TASK_REGISTRY: Dict[str, Callable] = {}


# ─────────────────────────────────────────────
# 日志配置
# ─────────────────────────────────────────────
def setup_logging(level: int = logging.INFO) -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


# ─────────────────────────────────────────────
# 注册任务装饰器（用于 python 类型任务）
# ─────────────────────────────────────────────
def register_task(name: str):
    """装饰器：将函数注册到全局任务表"""
    def decorator(func: Callable) -> Callable:
        TASK_REGISTRY[name] = func
        return func
    return decorator


# ─────────────────────────────────────────────
# 任务执行器
# ─────────────────────────────────────────────
class TaskExecutor:
    def __init__(self, task_config: Dict[str, Any], alert_enabled: bool = True):
        self.task_config = task_config
        self.alert_enabled = alert_enabled
        self.task_name = task_config.get("name", "unnamed")
        self.task_type = task_config.get("type", "shell")
        self.retries = task_config.get("retries", 0)
        self.retry_delay = task_config.get("retry_delay", 5)

    def _log(self, level: str, msg: str) -> None:
        getattr(logging, level)(f"[{self.task_name}] {msg}")

    def _alert(self, msg: str) -> None:
        if self.alert_enabled:
            print(f"\n{'='*60}")
            print(f"  🚨 任务失败告警: {self.task_name}")
            print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  错误: {msg}")
            print(f"{'='*60}\n")

    def _http_task(self) -> Any:
        import urllib.request
        import urllib.error

        url = self.task_config["url"]
        method = self.task_config.get("method", "GET").upper()
        headers = self.task_config.get("headers", {})
        body = self.task_config.get("body")
        timeout = self.task_config.get("timeout", 30)

        self._log("INFO", f"发起 {method} 请求: {url}")
        req = urllib.request.Request(url, method=method, headers=headers)
        if body:
            if isinstance(body, dict):
                body = json.dumps(body).encode("utf-8")
                req.add_header("Content-Type", "application/json")
            elif isinstance(body, str):
                body = body.encode("utf-8")
            req.data = body

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                body_resp = resp.read().decode("utf-8", errors="replace")
                self._log("INFO", f"响应状态: {status}")
                return {"status": status, "body": body_resp}
        except urllib.error.HTTPError as e:
            err_msg = f"HTTP错误 {e.code}: {e.reason}"
            self._alert(err_msg)
            raise
        except urllib.error.URLError as e:
            err_msg = f"URL错误: {e.reason}"
            self._alert(err_msg)
            raise
        except Exception as e:
            self._alert(f"HTTP请求异常: {e}")
            raise

    def _shell_task(self) -> Any:
        cmd = self.task_config["command"]
        cwd = self.task_config.get("cwd")
        env_extra = self.task_config.get("env", {})

        self._log("INFO", f"执行Shell命令: {cmd}")
        env = os.environ.copy()
        env.update(env_extra)

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                env=env,
                capture_output=True,
                text=True,
                timeout=self.task_config.get("timeout", 300),
            )
            if result.returncode == 0:
                self._log("INFO", f"命令执行成功 (退出码: 0)")
                return {"returncode": 0, "stdout": result.stdout, "stderr": result.stderr}
            else:
                err_msg = f"命令执行失败 (退出码: {result.returncode})\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
                self._alert(err_msg)
                return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.TimeoutExpired:
            err_msg = f"命令执行超时 (超时: {self.task_config.get('timeout', 300)}s)"
            self._alert(err_msg)
            raise
        except Exception as e:
            self._alert(f"Shell执行异常: {e}")
            raise

    def _python_task(self) -> Any:
        func_name = self.task_config["function"]
        args = self.task_config.get("args", [])
        kwargs = self.task_config.get("kwargs", {})

        self._log("INFO", f"调用Python函数: {func_name}")
        if func_name not in TASK_REGISTRY:
            err_msg = f"函数 '{func_name}' 未注册，请使用 @register_task('{func_name}') 装饰"
            self._alert(err_msg)
            raise NameError(err_msg)

        func = TASK_REGISTRY[func_name]
        try:
            result = func(*args, **kwargs)
            self._log("INFO", f"函数执行成功")
            return result
        except Exception as e:
            self._alert(f"Python函数执行异常: {e}")
            raise

    def _subprocess_script_task(self) -> Any:
        """通过 subprocess 调用其他 Python 脚本"""
        script_path = self.task_config["script"]
        args = self.task_config.get("script_args", [])
        cwd = self.task_config.get("cwd")

        self._log("INFO", f"调用子脚本: {script_path}")
        cmd = [sys.executable, script_path] + args
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=self.task_config.get("timeout", 300),
            )
            if result.returncode == 0:
                self._log("INFO", f"子脚本执行成功 (退出码: 0)")
                return {"returncode": 0, "stdout": result.stdout, "stderr": result.stderr}
            else:
                err_msg = f"子脚本执行失败 (退出码: {result.returncode})\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
                self._alert(err_msg)
                return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.TimeoutExpired:
            err_msg = f"子脚本执行超时 (超时: {self.task_config.get('timeout', 300)}s)"
            self._alert(err_msg)
            raise
        except Exception as e:
            self._alert(f"子脚本执行异常: {e}")
            raise

    def execute(self) -> Optional[Any]:
        """执行任务，支持重试"""
        task_type_map = {
            "http": self._http_task,
            "shell": self._shell_task,
            "python": self._python_task,
            "subprocess": self._subprocess_script_task,
        }

        action = task_type_map.get(self.task_type)
        if not action:
            err_msg = f"未知任务类型: {self.task_type}"
            self._alert(err_msg)
            raise ValueError(err_msg)

        last_error = None
        for attempt in range(self.retries + 1):
            try:
                return action()
            except Exception as e:
                last_error = e
                if attempt < self.retries:
                    self._log("WARNING", f"第 {attempt+1} 次失败，{self.retry_delay}s 后重试...")
                    time.sleep(self.retry_delay)
                else:
                    self._log("ERROR", f"任务最终失败: {e}")

        self._alert(f"重试 {self.retries} 次后仍失败: {last_error}")
        return None


# ─────────────────────────────────────────────
# 调度器
# ─────────────────────────────────────────────
class TaskScheduler:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.tasks: List[Dict] = []
        self.alert_enabled = True
        self._load_config()

    def _load_config(self) -> None:
        ext = os.path.splitext(self.config_path)[1].lower()
        with open(self.config_path, "r", encoding="utf-8") as f:
            if ext in (".yaml", ".yml"):
                raw = yaml.safe_load(f)
            elif ext == ".json":
                raw = json.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {ext}")

        self.tasks = raw.get("tasks", [])
        self.alert_enabled = raw.get("settings", {}).get("alert_enabled", True)
        logging.info(f"已加载 {len(self.tasks)} 个任务配置")

    def _schedule_task(self, task: Dict) -> None:
        name = task.get("name", "unnamed")
        schedule_rule = task.get("schedule", "")
        enabled = task.get("enabled", True)

        if not enabled:
            logging.info(f"任务 [{name}] 已禁用，跳过")
            return

        if not schedule_rule:
            logging.warning(f"任务 [{name}] 未配置 schedule，跳过")
            return

        job = TaskExecutor(task, alert_enabled=self.alert_enabled)

        # 解析调度规则
        # 格式: "every(10).seconds" / "every(5).minutes" / "every().hour.at('30:00')"
        #       "every().monday.at('09:00')" 等
        try:
            if re.match(r"every\(\d*\)\.\w+", schedule_rule) or re.match(r"every\(\)\.\w+", schedule_rule):
                # 动态构建 schedule 表达式
                # 简化处理：直接把规则字符串当作代码执行
                schedule_expr = f"schedule.{schedule_rule}.do(job.execute)"
                eval(compile(schedule_expr, "<string>", "eval"))
                logging.info(f"任务 [{name}] 已注册调度规则: {schedule_rule}")
            else:
                logging.warning(f"任务 [{name}] 的 schedule 格式无法解析: {schedule_rule}")
        except Exception as e:
            logging.error(f"任务 [{name}] 注册调度规则失败: {e}")

    def _register_user_tasks(self) -> None:
        """收集并注册用户自定义的 python 类型任务"""
        # 用户可以在 tasks_config.yaml 的同目录下创建 user_tasks.py
        # 脚本会自动导入所有以 task_ 开头的函数
        user_tasks_path = os.path.join(os.path.dirname(self.config_path), "user_tasks.py")
        if os.path.exists(user_tasks_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location("user_tasks", user_tasks_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # 自动注册所有 task_ 开头的函数
                for attr_name in dir(module):
                    if attr_name.startswith("task_"):
                        TASK_REGISTRY[attr_name] = getattr(module, attr_name)
                logging.info(f"已加载自定义任务模块: {user_tasks_path}")

    def start(self) -> None:
        setup_logging()
        logging.info("=" * 50)
        logging.info("  定时任务调度器启动")
        logging.info(f"  配置文件: {self.config_path}")
        logging.info("=" * 50)

        self._register_user_tasks()

        for task in self.tasks:
            self._schedule_task(task)

        logging.info("\n调度器运行中，按 Ctrl+C 停止...\n")
        while True:
            schedule.run_pending()
            time.sleep(1)


# ─────────────────────────────────────────────
# 示例：用户自定义任务（可放在 user_tasks.py）
# ─────────────────────────────────────────────
@register_task("hello_world")
def task_hello_world():
    print("Hello from registered task!")


@register_task("send_daily_report")
def task_send_daily_report():
    import urllib.request
    url = "https://example.com/api/report"
    req = urllib.request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=10) as resp:
        print(f"Report sent, status: {resp.status}")


# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────
if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG_PATH

    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        print("\n示例配置: workspace/scripts/tasks_config.yaml")
        sys.exit(1)

    scheduler = TaskScheduler(config_path)
    scheduler.start()
