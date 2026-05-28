# 测试：生成今日早报分镜脚本
from 分镜脚本生成器 import generate_storyboard, print_storyboard, generate_prompt

# 今日新闻（示例）
news = [
    ("麦吉尔大学：胰岛细胞移植新突破", 
     "绕过传统移植需先建立血供的难题，同时降低免疫排异风险",
     "技术"),
    ("Sana UP421：I型糖尿病患者14个月持续产胰岛素", 
     "细胞移植后无需免疫抑制剂，路径可行性持续验证",
     "新药"),
    ("Vertex BLA申报进展：功能性治愈数据更新", 
     "VX-880项目临床数据显示90%患者胰岛素独立性",
     "数据"),
]

title = "干细胞疗法三大新突破"
subtitle = "用精算师的视角，看懂健康行业"

shots = generate_storyboard(news, title, subtitle)
print_storyboard(shots)

print("\n" + "=" * 80)
print("【AI绘图提示词】")
print("=" * 80)
for shot in shots:
    prompt = generate_prompt(shot)
    print(f"\n镜头{shot['序号']} [{shot['类型']}] [{shot['景别']}]：")
    print(f"  {prompt}")
