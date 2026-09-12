"""
智能门诊辅助诊断知识库
Smart Clinic AI-Assisted Diagnosis Knowledge Base

基于临床路径的结构化推理引擎
"""

# 症状-诊断映射知识库
KNOWLEDGE_BASE = {
    "上呼吸道感染": {
        "symptoms": ["发热", "咳嗽", "咽痛", "鼻塞", "流涕", "打喷嚏"],
        "min_match": 3,
        "weight": 0.92,
        "category": "呼吸内科",
        "examinations": ["血常规", "C反应蛋白"],
        "medications": ["对乙酰氨基酚片", "复方甘草片"],
        "icd10": "J06.9"
    },
    "急性支气管炎": {
        "symptoms": ["咳嗽", "咳痰", "发热", "胸闷", "气促"],
        "min_match": 3,
        "weight": 0.85,
        "category": "呼吸内科",
        "examinations": ["血常规", "胸片", "痰培养"],
        "medications": ["阿莫西林胶囊", "氨溴索口服液", "布地奈德雾化液"],
        "icd10": "J20.9"
    },
    "肺炎": {
        "symptoms": ["高热", "咳嗽", "咳痰", "胸痛", "气促", "寒战"],
        "min_match": 3,
        "weight": 0.78,
        "category": "呼吸内科",
        "examinations": ["血常规", "胸片/CT", "血气分析", "痰培养"],
        "medications": ["头孢克洛胶囊", "左氧氟沙星片", "氨溴索口服液"],
        "icd10": "J18.9"
    },
    "急性胃肠炎": {
        "symptoms": ["恶心", "呕吐", "腹泻", "腹痛", "发热", "食欲下降"],
        "min_match": 3,
        "weight": 0.90,
        "category": "消化内科",
        "examinations": ["血常规", "大便常规", "电解质"],
        "medications": ["蒙脱石散", "口服补液盐", "奥美拉唑胶囊"],
        "icd10": "A09"
    },
    "胃炎": {
        "symptoms": ["上腹痛", "腹胀", "恶心", "嗳气", "食欲下降", "反酸"],
        "min_match": 3,
        "weight": 0.82,
        "category": "消化内科",
        "examinations": ["胃镜", "幽门螺杆菌检测", "血常规"],
        "medications": ["奥美拉唑胶囊", "铝碳酸镁片", "莫沙必利片"],
        "icd10": "K29.7"
    },
    "高血压": {
        "symptoms": ["头晕", "头痛", "耳鸣", "心悸", "视物模糊", "颈项僵硬"],
        "min_match": 2,
        "weight": 0.88,
        "category": "心血管内科",
        "examinations": ["血压监测", "心电图", "血脂", "肾功能", "眼底检查"],
        "medications": ["氨氯地平片", "缬沙坦胶囊"],
        "icd10": "I10"
    },
    "冠心病心绞痛": {
        "symptoms": ["胸痛", "胸闷", "心悸", "气促", "左肩放射痛", "出汗"],
        "min_match": 3,
        "weight": 0.75,
        "category": "心血管内科",
        "examinations": ["心电图", "心肌酶谱", "冠脉CTA", "心脏彩超"],
        "medications": ["硝酸甘油片", "阿司匹林肠溶片", "阿托伐他汀钙片"],
        "icd10": "I20.9"
    },
    "2型糖尿病": {
        "symptoms": ["多饮", "多尿", "多食", "体重下降", "视物模糊", "乏力"],
        "min_match": 3,
        "weight": 0.86,
        "category": "内分泌科",
        "examinations": ["空腹血糖", "糖化血红蛋白", "餐后血糖", "尿常规"],
        "medications": ["二甲双胍片", "格列齐特片"],
        "icd10": "E11"
    },
    "尿路感染": {
        "symptoms": ["尿频", "尿急", "尿痛", "腰痛", "发热", "血尿"],
        "min_match": 3,
        "weight": 0.91,
        "category": "泌尿外科",
        "examinations": ["尿常规", "尿培养", "泌尿系B超"],
        "medications": ["左氧氟沙星片", "碳酸氢钠片"],
        "icd10": "N39.0"
    },
    "偏头痛": {
        "symptoms": ["头痛", "恶心", "呕吐", "畏光", "畏声", "视物模糊"],
        "min_match": 3,
        "weight": 0.80,
        "category": "神经内科",
        "examinations": ["头颅CT/MRI", "脑电图"],
        "medications": ["布洛芬缓释胶囊", "盐酸氟桂利嗪胶囊"],
        "icd10": "G43.9"
    },
    "颈椎病": {
        "symptoms": ["颈痛", "肩痛", "上肢麻木", "头晕", "手指无力"],
        "min_match": 3,
        "weight": 0.84,
        "category": "骨科",
        "examinations": ["颈椎X线", "颈椎MRI"],
        "medications": ["塞来昔布胶囊", "甲钴胺片", "颈复康颗粒"],
        "icd10": "M54.2"
    },
    "腰椎间盘突出": {
        "symptoms": ["腰痛", "下肢放射痛", "下肢麻木", "行走困难", "弯腰受限"],
        "min_match": 3,
        "weight": 0.83,
        "category": "骨科",
        "examinations": ["腰椎MRI", "腰椎X线"],
        "medications": ["塞来昔布胶囊", "甲钴胺片", "腰痛宁胶囊"],
        "icd10": "M51.1"
    },
    "过敏性鼻炎": {
        "symptoms": ["鼻塞", "流涕", "打喷嚏", "鼻痒", "眼痒", "嗅觉减退"],
        "min_match": 3,
        "weight": 0.89,
        "category": "耳鼻喉科",
        "examinations": ["过敏原检测", "鼻内镜"],
        "medications": ["氯雷他定片", "布地奈德鼻喷剂"],
        "icd10": "J30.4"
    },
    "急性结膜炎": {
        "symptoms": ["眼红", "眼痒", "异物感", "分泌物增多", "畏光", "流泪"],
        "min_match": 3,
        "weight": 0.87,
        "category": "眼科",
        "examinations": ["裂隙灯检查", "结膜分泌物涂片"],
        "medications": ["左氧氟沙星滴眼液", "更昔洛韦眼用凝胶"],
        "icd10": "H10.3"
    },
    "湿疹": {
        "symptoms": ["皮疹", "瘙痒", "红斑", "渗出", "皮肤干燥", "脱屑"],
        "min_match": 3,
        "weight": 0.81,
        "category": "皮肤科",
        "examinations": ["过敏原检测", "皮肤镜"],
        "medications": ["氯雷他定片", "丁酸氢化可的松乳膏"],
        "icd10": "L30.9"
    },
    "失眠症": {
        "symptoms": ["入睡困难", "早醒", "多梦", "日间疲劳", "注意力下降", "焦虑"],
        "min_match": 3,
        "weight": 0.79,
        "category": "神经内科",
        "examinations": ["量表评估", "甲状腺功能"],
        "medications": ["佐匹克隆片", "谷维素片"],
        "icd10": "G47.0"
    },
    "贫血": {
        "symptoms": ["乏力", "头晕", "面色苍白", "心悸", "气促", "食欲下降"],
        "min_match": 3,
        "weight": 0.82,
        "category": "血液科",
        "examinations": ["血常规", "铁蛋白", "网织红细胞", "骨髓穿刺"],
        "medications": ["硫酸亚铁片", "叶酸片", "维生素B12注射液"],
        "icd10": "D50.9"
    },
    "痛风": {
        "symptoms": ["关节红肿", "关节剧痛", "发热", "第一跖趾关节痛", "活动受限"],
        "min_match": 3,
        "weight": 0.88,
        "category": "风湿免疫科",
        "examinations": ["血尿酸", "关节X线", "血常规", "肾功能"],
        "medications": ["秋水仙碱片", "非布司他片", "双氯芬酸钠缓释片"],
        "icd10": "M10.9"
    }
}

