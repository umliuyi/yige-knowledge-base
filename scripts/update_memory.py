# -*- coding: utf-8 -*-
"""Update MEMORY.md with today's key changes"""
import os

today = '2026-05-22'

new_section = """
## 四大专题知识库（2026-05-22建立）

| 专题 | 文件 | 核心内容 |
|------|------|---------|
| 一 | 知识库/专题一-干细胞治疗糖尿病.md | 疾病基础+治疗原理+PubMed临床数据+患者选择+Q&A+精算话术 |
| 二 | 知识库/专题二-DC-NK细胞免疫治疗肿瘤.md | DC/NK原理+乐城项目+PubMed临床数据+患者选择+Q&A |
| 三 | 知识库/专题三-慢阻肺COPD.md | COPD基础+ASCs治疗+现有方案对比+PubMed临床数据 |
| 四 | 知识库/专题四-膝关节干细胞.md | 骨关节炎+MSC治疗+各方案对比+PubMed临床数据+销售话术 |

**配套文件：**
- 知识库/四大专题总览.md — 一页总览
- 知识库/现有治疗方案vs新方法横向对比.md — 四病种横向对比

**更新节奏：** 每周五PubMed API自动检查最新文献
**使用：** 视频脚本/对客讲解/精算师视角分析

## 调研龙虾架构（2026-05-22重构）

**三龙虾并行：**
- 调研龙虾-A（6:30）：搜乐城政策 → growth/daily/ccfa1206/raw/lecheng_raw.md
- 调研龙虾-B（6:30）：搜新药审批 → growth/daily/ccfa1206/raw/newdrug_raw.md
- 汇总龙虾（6:40）：合并+写报告+发飞书

**配置：** 模型minimax-m2.7，超时300秒，prompt精简为三行

**禁用：** 旧调研龙虾（ccfa1206），prompt太重导致超时
"""

mem_path = r'C:\Users\Administrator\.openclaw-autoclaw\workspace\MEMORY.md'
with open(mem_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the 四大专题 section if it exists
if '## 四大专题知识库（2026-05-22建立）' in content:
    # Find and replace
    start = content.find('## 四大专题知识库（2026-05-22建立）')
    end = content.find('## 早报视频全自动流水线', start)
    if end > start:
        content = content[:start] + new_section.strip() + '\n\n' + content[end:]
        print('Replaced existing 四大专题 section')
else:
    # Insert before 早报视频 section
    marker = '## 早报视频全自动流水线'
    if marker in content:
        idx = content.find(marker)
        content = content[:idx] + new_section.strip() + '\n\n' + content[idx:]
        print('Inserted before 早报视频 section')
    else:
        content += '\n' + new_section
        print('Appended at end')

with open(mem_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('MEMORY.md updated successfully')