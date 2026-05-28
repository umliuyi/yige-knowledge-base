# -*- coding: utf-8 -*-
"""
飞书群客服机器人核心模块
===============================
功能：知识库问答 + 消息处理 + 飞书接入点（注释）

作者：编程龙虾
版本：v1.0
"""

import re
import json
import time
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher

# ============================================================
# 第一部分：知识库模块
# ============================================================

class KnowledgeBase:
    """
    知识库类：管理所有问答对，支持关键词+模糊匹配
    """

    def __init__(self):
        self.qa_pairs: List[Dict] = []
        self._load_knowledge()

    def _load_knowledge(self):
        """加载所有知识库内容"""
        self.qa_pairs = []

        # --------------------------------------------------
        # 1. 权益卡核心QA（15对+）
        # --------------------------------------------------
        equity_qa = [
            {
                "question": "权益卡多少钱？权益卡价格？买权益卡要多少钱？",
                "keywords": ["价格", "多少钱", "费用", "买卡", "购买", "收费", "报价", "价钱"],
                "answer": """【权益卡价格】

您好！权益卡是您享受乐城医疗特区专属权益的通行证。

📌 具体价格根据您选择的权益等级有所不同：
• 基础版权益卡：¥XXX/年
• 尊享版权益卡：¥XXX/年
• 至尊版权益卡：¥XXX/年

💡 包含的核心权益：
✅ 乐城先行区特药械优先使用权
✅ 专业医疗咨询服务
✅ 预约绿色通道
✅ 更多专属福利...

👉 如需了解详细价格和权益对比，请回复"权益卡套餐"，或直接联系我们获取最新报价！"""
            },
            {
                "question": "权益卡有什么权益？权益包括什么？",
                "keywords": ["权益", "包含", "服务", "福利", "内容", "有什么用", "功能", "好处"],
                "answer": """【权益卡核心权益】

您好！权益卡为您提供14项核心服务：

🏥 医疗服务类
1. 乐城特药械优先使用
2. 专家预约绿色通道
3. 全程导诊陪诊服务
4. 跨境医疗咨询服务

💊 药品相关类
5. 特殊药品代购服务
6. 用药指导与随访
7. 药品真伪验证

📋 权益服务类
8. 健康档案管理
9. 年度体检优惠
10. 第二诊疗意见
11. 术后康复指导
12. 营养师咨询
13. 心理疏导服务
14. 专属客服1对1服务

如有疑问，欢迎进一步咨询！"""
            },
            {
                "question": "权益卡适合人群？谁适合买？什么人适合？",
                "keywords": ["适合", "人群", "对象", "群体", "什么人", "谁适合", "适用人群"],
                "answer": """【权益卡适合人群】

您好！权益卡特别适合以下人群：

✅ 肿瘤/重症患者
   - 需要使用乐城先行区特许药械的患者
   - 寻求海外最新药物的患者

✅ 慢性病患者
   - 需要长期用药、定期复查的患者
   - 希望获得专业用药指导的患者

✅ 亚健康人群
   - 关注健康管理、预防医学的人群
   - 希望享受高端医疗服务的人群

✅ 追求品质医疗的人群
   - 希望获得VIP就医体验的患者
   - 需要专家绿色通道服务的患者

✅ 跨境医疗需求者
   - 有海外就医、体检需求的家庭
   - 希望获取国际第二诊疗意见的患者

您属于哪类人群呢？可以告诉我您的具体情况，我帮您推荐最适合的方案~"""
            },
            {
                "question": "CAR-T是什么？CAR-T治疗是什么？CAR-T免疫疗法？",
                "keywords": ["CAR-T", "cart", "免疫疗法", "细胞治疗", "CAR-T治疗", "嵌合抗原受体"],
                "answer": """【CAR-T细胞治疗介绍】

您好！CAR-T是当前最先进的肿瘤免疫治疗方法之一。

🔬 什么是CAR-T？
CAR-T全称"嵌合抗原受体T细胞疗法"（Chimeric Antigen Receptor T-Cell Therapy），是一种通过基因工程技术改造患者自身T细胞，使其能够精准识别并杀灭癌细胞的革命性治疗方法。

📋 治疗流程：
1. 采集患者T细胞
2. 实验室基因改造
3. 大量扩增改造后的CAR-T细胞
4. 回输患者体内
5. 持续监测与随访

✨ 优势：
• 精准打击癌细胞
• 一次治疗可能长期有效
• 对难治性肿瘤有效

📍 乐城先行区优势：
乐城是中国最早落地CAR-T治疗的特区，可以合法使用国际最新CAR-T产品，无需出国即可享受国际前沿治疗。

💰 关于费用：
CAR-T治疗费用较高，具体费用因治疗方案而异，欢迎私信了解详细报价。

有更多问题欢迎继续咨询！"""
            },
            {
                "question": "CAR-T治疗费用多少钱？CAR-T价格？",
                "keywords": ["CAR-T费用", "CAR-T价格", "CAR-T多少钱", "CAR-T收费"],
                "answer": """【CAR-T治疗费用参考】

您好！CAR-T治疗属于高端个性化治疗，费用因患者情况而异：

💰 费用构成：
• 采血和细胞培养：基础费用
• CAR-T细胞制备：主要成本（个性化定制）
• 回输治疗及住院：根据疗程
• 后续监测随访：定期复查

📊 市场价格区间：
• 国内已上市CAR-T产品：约100-120万人民币/次
• 乐城可用的国际最新CAR-T：费用因产品而异

💡 温馨提示：
1. 具体费用需评估患者病情后确定
2. 部分产品可能有慈善援助政策
3. 建议先做详细评估了解适合的治疗方案

👉 立即预约专家评估，了解您的具体情况和费用方案！"""
            },
            {
                "question": "CAR-T适合哪些疾病？哪些癌症可以用CAR-T？",
                "keywords": ["CAR-T适应症", "CAR-T适用", "哪些病", "什么癌症", "适应疾病"],
                "answer": """【CAR-T适应症】

您好！CAR-T细胞治疗主要用于以下疾病：

🩸 血液肿瘤：
• 复发或难治性B细胞急性淋巴细胞白血病（B-ALL）
• 弥漫性大B细胞淋巴瘤（DLBCL）
• 滤泡性淋巴瘤（FL）
• 套细胞淋巴瘤（MCL）
• 多发性骨髓瘤（MM）
• 原发性纵隔大B细胞淋巴瘤

🔬 研究中/逐步获批适应症：
• 急性髓系白血病（AML）
• T细胞淋巴瘤
• 实体瘤（如脑胶质瘤、肝癌、胰腺癌等）- 仍在研究中

⏰ 重要提示：
• CAR-T治疗需要专业医生评估
• 不同产品适应症不同
• 乐城可使用国际最新获批产品

📋 建议：
如需评估是否适合CAR-T治疗，请提供您的病情信息，我们安排专家为您评估！"""
            },
            {
                "question": "权益卡怎么办理？如何购买权益卡？权益卡购买流程？",
                "keywords": ["购买", "办理", "开通", "注册", "申请", "流程", "步骤", "怎么买"],
                "answer": """【权益卡购买流程】

您好！购买权益卡非常简单：

📋 办理流程：
1️⃣ 咨询了解 → 联系我们确认需求
2️⃣ 选择套餐 → 根据您的需求选择权益等级
3️⃣ 提交资料 → 提供必要个人信息
4️⃣ 支付费用 → 完成付款
5e⃣ 开通权益 → 1-3个工作日内开通
6️⃣ 享受服务 → 开始您的专属权益之旅

💬 购买方式：
• 微信联系顾问直接购买
• 拨打服务热线
• 扫码进群咨询

📱 所需信息：
• 姓名 + 手机号
• 身份证号码（部分服务需要）
• 健康状况（便于提供精准服务）

⏰ 服务时间：
工作日 9:00-18:00，24小时内必有回复！

如需人工帮助，请直接回复"转人工"，我们的客服将为您服务！"""
            },
            {
                "question": "权益卡和乐城卡有什么区别？是一回事吗？",
                "keywords": ["区别", "不同", "一样吗", "关系", "是什么卡"],
                "answer": """【权益卡与乐城卡的关系】

您好！很多朋友都有这个疑问，让我来解释：

🔗 关系说明：
"权益卡"和"乐城卡"通常指的是同一张卡，只是叫法不同。

📍 这张卡的核心价值：
• 是您在乐城国际医疗旅游先行区享受专属权益的凭证
• 凭此卡可享受特药优先、专家预约、绿色通道等服务

💡 为什么有不同的名称？
• "乐城卡" → 强调地域（乐城专属）
• "权益卡" → 强调功能（多项权益）

✅ 无论您叫什么，都是同一张卡，享受同样的服务！

如有其他疑问，欢迎继续咨询~"""
            },
            {
                "question": "权益卡有效期多久？过期了怎么办？",
                "keywords": ["有效期", "过期", "多久", "时间", "续费", "续期", "年费"],
                "answer": """【权益卡有效期说明】

您好！关于权益卡有效期：

📅 有效期规则：
• 权益卡有效期为1年（从购买之日起计算）
• 到期前30天内可申请续费续期
• 续费可享受老客户优惠

⏰ 过期后怎么办？
• 过期后权益暂停，但您的健康档案保留
• 可随时续费恢复全部权益
• 续费价格通常有优惠

💡 温馨提示：
• 建议到期前及时续费，避免服务中断
• 续费时如信息有变请及时更新
• 续费后即刻恢复所有权益

如需续费或有其他问题，请联系您的专属客服！"""
            },
            {
                "question": "权益卡可以退款吗？可以退吗？",
                "keywords": ["退款", "退费", "退货", "取消", "退款政策"],
                "answer": """【退款政策说明】

您好！关于退款问题：

📋 退款规则：
• 购买后7天内（如未使用服务）：可申请全额退款
• 购买后7-30天（如未使用核心服务）：可申请部分退款
• 购买超过30天：按照实际使用情况核算退款

❌ 不适用退款情况：
• 已使用核心医疗服务
• 已预约专家并产生费用
• 定制化服务已开始执行

💡 退款流程：
1. 联系客服申请退款
2. 提供订单信息
3. 核实使用情况
4. 财务退款（5-7个工作日）

如有疑问，欢迎咨询！"""
            },
            {
                "question": "权益卡有14项服务具体是什么？",
                "keywords": ["14项", "14", "服务项目", "具体服务"],
                "answer": """【权益卡14项核心服务详解】

您好！权益卡包含以下14项服务：

🏥【医疗服务类】4项
1️⃣ 乐城特药械优先使用
2️⃣ 专家预约绿色通道
3️⃣ 全程导诊陪诊服务
4️⃣ 跨境医疗咨询服务

💊【药品相关类】3项
5️⃣ 特殊药品代购服务
6️⃣ 用药指导与随访
7️⃣ 药品真伪验证

📋【健康管理类】7项
8️⃣ 健康档案管理
9️⃣ 年度体检优惠
🔟 第二诊疗意见
1️⃣1️⃣ 术后康复指导
1️⃣2️⃣ 营养师咨询
1️⃣3️⃣ 心理疏导服务
1️⃣4️⃣ 专属客服1对1服务

💎 尊享版/至尊版额外增加：
• 更多专家号源
• 更快速的绿色通道
• 私人健康管家服务

如需了解某个服务的详细内容，请告诉我！"""
            },
            {
                "question": "权益卡包含特药吗？有哪些特药？",
                "keywords": ["特药", "特许药械", "药品", "新药", "进口药"],
                "answer": """【乐城特药介绍】

您好！乐城先行区最大的优势之一就是可以使用国际最新药械！

💊 特药优势：
✅ 先行区享有"特许药械"政策
✅ 国际最新获批的药物可在乐城先行使用
✅ 无需出国即可用上国际新药
✅ 部分药物价格比海外更低

🏥 部分可获取的特药类别：
• 肿瘤免疫药物（PD-1/PD-L1等）
• 靶向药物（多种实体瘤）
• CAR-T细胞治疗产品
• 罕见病药物
• 眼科特许药械
• 体检早筛产品

💡 特药获取流程：
1. 咨询了解适合的药物
2. 专家评估确认方案
3. 协助采购/申请
4. 在乐城使用

📋 具体药物和费用需评估后确定，欢迎联系我们！"""
            },
            {
                "question": "我是患者家属可以购买权益卡吗？",
                "keywords": ["家属", "家人", "代替", "代购", "帮别人买", "患者家属"],
                "answer": """【家属购买权益卡】

您好！当然可以！

👨‍👩‍👧‍👦 家属完全可以为患者购买：
• 子女为父母购买
• 配偶之间互相购买
• 子女为子女购买
• 任何人均可购买

📋 购买时需注意：
1. 提供患者的真实健康信息
2. 购买后服务对象为患者本人
3. 家属可作为紧急联系人
4. 沟通时可由家属代为咨询

💡 建议：
• 如实告知患者病情，以便我们提供更精准的服务
• 保留好购买凭证
• 了解患者本人意愿

❤️ 我们的服务：
• 全程1对1专属服务
• 尊重患者隐私
• 尽心协助每一位患者

有更多问题欢迎咨询！"""
            },
            {
                "question": "没有病可以买权益卡吗？健康人需要吗？",
                "keywords": ["健康人", "没病", "正常人", "预防", "体检", "亚健康"],
                "answer": """【健康人群是否需要权益卡】

您好！这个问题很好！

💡 权益卡的价值不仅限于患者：

🏥 健康人群的价值：
✅ 年度体检优惠套餐
✅ 早筛早检服务（乐城特色）
✅ 专家健康咨询
✅ 跨境体检服务
✅ 健康档案建立
✅ 营养师/运动指导

🌟 乐城独特优势：
• 引进国际最新体检早筛技术
• 精密体检早于国内普通体检发现早期问题
• 部分高端人群专程来乐城做体检

👥 特别推荐：
• 有家族病史的人群
• 亚健康状态人群（长期疲劳、压力大）
• 35岁以上定期体检人群
• 追求高品质医疗服务的精英人群

💰 投资健康是最好的投资！

如需了解更多，回复"权益卡套餐"获取详细介绍~"""
            },
            {
                "question": "权益卡和保险有什么区别？",
                "keywords": ["保险", "区别", "不同", "对比", "医疗险", "重疾险"],
                "answer": """【权益卡 vs 医疗保险】

您好！这是个好问题，两者有本质区别：

📋 权益卡 = 医疗服务通行证
• 享受乐城专属医疗服务的资格
• 包含预约、陪诊、咨询等服务
• 享受特药优先权和绿色通道
• 类似"高端医疗会员卡"

🏥 医疗保险 = 费用报销
• 生病后报销医疗费用
• 事后补偿型
• 需要先花钱再报销
• 可能有免赔额、报销比例限制

💡 两者的关系：
权益卡 + 医疗保险 = 更全面的保障
• 权益卡解决"看得上、看得好"的问题
• 医疗保险解决"看得起"的问题
• 两者互补，不冲突

🎁 权益卡额外价值：
• 不是所有人都能享受的专属通道
• 节省时间、享受更好服务
• 部分产品和服务是金钱买不到的

有更多问题欢迎咨询！"""
            },
        ]

        # --------------------------------------------------
        # 2. 乐城项目核心QA（10对+）
        # --------------------------------------------------
        lecheng_qa = [
            {
                "question": "乐城有什么热门项目？乐城推荐项目？",
                "keywords": ["热门", "推荐", "特色", "明星项目", "主要项目", "有什么"],
                "answer": """【乐城热门医疗项目】

您好！乐城先行区有很多国际领先的医疗项目：

🌟 热门项目：

1️⃣ 肿瘤免疫治疗
   - CAR-T细胞治疗
   - PD-1/PD-L1免疫治疗
   - 树突细胞治疗

2️⃣ 精准体检/早筛
   - 肿瘤标志物精筛
   - 基因检测
   - 肠癌早筛

3️⃣ 眼科服务
   - 特许人工晶体植入
   - 青少年近视防控
   - 干眼症治疗

4️⃣ 再生医学
   - 干细胞治疗
   - 干细胞抗衰老
   - 膝关节干细胞修复

5️⃣ 辅助生殖
   - 试管婴儿
   - 胚胎冷冻

6️⃣ 运动医学
   - 膝关节PRP/干细胞治疗
   - 运动损伤康复

您对哪类项目感兴趣？我来帮您详细介绍！"""
            },
            {
                "question": "干细胞治疗是什么？干细胞有什么用？",
                "keywords": ["干细胞", "stem cell", "细胞治疗", "干细胞治疗", "干细胞移植"],
                "answer": """【干细胞治疗介绍】

您好！干细胞被称为"万能细胞"，是当前再生医学的核心。

🔬 什么是干细胞？
干细胞是具有自我复制和多向分化潜能的原始细胞，可以分化成人体各种类型的细胞（如神经细胞、肌肉细胞、骨细胞等）。

💡 干细胞治疗原理：
• 补充和修复受损组织
• 调节免疫功能
• 分泌生长因子促进愈合
• 抗炎作用

🏥 乐城热门干细胞项目：

1️⃣ 膝关节干细胞修复
   - 适应：膝关节炎、运动损伤
   - 效果：修复软骨、减轻疼痛

2️⃣ 干细胞抗衰老
   - 改善精力、睡眠
   - 调节亚健康状态

3️⃣ 干细胞治疗帕金森
   - 国内正在临床试验阶段
   - 乐城有部分服务

4️⃣ 干细胞美容
   - 面部抗衰
   - 改善肤质

📋 治疗流程：
评估 → 方案制定 → 干细胞采集/来源 → 培养 → 回输 → 随访

💰 费用：因项目而异，欢迎咨询获取详细报价

如需了解更多信息，请告诉我您的需求！"""
            },
            {
                "question": "干细胞治疗费用多少？干细胞多少钱？",
                "keywords": ["干细胞费用", "干细胞价格", "干细胞多少钱", "干细胞收费"],
                "answer": """【干细胞治疗费用参考】

您好！干细胞治疗费用因项目而异：

💰 常见干细胞项目费用：

1️⃣ 膝关节干细胞修复
   • 约 ¥3-8万/次
   • 通常需要1-3次疗程

2️⃣ 干细胞抗衰老（全身）
   • 约 ¥5-20万/疗程
   • 根据方案定制

3️⃣ 干细胞面部美容
   • 约 ¥1-5万/次
   • 疗程更优惠

4️⃣ 特定疾病治疗
   • 费用需评估后确定
   • 部分项目有慈善援助

📋 费用影响因素：
• 干细胞来源（自体/异体）
• 细胞数量和活性要求
• 治疗次数和疗程
• 配套服务

💡 温馨提示：
• 具体费用需面诊评估后确定
• 部分项目可分期付款
• 建议先做健康评估了解适合方案

👉 如需了解适合您的方案和费用，请联系我们的专家！"""
            },
            {
                "question": "乐城预约流程？怎么预约乐城？",
                "keywords": ["预约", "挂号", "预约流程", "怎么预约", "预约方式", "挂号"],
                "answer": """【乐城预约流程】

您好！预约乐城服务非常简单：

📋 预约流程：

Step 1️⃣ 咨询了解
• 告诉我们您的需求
• 了解项目详情和费用

Step 2️⃣ 提交资料
• 提供基本信息（姓名、手机、身份证）
• 提交相关病历资料（如有）

Step 3️⃣ 专家评估
• 我们的专家为您评估
• 确认是否适合该项目
• 制定个性化方案

Step 4️⃣ 确认预约
• 确认到院时间
• 发送预约确认函
• 告知注意事项

Step 5️⃣ 到院就诊
• 绿色通道接待
• 全程导诊陪诊

Step 6️⃣ 后续服务
• 用药指导
• 定期随访
• 持续健康管理

💬 预约方式：
• 微信联系顾问
• 拨打服务热线
• 进群咨询

⏰ 预约时间：
• 提前3-7天预约为最佳
• 节假日需提前更久
• 专家号源有限

回复"转人工"立即获得一对一服务！"""
            },
            {
                "question": "乐城有哪些医院？乐城医院列表？",
                "keywords": ["医院", "医疗机构", "哪些医院", "乐城医院", "和睦家", "博鳌"],
                "answer": """【乐城先行区医院介绍】

您好！乐城国际医疗旅游先行区有多家顶级医疗机构：

🏥 知名医院：

1️⃣ 博鳌超级医院
   • 共享平台模式
   • 院士专家团队
   • 特许药械使用

2️⃣ 博鳌恒大国际医院
   • 肿瘤专科医院
   • 布莱根和丹娜法伯战略合作
   • 国际最新肿瘤治疗

3️⃣ 博鳌乐城和睦家医疗中心
   • 高端全科服务
   • 国际标准的疫苗服务
   • 辅助生殖

4️⃣ 博鳌一龄生命养护中心
   • 高端体检
   • 干细胞抗衰老
   • 亚健康调理

5️⃣ 博鳌国际医院
   • 综合医院
   • 精准医疗中心

6️⃣ 慈铭国际医院
   • 体检早筛
   • 基因检测

7️⃣ 其他专科机构
   • 眼科中心
   • 耳鼻喉科
   • 康复中心

💡 我们的服务：
• 根据您的需求推荐最适合的医院
• 协助预约专家
• 全程导诊服务

如有需要，请告诉我们您的需求！"""
            },
            {
                "question": "去乐城需要办理什么手续？乐城就医要什么证件？",
                "keywords": ["手续", "证件", "材料", "准备", "要求", "通行证", "签证"],
                "answer": """【乐城就医所需材料】

您好！乐城在国内，就医手续非常方便：

📋 国内居民（无需出境）：
✅ 身份证（必备）
✅ 医保卡（如有）
✅ 相关病历资料
✅ 检查报告（如有）
✅ 病理切片/影像片子（如有）

🏥 特殊项目可能需要：
• 专家评估后的治疗方案
• 特殊用药申请批文（院方处理）

🌍 境外人士：
• 护照
• 签证（如需要）
• 其他身份证件

💡 出行准备：
• 订好往返机票/火车票
• 预订酒店（我们可协助）
• 了解当地天气
• 带上必要生活用品

🚗 交通指南：
• 飞：海口美兰机场 → 动车/自驾到琼海
• 飞：琼海博鳌机场（少量航班）
• 动：海口/三亚 → 琼海站

💡 我们可以提供：
• 交通指南
• 住宿推荐
• 接送服务（部分套餐）

有更多问题欢迎咨询！"""
            },
            {
                "question": "乐城项目可以医保报销吗？",
                "keywords": ["医保", "报销", "社保", "商业保险", "保险"],
                "answer": """【乐城医保/报销政策】

您好！关于报销问题：

💳 医保情况：
• 博鳌乐城执行海南医保政策
• 部分基础项目可医保结算
• 特许药械项目多为自费

🏥 报销可能性：
1️⃣ 基础检查/治疗 → 可用医保
2️⃣ 特许药械/进口药物 → 自费
3️⃣ 高端服务套餐 → 自费
4️⃣ 干细胞治疗 → 自费

💡 商业保险：
• 部分商业医疗险可报销
• 需查看保险条款
• 建议提前咨询保险公司

📋 建议：
• 先确认您的医保类型
• 了解保险报销范围
• 我们可提供发票和病历用于报销

💰 费用透明：
• 就医前提供详细费用预估
• 无隐形消费
• 各项费用明码标价

如需了解具体项目的费用和报销情况，请告诉我！"""
            },
            {
                "question": "去乐城干细胞治疗需要住院吗？",
                "keywords": ["住院", "当天", "停留", "时间", "多久", "干细胞疗程"],
                "answer": """【干细胞治疗住院情况】

您好！关于干细胞治疗是否住院：

💉 项目类型不同：

1️⃣ 膝关节干细胞注射
• 通常：门诊治疗
• 住院：通常不需要
• 留观：注射后休息1-2小时

2️⃣ 干细胞抗衰老（静脉回输）
• 通常：门诊治疗
• 住院：不需要
• 留观：30分钟-1小时

3️⃣ 住院干细胞治疗
• 部分重症治疗需要住院
• 住院时间：数天至数周不等

📅 整体时间安排：
• 前期评估：半天~1天
• 干细胞采集（如自体）：1天
• 等待培养：2-4周
• 回输治疗：半天
• 总行程建议：3-5天（可顺便游玩）

💡 建议：
• 提前预约专家评估
• 安排好时间
• 干细胞治疗建议有人陪同

如有更多问题，请告诉我您的具体情况！"""
            },
            {
                "question": "乐城和睦家和博鳌超级医院哪个好？",
                "keywords": ["和睦家", "超级医院", "博鳌", "哪个好", "选择", "对比"],
                "answer": """【乐城医疗机构对比】

您好！这几个机构各有特色：

🏥 博鳌超级医院
• 定位：共享医院平台
• 优势：院士专家团队强大
• 特色：疑难重症、特许药械
• 适合：肿瘤、复杂病症

🏥 博鳌乐城和睦家
• 定位：高端全科
• 优势：国际标准、服务好
• 特色：疫苗、辅助生殖、体检
• 适合：健康人群、高端体检

🏥 一龄生命养护中心
• 定位：高端抗衰老
• 优势：环境好、套餐服务
• 特色：干细胞抗衰、亚健康调理
• 适合：亚健康、抗衰需求

🏥 恒大国际医院
• 定位：肿瘤专科
• 优势：与丹娜法伯合作
• 特色：国际最新肿瘤治疗
• 适合：肿瘤患者

💡 如何选择？
• 先告诉我们的您的需求
• 我们会根据您的病情推荐
• 也可以多咨询几家对比

有具体问题欢迎继续咨询！"""
            },
            {
                "question": "乐城辅助生殖有什么优势？试管婴儿？",
                "keywords": ["辅助生殖", "试管婴儿", "试管", "生殖", "不孕", "冻卵", "胚胎"],
                "answer": """【乐城辅助生殖介绍】

您好！乐城的辅助生殖服务有很大优势：

🌟 乐城辅助生殖优势：

1️⃣ 政策优势
• 乐城享有特许政策
• 可使用国际最新技术和药物
• 部分在国内尚未获批的产品可在乐城使用

2️⃣ 技术优势
• 国际同步的胚胎实验室
• 经验丰富的专家团队
• 与国际顶尖机构合作

3️⃣ 药物优势
• 进口促排卵药物
• 最新拮抗剂方案
• 减少副作用

4️⃣ 服务优势
• 一对一全程服务
• 预约制减少等待
• 良好的就医环境

💼 服务项目：
• 试管婴儿（IVF-ET）
• 胚胎植入前遗传学筛查（PGS）
• 冷冻卵子/胚胎
• 男科服务

💰 费用参考：
• 试管婴儿：约¥8-15万/周期
• 具体因方案而异

📋 流程：
评估 → 方案制定 → 促排卵 → 取卵/取精 → 胚胎培养 → 移植 → 验孕

欢迎告诉我们您的具体情况！"""
            },
        ]

        # --------------------------------------------------
        # 3. 通用引导QA
        # --------------------------------------------------
        guide_qa = [
            {
                "question": "转人工！转人工服务！想要人工客服！",
                "keywords": ["转人工", "人工", "人工客服", "客服", "人工服务", "真人", "有人吗"],
                "answer": """【转接人工服务】

您好！正在为您转接人工客服~

⏳ 请稍等片刻：
• 人工客服将在5分钟内回复
• 工作时间：周一至周五 9:00-18:00
• 非工作时间请留言，稍后回复

💬 如急需帮助：
• 微信搜索并添加顾问微信
• 拨打服务热线

🔄 留言方式：
• 直接描述您的问题
• 留下联系方式
• 我们会第一时间回复

感谢您的耐心等待！🙏"""
            },
            {
                "question": "加微信！怎么加微信？微信号？",
                "keywords": ["微信", "加微信", "微信号", "vx", "加v", "联系微信"],
                "answer": """【添加微信】

您好！想要添加我们的微信吗？

📱 微信联系：
• 请回复您的手机号
• 或直接告诉我们您的微信
• 我们的顾问会主动加您

💬 微信服务内容：
• 1对1专属咨询
• 最新活动推送
• 预约提醒服务
• 专人跟进服务

⏰ 回复时间：
• 工作时间：5分钟内回复
• 非工作时间：24小时内回复

🌟 强烈建议加微信：
• 获取第一手资讯
• 享受专属优惠
• 咨询更方便快捷

请告诉我您的手机号或微信，我们马上联系您！"""
            },
            {
                "question": "进入社群！怎么进群？群聊！",
                "keywords": ["进群", "加群", "群", "社群", "微信群", "群聊", "加入群"],
                "answer": """【加入我们的社群】

您好！想要加入我们的微信群吗？

🌟 社群福利：
• 第一时间获取活动优惠
• 与专业人士交流
• 分享健康资讯
• 不定期专家讲座

📋 入群方式：
1️⃣ 方法一：回复您的手机号，我们拉您入群
2️⃣ 方法二：让已入群的朋友邀请您
3️⃣ 方法三：关注公众号，菜单栏有入群入口

💡 入群后请：
• 修改群昵称为"姓名+需求"
• 遵守群规
• 积极互动交流

❌ 群内禁止：
• 发广告
• 发无关链接
• 人身攻击

欢迎加入我们的大家庭！🎉"""
            },
            {
                "question": "你们的联系方式？电话多少？电话？",
                "keywords": ["电话", "联系方式", "热线", "手机", "联系", "电话多少", "拨打"],
                "answer": """【联系我们】

您好！以下是我们的联系方式：

📞 联系电话：
• 客服热线：400-XXX-XXXX
• 顾问手机：[请回复手机号获取]

💬 微信：
• 关注公众号后联系
• 或回复"加微信"获取

📍 地址：
• 海南琼海市博鳌乐城国际医疗旅游先行区

⏰ 服务时间：
• 周一至周五：9:00-18:00
• 周六：9:00-12:00
• 周日及节假日：休息

💌 在线咨询：
• 微信：工作时间内即时回复
• 官网：www.xxxx.com

📱 建议：
• 拨打热线快速咨询
• 或留下您的电话，我们回拨给您

感谢您的关注！"""
            },
            {
                "question": "你好！打招呼！Hello！",
                "keywords": ["你好", "您好", "hi", "hello", "hi", "早上好", "晚上好", "在吗", "在不在"],
                "answer": """您好！👋 欢迎来到乐城健康服务中心！

我是您的智能客服助手，很高兴为您服务！

🏥 我可以帮您解答：
• 权益卡相关问题（价格、权益、购买）
• 乐城热门医疗项目
• 干细胞治疗
• CAR-T免疫治疗
• 预约流程咨询
• 其他健康相关问题

💡 试试这样问我：
• "权益卡多少钱？"
• "乐城有什么项目？"
• "CAR-T是什么？"
• "怎么预约？"

当然，如果您需要人工客服，随时回复"转人工"~

请问有什么可以帮到您？"""
            },
            {
                "question": "感谢！谢谢！THX！Thanks！",
                "keywords": ["谢谢", "感谢", "谢", "thx", "thanks", "感激", "多谢"],
                "answer": """不客气！😊

很高兴能帮到您！

💡 温馨提示：
• 如有其他问题，随时咨询
• 回复"转人工"可联系客服
• 回复"加微信"获取专属顾问

祝您健康！🌟"""
            },
        ]

        # 合并所有QA
        self.qa_pairs.extend(equity_qa)
        self.qa_pairs.extend(lecheng_qa)
        self.qa_pairs.extend(guide_qa)

    def get_all_qa_count(self) -> Dict:
        """获取各类QA数量"""
        equity_count = sum(1 for qa in self.qa_pairs if any(k in str(qa.get("question", "")) for k in ["权益", "权益卡", "CAR-T"]))
        lecheng_count = sum(1 for qa in self.qa_pairs if any(k in str(qa.get("question", "")) for k in ["乐城", "干细胞", "医院", "预约"]))
        guide_count = len(self.qa_pairs) - equity_count - lecheng_count
        return {
            "equity_qa": len([qa for qa in self.qa_pairs if any(k in qa.get("question", "") for k in ["权益卡", "CAR-T", "适合人群", "14项", "权益", "特药"])]),
            "lecheng_qa": len([qa for qa in self.qa_pairs if any(k in qa.get("question", "") for k in ["乐城", "干细胞", "医院", "预约"])]),
            "guide_qa": len([qa for qa in self.qa_pairs if any(k in qa.get("question", "") for k in ["转人工", "加微信", "进群", "联系方式", "你好", "谢谢"])]),
            "total": len(self.qa_pairs)
        }

    def extract_keywords(self, text: str) -> List[str]:
        """从用户输入中提取关键词"""
        # 简单分词 + 去除停用词
        stop_words = {"的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这", "那", "什么", "怎么", "吗", "呢", "吧", "啊", "哦", "嗯", "呀"}
        # 简单按标点和空格分词
        words = re.split(r'[\s,.!?，。！？、：:；;]+', text)
        keywords = [w for w in words if len(w) >= 2 and w not in stop_words]
        return keywords

    def calculate_similarity(self, s1: str, s2: str) -> float:
        """计算两个字符串的相似度（SequenceMatcher）"""
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

    def keyword_match_score(self, user_input: str, qa: Dict) -> float:
        """计算关键词匹配得分"""
        user_lower = user_input.lower()
        score = 0.0

        # 1. 直接匹配问题（高权重）
        for q in qa.get("question", "").split("|"):
            sim = self.calculate_similarity(user_input, q)
            score = max(score, sim * 3.0)  # 问题匹配权重3x

        # 2. 关键词匹配
        keywords = qa.get("keywords", [])
        for kw in keywords:
            if kw.lower() in user_lower:
                score += 1.0  # 每匹配一个关键词+1分

        # 3. 关键词反向验证：用户词与QA关键词的重叠
        user_words = set(self.extract_keywords(user_input))
        qa_kw_set = set(kw.lower() for kw in keywords)
        overlap = user_words & qa_kw_set
        score += len(overlap) * 0.5  # 重叠词额外加权

        return score

    def find_best_match(self, user_input: str) -> Tuple[Optional[Dict], float]:
        """
        查找最佳匹配的QA
        返回：(最佳QA, 得分)
        """
        best_qa = None
        best_score = 0.0
        min_threshold = 0.3  # 最低匹配阈值

        for qa in self.qa_pairs:
            score = self.keyword_match_score(user_input, qa)
            if score > best_score:
                best_score = score
                best_qa = qa

        if best_score >= min_threshold:
            return best_qa, best_score
        return None, 0.0