# 全部可用症状列表
ALL_SYMPTOMS = sorted(set(
    symptom
    for disease in KNOWLEDGE_BASE.values()
    for symptom in disease["symptoms"]
))

# 科室列表
ALL_DEPARTMENTS = sorted(set(
    disease["category"] for disease in KNOWLEDGE_BASE.values()
))
# 药品目录（去重）
ALL_MEDICATIONS = sorted(set(
    med
    for disease in KNOWLEDGE_BASE.values()
    for med in disease["medications"]
))

# 检查项目目录（去重）
ALL_EXAMINATIONS = sorted(set(
    exam
    for disease in KNOWLEDGE_BASE.values()
    for exam in disease['examinations']
))
# 过敏史-药品冲突映射
ALLERGY_DRUG_MAP = {
    '青霉素过敏': ['阿莫西林胶囊', '阿莫西林'],
    '磺胺类药物过敏': ['复方新诺明片', '磺胺甲噁唑'],
    '头孢类过敏': ['头孢克洛胶囊', '头孢呋辛', '头孢类'],
    '海鲜过敏': [],
    '花粉过敏': [],
}


# 演示医院数据
DEMO_HOSPITAL = {
    'name': '东方仁济医院',
    'address': '东方市健康大道168号',
    'departments': {
        '全科': [{'name': '陈建国', 'title': '主治医师'}],
        '呼吸内科': [{'name': '王志明', 'title': '主任医师'}, {'name': '李华', 'title': '副主任医师'}],
        '消化内科': [{'name': '张强', 'title': '主任医师'}, {'name': '刘芳', 'title': '副主任医师'}],
        '心血管内科': [{'name': '赵伟', 'title': '主任医师'}, {'name': '孙丽', 'title': '主治医师'}],
        '内分泌科': [{'name': '周明', 'title': '主任医师'}, {'name': '吴静', 'title': '副主任医师'}],
        '神经内科': [{'name': '郑刚', 'title': '副主任医师'}, {'name': '黄磊', 'title': '主治医师'}],
        '骨科': [{'name': '马超', 'title': '主任医师'}, {'name': '林峰', 'title': '副主任医师'}],
        '耳鼻喉科': [{'name': '何平', 'title': '副主任医师'}, {'name': '徐明', 'title': '主治医师'}],
        '眼科': [{'name': '罗敏', 'title': '主任医师'}, {'name': '谢涛', 'title': '副主任医师'}],
        '皮肤科': [{'name': '韩冰', 'title': '副主任医师'}, {'name': '唐晓', 'title': '主治医师'}],
        '泌尿外科': [{'name': '冯强', 'title': '主任医师'}, {'name': '董明', 'title': '副主任医师'}],
        '风湿免疫科': [{'name': '曹阳', 'title': '副主任医师'}, {'name': '彭静', 'title': '主治医师'}],
        '血液科': [{'name': '蒋涛', 'title': '主任医师'}, {'name': '沈磊', 'title': '副主任医师'}],
    }
}

def analyze_symptoms(selected_symptoms):
    """
    症状推理引擎
    根据患者选择的症状，返回匹配度最高的诊断建议列表
    """
    if not selected_symptoms:
        return []

    results = []
    for disease_name, info in KNOWLEDGE_BASE.items():
        matched = [s for s in selected_symptoms if s in info["symptoms"]]
        match_count = len(matched)

        if match_count >= info["min_match"]:
            # 计算匹配置信度
            confidence = min(
                round((match_count / len(info["symptoms"])) * info["weight"] * 100, 1),
                99.0
            )
            results.append({
                "disease": disease_name,
                "confidence": confidence,
                "category": info["category"],
                "matched_symptoms": matched,
                "icd10": info["icd10"],
                "examinations": info["examinations"],
                "medications": info["medications"]
            })

    # 按置信度降序排列
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results[:5]  # 返回前5个最可能的诊断
