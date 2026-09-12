# Smart Clinic - 智能门诊医生工作站

门诊管理系统原型，医生端和患者端分离，包含挂号、候诊、AI 辅助诊断、开方等完整流程。

## 功能

### 医生端
- 挂号分诊：选择医院、科室、医生
- 候诊队列：门诊首页显示当前候诊患者
- AI 辅助诊断：基于症状知识库提供诊断建议
- 检查项目：血常规、CT、MRI 等检查
- 过敏校验：开方时检测患者过敏史
- 药品目录：处方药品自动补全
- 就诊历史：查看患者历次就诊记录
- ICD-10 编码：诊断关联国际疾病分类
- 处方打印

### 患者端
- 自助挂号：手机端选医院 → 选科室 → 填信息
- 就诊记录：手机号查询个人就诊历史
- 就诊指南：就诊流程说明
- 医院信息：科室和医生列表

## 技术栈

- 后端：Python Flask
- 数据库：SQLite + Flask-SQLAlchemy
- 前端：Bootstrap 5
- 模板：Jinja2

## 快速开始

`ash
git clone https://github.com/Yuanleee-walker/smart-clinic.git
cd smart-clinic
pip install -r requirements.txt
python app.py
`

首次启动自动创建数据库和演示数据。

## 访问

- 医生端：http://127.0.0.1:5000/login（账号：admin / admin123）
- 患者端：http://127.0.0.1:5000/patient（无需登录）

## 项目结构

`
smart-clinic/
├── app.py
├── models.py
├── knowledge_base.py
├── requirements.txt
├── start.bat
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── patients.html
│   ├── patient_history.html
│   ├── visits.html
│   ├── new_visit.html
│   ├── visit_detail.html
│   ├── print_prescription.html
│   ├── register.html
│   ├── patient_index.html
│   ├── patient_my_visits.html
│   ├── patient_guide.html
│   └── patient_hospital.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── instance/
    └── clinic.db
`

## 数据模型

- Patient：患者信息（姓名、性别、年龄、电话、过敏史）
- Visit：就诊记录（科室、医生、主诉、症状、诊断、检查、状态）
- Prescription：处方（药品、剂量、用法、数量）

## 演示数据

内置"东方仁济医院"：
- 13 个科室
- 27 位医生
- 8 位演示患者

## 相关项目

[Smart Health Monitor](https://github.com/Yuanleee-walker/smart-health-monitor) - 公共卫生监测大屏

## License

MIT
