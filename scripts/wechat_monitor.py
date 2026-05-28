"""
微信公众号自动化监控脚本
功能：给定公众号名称，自动获取最新文章列表，并抓取文章内容

测试结论（基于实际测试）:
1. 微信公众号文章（mp.weixin.qq.com）可直接用requests抓取 ✓
2. 搜狗微信搜索结果通过JS动态加载，直接requests无法获取文章URL ✗
3. RSSHub公共服务(rsshub.app)超时不可用，需要自建
4. 公众号biz参数需要通过其他方式获取

推荐方案：
- 方案A（推荐）：如果有公众号的biz参数，直接调用历史文章接口
- 方案B：使用RSSHub自建服务，将公众号转为RSS订阅
- 方案C：使用浏览器自动化（如Selenium/Playwright）获取搜狗搜索结果
"""

import requests
import re
import json
import time
import hashlib
import os
from datetime import datetime
from urllib.parse import quote, urljoin
from typing import List, Dict, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeChatMonitor:
    """微信公众号监控器"""
    
    def __init__(self, cache_dir: str = None):
        """
        初始化监控器
        
        Args:
            cache_dir: 缓存目录，用于存储已爬取的文章URL
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.cache_dir = cache_dir or './cache'
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_file(self, biz: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.cache_dir, f'{biz}_articles.json')
    
    def _load_cache(self, biz: str) -> Dict[str, str]:
        """加载已爬取的文章缓存"""
        cache_file = self._get_cache_file(biz)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载缓存失败: {e}")
        return {}
    
    def _save_cache(self, biz: str, articles: Dict[str, str]):
        """保存文章缓存"""
        cache_file = self._get_cache_file(biz)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存缓存失败: {e}")
    
    def fetch_article_content(self, url: str) -> Optional[Dict]:
        """
        获取文章内容
        
        Args:
            url: 文章URL
            
        Returns:
            包含标题、正文、发布时间等信息的字典，失败返回None
        """
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"获取文章失败 [{response.status_code}]: {url}")
                return None
            
            html = response.text
            
            # 检查是否需要授权
            if any(x in html for x in ['环境异常', '验证环境', '请求已被拦截']):
                logger.warning(f"文章需要授权: {url}")
                return None
            
            # 提取标题
            title_match = re.search(r'<title>([^<]+)</title>', html)
            title = title_match.group(1).strip() if title_match else ''
            
            # 提取发布日期
            date_match = re.search(r'var\s+publish_time\s*=\s*["\']([^"\']+)["\']', html)
            publish_time = date_match.group(1) if date_match else ''
            
            # 提取作者
            author_match = re.search(r'var\s+author\s*=\s*["\']([^"\']+)["\']', html)
            author = author_match.group(1) if author_match else ''
            
            # 提取正文内容（简化版）
            content_match = re.search(
                r'<div[^>]+id\s*=\s*["\']js_content["\'][^>]*>(.*?)</div>\s*<div[^>]+id\s*=\s*["\']js_content["\']',
                html, re.DOTALL
            )
            content = ''
            if content_match:
                # 去除HTML标签，保留纯文本
                content = re.sub(r'<[^>]+>', '', content_match.group(1))
                content = re.sub(r'\s+', ' ', content).strip()
            
            return {
                'url': url,
                'title': title,
                'author': author,
                'publish_time': publish_time,
                'content': content[:500],  # 截取前500字符
                'fetch_time': datetime.now().isoformat(),
            }
            
        except Exception as e:
            logger.error(f"抓取文章异常: {e} - {url}")
            return None
    
    def fetch_articles_by_biz(self, biz: str, count: int = 10) -> List[Dict]:
        """
        通过biz获取公众号历史文章列表
        
        Args:
            biz: 公众号biz参数（如'MjM5MTU5MTQyMA=='）
            count: 获取文章数量
            
        Returns:
            文章列表
        """
        articles = []
        
        # 微信历史文章接口
        api_url = f'https://mp.weixin.qq.com/mp/profile_ext'
        params = {
            'action': 'home',
            '__biz': biz,
            'devicetype': 'Windows 10',
            'version': '62070116',
            'f': 'json',
            'ajax': '1',
        }
        
        # 添加头部
        headers = {**self.headers, 'Referer': f'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz}'}
        
        try:
            response = self.session.get(api_url, params=params, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"获取文章列表失败 [{response.status_code}]: {biz}")
                return articles
            
            data = response.json()
            
            # 检查返回数据
            if data.get('ret') == 0 and 'appmsg_list' in data:
                for item in data['appmsg_list'][:count]:
                    articles.append({
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'digest': item.get('digest', ''),
                        'create_time': item.get('datetime', ''),
                    })
                logger.info(f"通过biz获取到 {len(articles)} 篇文章: {biz}")
            else:
                logger.warning(f"biz接口返回异常: {data}")
                
        except Exception as e:
            logger.error(f"获取文章列表异常: {e}")
        
        return articles
    
    def get_article_urls_from_cache(self, biz: str) -> List[str]:
        """
        从缓存获取所有已爬取的文章URL
        
        Args:
            biz: 公众号biz
            
        Returns:
            文章URL列表
        """
        cache = self._load_cache(biz)
        return list(cache.keys())
    
    def check_new_articles(self, biz: str) -> List[Dict]:
        """
        检查新文章（与缓存对比）
        
        Args:
            biz: 公众号biz
            
        Returns:
            新文章列表
        """
        old_cache = self._load_cache(biz)
        old_urls = set(old_cache.keys())
        
        # 获取最新文章
        new_articles = self.fetch_articles_by_biz(biz, count=10)
        
        # 找出新增文章
        result = []
        for article in new_articles:
            url = article['url']
            if url not in old_cache:
                result.append(article)
                old_cache[url] = json.dumps(article, ensure_ascii=False)
        
        # 更新缓存
        if result:
            self._save_cache(biz, old_cache)
            logger.info(f"发现 {len(result)} 篇新文章")
        
        return result
    
    def get_biz_by_search(self, keyword: str) -> List[Dict]:
        """
        通过搜索获取公众号的biz（需要浏览器自动化）
        
        这个方法需要使用Selenium或Playwright来执行JavaScript，
        因为搜狗微信搜索的结果是动态加载的。
        
        Args:
            keyword: 公众号名称关键词
            
        Returns:
            公众号列表，包含biz、名称等信息
        """
        # 注意：这个方法需要浏览器自动化支持
        # 推荐使用 Playwright 或 Selenium
        # 下面的代码是伪代码，需要根据实际情况实现
        
        logger.info(f"开始搜索公众号: {keyword}")
        
        # 方法1: 使用Playwright
        # from playwright.sync_api import sync_playwright
        # 
        # with sync_playwright() as p:
        #     browser = p.chromium.launch()
        #     page = browser.new_page()
        #     page.goto(f'https://weixin.sogou.com/weixin?type=1&query={quote(keyword)}')
        #     page.wait_for_selector('.tit')
        #     # 提取biz...
        
        # 方法2: 使用RSSHub
        # 如果能自建RSSHub，可以使用：
        # rsshub_url = f'http://your-rsshub-instance/weixin/mp/{biz}'
        
        return []
    
    @staticmethod
    def md5(text: str) -> str:
        """计算MD5"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()


