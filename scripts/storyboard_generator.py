# -*- coding: utf-8 -*-
"""分镜脚本生成器 - 健康早报版
基于李一帆9镜头框架，针对健康/医学内容优化
"""

def generate_storyboard(news_items, title, subtitle=""):
    """生成早报视频分镜脚本
    Args:
        news_items: list of (news_title, news_body, category)
        title: 早报标题
        subtitle: 副标题
    Returns:
        list of shot dicts
    """
    total_items = len(news_items)
    
    shots = []
    
    # ===== 封面（5个镜头）=====
    shots.append({
        "num": 1, "type": "封面", "shot_type": "远景",
        "camera": "固定镜头", "light": "逆光",
        "画面": "乐城天际线，黄昏时分，逆光勾勒建筑轮廓，天空呈蓝紫渐变，营造专业沉稳氛围",
        "台词": title,
        "note": "交代整体氛围，开场定调"
    })
    
    shots.append({
        "num": 2, "type": "封面", "shot_type": "中景",
        "camera": "缓慢推进", "light": "自然顶光",
        "画面": "精算师在办公桌前，翻阅医疗报告，数据图表在屏幕上映出，专业感十足",
        "台词": subtitle or "用精算师的视角，看懂健康行业",
        "note": "建立人物IP，强化专业人设"
    })
    
    shots.append({
        "num": 3, "type": "封面", "shot_type": "特写",
        "camera": "微拉", "light": "侧光",
        "画面": "手握钢笔，在文件上标注重点，镜头从文件拉开到人物侧脸",
        "台词": "今天的重要内容",
        "note": "特写细节，增加真实感"
    })
    
    shots.append({
        "num": 4, "type": "封面", "shot_type": "中景",
        "camera": "横移", "light": "冷色环境光",
        "画面": "书架/医疗设备/乐城元素依次入画，展示专业背景",
        "台词": "今日摘要",
        "note": "转场过渡，引入正题"
    })
    
    shots.append({
        "num": 5, "type": "封面", "shot_type": "特写",
        "camera": "推镜头", "light": "聚焦光",
        "画面": "数据图表特写，数字跳动或增长箭头，暗示今日内容分量",
        "台词": f"共{total_items}条重要资讯",
        "note": "信息量预告，制造期待"
    })
    
    # ===== 新闻内容（每条2个镜头）=====
    category_map = {
        "新药": "新药审批/研发突破",
        "技术": "治疗技术进展",
        "政策": "政策利好",
        "数据": "行业数据",
        "事件": "重要事件",
        "default": "行业资讯"
    }
    
    for i, (news_title, news_body, category) in enumerate(news_items):
        base = 5 + i * 2
        cat_desc = category_map.get(category, category_map["default"])
        
        shots.append({
            "num": base, "type": "新闻", "shot_type": "中景",
            "camera": "推向画面", "light": "冷色顶光",
            "画面": f"{cat_desc}相关画面，数据图表或医疗场景",
            "台词": news_title,
            "note": f"【{category}】强化分类感知"
        })
        
        body_short = news_body[:80] + "..." if len(news_body) > 80 else news_body
        shots.append({
            "num": base + 1, "type": "新闻", "shot_type": "特写",
            "camera": "缓慢拉远", "light": "丁达尔光/逆光",
            "画面": "核心数据或关键信息特写，配合图表或医疗元素",
            "台词": body_short,
            "note": "一句话概括核心价值"
        })
    
    # ===== 结尾（2个镜头）=====
    last = 5 + total_items * 2
    
    shots.append({
        "num": last, "type": "结尾", "shot_type": "中景",
        "camera": "固定", "light": "温暖侧光",
        "画面": "精算师起身，走向窗边，望向远方，留下思考的背影",
        "台词": "关注健康，精算未来",
        "note": "情绪落点，传递使命感"
    })
    
    shots.append({
        "num": last + 1, "type": "结尾", "shot_type": "远景",
        "camera": "拉远", "light": "逆光剪影",
        "画面": "乐城天际线全景，镜头缓缓拉远，建筑在夕阳下形成剪影",
        "台词": "刘一｜精算师聊健康",
        "note": "品牌落位，收尾"
    })
    
    return shots

def print_shots(shots):
    """打印分镜脚本"""
    print("=" * 80)
    print("【早报视频分镜脚本】")
    print("=" * 80)
    for s in shots:
        print(f"\n镜头{s['num']} | {s['type']}")
        print(f"  景别：{s['shot_type']}  | 运镜：{s['camera']}  | 光影：{s['light']}")
        print(f"  画面：{s['画面']}")
        print(f"  台词：{s['台词']}")
        print(f"  备注：{s['note']}")

def make_prompt(s):
    """生成AI绘图提示词"""
    return f"{s['shot_type']}，{s['画面']}，{s['light']}，电影感，8K，高清"

def make_voice_params(s):
    """生成配音参数（edge-tts风格）
    
    Returns:
        dict with rate, pitch, volume suggestions
    """
    t = s['type']
    cam = s['camera']
    
    if t == "封面" and cam == "推镜头":
        return {"rate": "+0%", "pitch": "0Hz", "style": "新闻播报", "speed": "中等"}
    elif t == "新闻" and s['shot_type'] == "特写":
        return {"rate": "-10%", "pitch": "0Hz", "style": "讲解", "speed": "稍慢"}
    elif t == "结尾":
        return {"rate": "+5%", "pitch": "0Hz", "style": "温暖收尾", "speed": "中等偏慢"}
    else:
        return {"rate": "0%", "pitch": "0Hz", "style": "标准", "speed": "中等"}

if __name__ == "__main__":
    # 测试
    news = [
        ("麦吉尔大学：胰岛细胞移植新突破", 
         "绕过传统移植需先建立血供的难题，同时降低免疫排异风险",
         "技术"),
        ("Sana UP421：I型糖尿病患者14个月持续产胰岛素", 
         "细胞移植后无需免疫抑制剂，路径可行性持续验证",
         "新药"),
        ("Vertex BLA申报进展", 
         "功能性治愈数据更新，90%患者胰岛素独立性",
         "数据"),
    ]
    
    title = "干细胞疗法三大新突破"
    subtitle = "用精算师的视角，看懂健康行业"
    
    shots = generate_storyboard(news, title, subtitle)
    print_shots(shots)
    
    print("\n" + "=" * 80)
    print("【AI绘图提示词 + 配音参数】")
    print("=" * 80)
    for s in shots:
        p = make_prompt(s)
        v = make_voice_params(s)
        print(f"\n镜头{s['num']} [{s['type']}]:")
        print(f"  图：{p}")
        print(f"  声：语速{v['rate']}，音调{v['pitch']}，风格={v['style']}，速度={v['speed']}")