# ============================================================
# 第二部分：消息处理模块
# ============================================================

class MessageProcessor:
    """
    消息处理器：接收消息 → 提取关键词 → 匹配答案 → 返回回复
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.fallback_count = 0

    def process(self, user_message: str) -> str:
        """
        处理用户消息，返回回复内容
        """
        # 清洗消息
        user_message = user_message.strip()

        if not user_message:
            return "您好，请输入您的问题~"

        # 匹配最佳答案
        best_qa, score = self.kb.find_best_match(user_message)

        if best_qa:
            return best_qa["answer"]

        # 模糊匹配兜底
        return self._fuzzy_fallback(user_message)

    def _fuzzy_fallback(self, user_message: str) -> str:
        """模糊匹配兜底回复"""
        keywords = self.kb.extract_keywords(user_message)

        # 简单意图判断兜底
        msg_lower = user_message.lower()

        # 关心价格的
        if any(w in msg_lower for w in ["多少", "价格", "费用", "钱"]):
            return """【关于费用】

您好！您似乎在询问费用相关问题~

您可能感兴趣的内容：
💰 权益卡价格 → 回复"权益卡价格"
💰 CAR-T治疗费用 → 回复"CAR-T费用"
💰 干细胞治疗费用 → 回复"干细胞费用"