class WeChatArticleParser:
    """微信公众号文章解析器"""
    
    @staticmethod
    def extract_text_content(html: str) -> str:
        """
        从文章HTML中提取纯文本内容
        
        Args:
            html: 文章HTML
            
        Returns:
            纯文本内容
        """
        # 移除script和style标签
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        
        # 移除HTML注释
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # 替换换行标签
        html = re.sub(r'<br\s*/?>', '\n', html)
        html = re.sub(r'</p>', '\n', html)
        html = re.sub(r'</div>', '\n', html)
        
        # 移除所有HTML标签
        text = re.sub(r'<[^>]+>', '', html)
        
        # 清理空白字符
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        return text.strip()


# ============================================================
# 便捷函数
# ============================================================

def monitor_biz(biz: str, cache_dir: str = None) -> List[Dict]:
    """
    监控指定公众号的新文章
    
    Args:
        biz: 公众号biz参数
        cache_dir: 缓存目录
        
    Returns:
        新文章列表
    """
    monitor = WeChatMonitor(cache_dir)
    return monitor.check_new_articles(biz)


def fetch_article(url: str) -> Optional[Dict]:
    """
    获取单篇文章内容
    
    Args:
        url: 文章URL
        
    Returns:
        文章内容字典
    """
    monitor = WeChatMonitor()
    return monitor.fetch_article_content(url)


# ============================================================
# 常用公众号biz配置
# ============================================================

# 常见海南/乐城相关公众号biz（需要手动查找）
KNOWN_BIZS = {
    # 格式: '公众号名称': 'biz参数',
    # '乐城先行区': 'MjM5OTAwMTY2MA==',  # 示例，需要替换为真实的
}


# ============================================================
# 主程序示例
# ============================================================

if __name__ == '__main__':
    print("="*60)
    print("微信公众号监控工具")
    print("="*60)
    
    # 示例1: 通过biz获取文章
    print("\n示例1: 通过biz获取文章列表")
    biz = 'MjM5OTAwMTY2MA=='  # 需要替换为真实biz
    monitor = WeChatMonitor()
    articles = monitor.fetch_articles_by_biz(biz, count=5)
    for i, a in enumerate(articles):
        print(f"  {i+1}. {a['title']}")
        print(f"     {a['url']}")
    
    # 示例2: 获取单篇文章内容
    print("\n示例2: 获取单篇文章内容")
    test_url = "https://mp.weixin.qq.com/s/n0BJPD-bsH9IYgNCI-rJ-A"
    article = fetch_article(test_url)
    if article:
        print(f"标题: {article['title']}")
        print(f"内容预览: {article['content'][:200]}...")
    
    # 示例3: 检查新文章
    print("\n示例3: 检查新文章（需要先有缓存）")
    new_articles = monitor.check_new_articles(biz)
    if new_articles:
        print(f"发现 {len(new_articles)} 篇新文章:")
        for a in new_articles:
            print(f"  - {a['title']}")
    else:
        print("没有发现新文章")
    
    print("\n" + "="*60)
    print("使用说明:")
    print("1. 获取公众号biz:")
    print("   - 方法A: 打开公众号历史消息页面，从URL中提取__biz参数")
    print("   - 方法B: 通过搜狗搜索，使用Playwright等工具自动化提取")
    print("   - 方法C: 访问 https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=xxx")
    print("2. 使用monitor_biz(biz)监控指定公众号")
    print("3. 使用fetch_article(url)获取单篇文章内容")
    print("="*60)