如果都不是您想了解的，欢迎直接描述您的问题，或者回复"转人工"咨询客服！"""

        # 关心预约的
        if any(w in msg_lower for w in ["预约", "挂号", "怎么"]):
            return """【预约服务】

您好！关于预约：

📋 快速预约方式：
• 回复"预约流程"了解详细步骤
• 回复"加微信"联系顾问直接预约
• 回复"转人工"获取帮助

💡 也可以直接告诉我：
• 您想了解的项目
• 您的基本情况
• 希望的到院时间

我来帮您安排！"""

        # 关心CAR-T或干细胞的
        if any(w in msg_lower for w in ["治疗", "什么", "哪些"]):
            return """【项目咨询】

您好！您可以尝试以下方式找到答案：

🔍 您可能想问：
• 回复"CART"了解CAR-T治疗
• 回复"干细胞"了解干细胞项目
• 回复"热门项目"了解乐城特色

💬 或者：
• 直接描述您的病情/需求
• 回复"转人工"有专人解答

希望对您有帮助！"""

        self.fallback_count += 1
        return f"""【未能识别问题】

您好！抱歉没有理解您的问题~

💡 您可以尝试：
• 换个方式描述您的问题
• 咨询常见问题（如：权益卡、预约流程）
• 回复"转人工"联系客服
• 回复"加微信"获得更详细的帮助

感谢您的理解！"""


# ============================================================
# 第三部分：飞书接入模块（注释说明）
# ============================================================

class FeishuConnector:
    """
    飞书接入模块

    ⚠️ 注意：以下代码为注释说明，实际使用需要飞书应用凭证
    ⚠️ 飞书应用需要在 https://open.feishu.cn 创建并配置
    """

    # ============================================================
    # 方式一：Webhook 签名校验 + 接收消息（适合简单的被动接收消息）
    # ============================================================

    """
    # 配置项（需要在飞书群机器人设置中获取）
    FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    FEISHU_VERIFICATION_TOKEN = "xxxxxxxxxxxxxxxxxxxx"  # 事件订阅的 Verification Token
    FEISHU_ENCRYPT_KEY = "xxxxxxxxxxxxxxxxxxxx"         # 可选：加密密钥

    def __init__(self, webhook_url: str, verification_token: str):
        self.webhook_url = webhook_url
        self.verification_token = verification_token

    # --------------------------------------------------
    # 1. 验证请求签名（飞书安全校验）
    # --------------------------------------------------
    def verify_sign(self, timestamp: str, sign: str) -> bool:
        '''
        飞书请求签名验证算法：
        1. 将 timestamp + "\n" + encrypt_key 作为待签名字符串
        2. 使用 HMAC SHA256 + Base64 进行签名
        3. 与请求中的 sign 参数比对
        '''
        import hmac
        import hashlib
        import base64

        if not FEISHU_ENCRYPT_KEY:
            return True  # 未启用加密时跳过

        string_to_sign = f"{timestamp}\n{FEISHU_ENCRYPT_KEY}"
        hmac_obj = hmac.new(
            string_to_sign.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha256
        )
        my_sign = base64.b64encode(hmac_obj.digest()).decode("utf-8")
        return my_sign == sign

    # --------------------------------------------------
    # 2. 处理接收到的飞书消息（Flask示例）
    # --------------------------------------------------
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route("/feishu/webhook", methods=["POST"])
    def feishu_webhook():
        '''
        飞书消息回调接口
        需要在飞书后台配置：事件订阅 → 请求地址配置
        '''
        # 1. 验证签名（生产环境必须验证）
        body = request.json
        if body.get("type") == "url_verification":
            # 飞书验证回调地址有效性
            return jsonify({" challenge": body.get("challenge") })

        # 2. 解密消息体（如果启用了加密）
        timestamp = request.headers.get("X-lark-timestamp", "")
        sign = request.headers.get("X-lark-signature", "")
        if not self.verify_sign(timestamp, sign):
            return jsonify({"error": "invalid signature"}), 403

        # 3. 解析消息
        event = body.get("event", {})
        msg_type = event.get("msg_type", "text")
        content = event.get("content", {})

        if msg_type == "text":
            user_text = content.get("text", "").strip()

            # 4. 调用消息处理器
            processor = MessageProcessor(KnowledgeBase())
            reply_text = processor.process(user_text)

            # 5. 通过 webhook 回复消息（被动响应，不需要 access_token）
            self.send_text_message(reply_text, event.get("chat_id"), event.get("message_id"))

        return jsonify({"code": 0, "msg": "success"})

    # --------------------------------------------------
    # 3. 通过 Webhook 发送文本消息
    # --------------------------------------------------
    def send_text_message(self, text: str, chat_id: str = None, message_id: str = None):
        '''
        通过飞书机器人 Webhook 发送文本消息

        REST API: POST https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_url}
        请求体: {"msg_type": "text", "content": {"text": "..."}}

        注意：这种方式只能发送消息，无法获取聊天历史
        如需更完整功能，请使用"方式二：调用飞书 IM API"
        '''
        import requests

        payload = {
            "msg_type": "text",
            "content": {
                "text": text
            },
            "chat_id": chat_id,  # 可选，指定发送的群
            "message_id": message_id  # 可选，回复指定消息
        }

        response = requests.post(self.webhook_url, json=payload)
        return response.json()
    """

    # ============================================================
    # 方式二：使用飞书 IM API（需要 Access Token）
    # ============================================================

    """
    # 配置项
    FEISHU_APP_ID = "cli_xxxxxxxxxxxx"        # 飞书应用的 App ID
    FEISHU_APP_SECRET = "xxxxxxxxxxxxxxxx"     # 飞书应用的 App Secret

    # --------------------------------------------------
    # 4. 获取 Access Token
    # --------------------------------------------------
    def get_access_token(self) -> str:
        '''
        获取 tenant_access_token（用于调用飞书 API）

        REST API: POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
        请求体: {"app_id": "...", "app_secret": "..."}

        返回: {"code": 0, "msg": "success", "tenant_access_token": "...", "expire": 7200}
        '''
        import requests

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.FEISHU_APP_ID,
            "app_secret": self.FEISHU_APP_SECRET
        }

        response = requests.post(url, json=payload)
        result = response.json()

        if result.get("code") == 0:
            return result.get("tenant_access_token", "")
        else:
            raise Exception(f"获取AccessToken失败: {result}")

    # --------------------------------------------------
    # 5. 发送消息（通过 IM API）
    # --------------------------------------------------
    def send_message_via_api(self, receive_id_type: str, receive_id: str, msg_type: str, content: dict):
        '''
        发送消息（支持私聊/群聊）

        REST API: POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}
        Headers: Authorization: Bearer {access_token}

        参数:
        - receive_id_type: open_id / chat_id
        - receive_id: open_id（私聊用户）或 chat_id（群聊）
        - msg_type: text / post / image / file 等
        - content: 消息内容 JSON

        返回: {"code": 0, "msg": "success", "data": {...}}
        '''
        import requests

        access_token = self.get_access_token()
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps(content)  # content 必须是 JSON 字符串
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    # --------------------------------------------------
    # 6. 接收消息（事件订阅 - 文档模式）
    # --------------------------------------------------
    # 参考: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python-sdk/event-subscription-overview
    #
    # 使用 Flask/Django 框架搭建 WebServer：
    # 1. 在飞书开放平台配置"事件订阅" → 请求地址URL
    # 2. 接收 GET 请求验证 URL（url_verification）
    # 3. 接收 POST 请求处理事件消息
    #
    # 示例（Flask）：
    #
    # from flask import Flask, request, jsonify
    # import os
    #
    # app = Flask(__name__)
    #
    # @app.route("/feishu/event", methods=["GET", "POST"])
    # def handle_feishu_event():
    #     if request.method == "GET":
    #         # URL 验证
    #         params = request.args
    #         challenge = params.get("challenge")
    #         if challenge:
    #             return jsonify({" challenge": challenge})
    #         return jsonify({"error": "missing challenge"}), 400
    #
    #     # POST: 处理事件
    #     body = request.json
    #     event = body.get("event", {})
    #     # ... 处理逻辑
    #     return jsonify({"code": 0})
    """

    # ============================================================
    # 方式三：直接接入点（使用本机器人模块时调用）
    # ============================================================

    @staticmethod
    def handle_feishu_message(message_content: str, chat_id: str = None, message_id: str = None) -> str:
        """
        处理飞书消息的接入点函数

        使用方式：
        from feishu_chatbot import FeishuConnector, KnowledgeBase, MessageProcessor

        # 初始化
        kb = KnowledgeBase()
        processor = MessageProcessor(kb)

        # 在您的 Webhook 路由中调用：
        def on_feishu_message(message: str, chat_id: str = None, message_id: str = None):
            reply = FeishuConnector.handle_feishu_message(message, chat_id, message_id)
            return reply

        # 然后将 reply 通过飞书 API 发送出去
        """
        kb = KnowledgeBase()
        processor = MessageProcessor(kb)
        reply = processor.process(message_content)
        return reply


# ============================================================
# 第四部分：主程序 / 演示
# ============================================================

def demo():
    """演示模式 - 本地测试知识库"""
    print("=" * 60)
    print("飞书客服机器人 - 演示模式")
    print("=" * 60)

    kb = KnowledgeBase()
    processor = MessageProcessor(kb)

    # 打印知识库统计
    counts = kb.get_all_qa_count()
    print(f"\n📊 知识库统计：")
    print(f"   权益卡核心QA：{counts['equity_qa']}对")
    print(f"   乐城项目核心QA：{counts['lecheng_qa']}对")
    print(f"   通用引导QA：{counts['guide_qa']}对")
    print(f"   总计：{counts['total']}对")
    print()

    # 测试用例
    test_cases = [
        "权益卡多少钱？",
        "CAR-T是什么？",
        "干细胞治疗费用",
        "怎么预约？",
        "你们有哪些医院？",
        "转人工",
        "加微信",
        "适合什么人买？",
        "可以退款吗",
        "有14项服务是什么",
    ]

    print("-" * 60)
    print("测试问答：")
    print("-" * 60)

    for i, test in enumerate(test_cases, 1):
        print(f"\n【测试 {i}】用户：{test}")
        reply = processor.process(test)
        # 打印回复的前100字符
        reply_preview = reply[:100].replace("\n", " ")
        print(f"   机器人：{reply_preview}...")
        best_qa, score = kb.find_best_match(test)
        print(f"   匹配得分：{score:.2f}")


if __name__ == "__main__":
    demo()
