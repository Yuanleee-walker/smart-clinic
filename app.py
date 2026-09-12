import json
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from models import db, Patient, Visit, Prescription
from knowledge_base import analyze_symptoms, ALL_SYMPTOMS, ALL_DEPARTMENTS, KNOWLEDGE_BASE, ALL_MEDICATIONS, ALL_EXAMINATIONS, ALLERGY_DRUG_MAP, DEMO_HOSPITAL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'smart-clinic-dev-key-2026'
db.init_app(app)

USERS = {'admin': 'admin123', 'doctor': 'doctor123'}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('visit_list'))
        return render_template('login.html', error='用户名或密码错误')
    if 'user' in session:
        return redirect(url_for('visit_list'))
    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return redirect(url_for('visit_list'))


@app.route('/patients')
@login_required
def patients():
    search = request.args.get('search', '').strip()
    if search:
        query = Patient.query.filter(db.or_(Patient.name.contains(search), Patient.phone.contains(search), Patient.id_card.contains(search)))
    else:
        query = Patient.query
    patient_list = query.order_by(Patient.created_at.desc()).all()
    return render_template('patients.html', patients=patient_list, search=search)

@app.route('/visit')
@login_required
def visit_list():
    from datetime import datetime
    status = request.args.get('status', 'all')
    query = Visit.query
    if status != 'all':
        query = query.filter_by(status=status)
    visits = query.order_by(Visit.visit_date.desc()).all()
    
    # 计算今日候诊队列
    today = datetime.now().date()
    waiting = Visit.query.filter_by(status='就诊中').filter(Visit.visit_date >= today).order_by(Visit.visit_date.asc()).all()
    waiting_list = []
    for v in waiting:
        wait_minutes = int((datetime.now() - v.visit_date).total_seconds() / 60)
        waiting_list.append({
            'id': v.id,
            'patient_name': v.patient.name,
            'department': v.department,
            'doctor_name': v.doctor_name,
            'wait_time': wait_minutes
        })
    
    return render_template('visits.html', visits=visits, current_status=status, waiting_list=waiting_list)


@app.route('/visit/new', methods=['GET', 'POST'])
@login_required
def new_visit():
    if request.method == 'POST':
        data = request.form
        visit_id = data.get('visit_id', '').strip()
        patient_id = data.get('patient_id')
        if patient_id:
            patient = Patient.query.get(int(patient_id))
        else:
            patient = Patient(name=data['patient_name'], gender=data['gender'], age=int(data['age']), phone=data.get('phone', ''), id_card=data.get('id_card', ''))
            db.session.add(patient)
            db.session.flush()
        
        if visit_id:
            visit = Visit.query.get(int(visit_id))
            visit.chief_complaint = data.get('chief_complaint', '')
            visit.present_illness = data.get('present_illness', '')
            visit.past_history = data.get('past_history', '')
            visit.physical_exam = data.get('physical_exam', '')
            visit.symptoms = data.get('symptoms_json', '[]')
            visit.diagnosis = data.get('diagnosis', '')
            visit.diagnosis_icd10 = data.get('diagnosis_icd10', '')
            visit.examinations = data.get('examinations_json', '[]')
            Prescription.query.filter_by(visit_id=visit.id).delete()
        else:
            visit = Visit(patient_id=patient.id, department=data.get('department', '全科'), chief_complaint=data.get('chief_complaint', ''), present_illness=data.get('present_illness', ''), past_history=data.get('past_history', ''), physical_exam=data.get('physical_exam', ''), symptoms=data.get('symptoms_json', '[]'), diagnosis=data.get('diagnosis', ''), diagnosis_icd10=data.get('diagnosis_icd10', ''), examinations=data.get('examinations_json', '[]'), status='就诊中')
            db.session.add(visit)
            db.session.flush()
        
        drug_names = request.form.getlist('drug_name[]')
        dosages = request.form.getlist('dosage[]')
        frequencies = request.form.getlist('frequency[]')
        quantities = request.form.getlist('quantity[]')
        remarks_list = request.form.getlist('remarks[]')
        for i in range(len(drug_names)):
            if drug_names[i].strip():
                rx = Prescription(visit_id=visit.id, drug_name=drug_names[i].strip(), dosage=dosages[i] if i < len(dosages) else '', frequency=frequencies[i] if i < len(frequencies) else '', quantity=quantities[i] if i < len(quantities) else '', remarks=remarks_list[i] if i < len(remarks_list) else '')
                db.session.add(rx)
        db.session.commit()
        return jsonify({'success': True, 'visit_id': visit.id})
    
    # GET
    patient_list = Patient.query.order_by(Patient.created_at.desc()).all()
    visit_id = request.args.get('visit_id', '')
    existing_visit = None
    if visit_id:
        existing_visit = Visit.query.get(int(visit_id))
    return render_template('new_visit.html', patients=patient_list, all_symptoms=ALL_SYMPTOMS, all_departments=ALL_DEPARTMENTS, all_medications=ALL_MEDICATIONS, all_examinations=ALL_EXAMINATIONS, existing_visit=existing_visit)




@app.route('/visit/<int:visit_id>')
@login_required
def visit_detail(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    symptoms_list = json.loads(visit.symptoms) if visit.symptoms else []
    examinations_list = json.loads(visit.examinations) if visit.examinations else []
    return render_template('visit_detail.html', visit=visit, symptoms_list=symptoms_list, examinations_list=examinations_list)
@app.route('/visit/<int:visit_id>/finish', methods=['POST'])
@login_required
def finish_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    visit.status = '已完成'
    db.session.commit()
    return jsonify({'success': True})

@app.route('/visit/<int:visit_id>/delete', methods=['POST'])
@login_required
def delete_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    Prescription.query.filter_by(visit_id=visit.id).delete()
    db.session.delete(visit)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/visit/<int:visit_id>/print')
@login_required
def print_prescription(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    return render_template('print_prescription.html', visit=visit)

@app.route('/api/ai-diagnosis', methods=['POST'])
@login_required
def ai_diagnosis():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    results = analyze_symptoms(symptoms)
    return jsonify({'results': results})

@app.route('/patient/<int:patient_id>/history')
@login_required
def patient_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    visits = Visit.query.filter_by(patient_id=patient_id).order_by(Visit.visit_date.desc()).all()
    return render_template('patient_history.html', patient=patient, visits=visits)

@app.route('/api/allergy-check', methods=['POST'])
@login_required
def allergy_check():
    data = request.get_json()
    patient_id = data.get('patient_id')
    drugs = data.get('drugs', [])
    if not patient_id:
        return jsonify({'warnings': []})
    patient = Patient.query.get(int(patient_id))
    if not patient or not patient.allergy_history:
        return jsonify({'warnings': []})
    warnings = []
    allergy = patient.allergy_history
    for drug in drugs:
        for allergy_key, conflict_drugs in ALLERGY_DRUG_MAP.items():
            if allergy_key in allergy or allergy in allergy_key:
                for conflict_drug in conflict_drugs:
                    if conflict_drug in drug or drug in conflict_drug:
                        warnings.append({'drug': drug, 'allergy': allergy, 'message': f'药品「{drug}」可能与患者过敏史「{allergy}」冲突，请确认是否继续'})
                        break
    return jsonify({'warnings': warnings})
@app.route('/api/patients', methods=['GET'])
@login_required
def api_patients():
    search = request.args.get('q', '')
    if len(search) >= 1:
        patients = Patient.query.filter(Patient.name.contains(search)).limit(10).all()
    else:
        patients = Patient.query.limit(20).all()
    return jsonify([p.to_dict() for p in patients])

@app.route('/api/symptoms')
@login_required
def api_symptoms():
    return jsonify(ALL_SYMPTOMS)

@app.route('/api/drug-suggestions')
@login_required
def drug_suggestions():
    diagnosis = request.args.get('diagnosis', '')
    for disease_name, info in KNOWLEDGE_BASE.items():
        if diagnosis in disease_name or disease_name in diagnosis:
            return jsonify({'medications': info['medications'], 'examinations': info['examinations']})
    return jsonify({'medications': [], 'examinations': []})


# ==================== 患者端路由 ====================

@app.route('/patient')
def patient_index():
    """患者端首页"""
    return render_template('patient_index.html')

@app.route('/patient/my-visits')
def patient_my_visits():
    """患者端 - 我的就诊"""
    return render_template('patient_my_visits.html')

@app.route('/patient/guide')
def patient_guide():
    """患者端 - 就诊指南"""
    return render_template('patient_guide.html')

@app.route('/patient/hospital')
def patient_hospital():
    """患者端 - 医院信息"""
    return render_template('patient_hospital.html')

@app.route('/api/patient/today-stats')
def api_patient_today_stats():
    """患者端 - 今日就诊统计"""
    from datetime import date
    today = date.today()
    today_visits = Visit.query.filter(db.func.date(Visit.visit_date) == today).count()
    waiting = Visit.query.filter_by(status='就诊中').count()
    
    # 计算平均等待时间（简单估算）
    avg_wait = 15  # 默认15分钟
    
    return jsonify({
        'today_visits': today_visits,
        'waiting_count': waiting,
        'avg_wait_minutes': avg_wait
    })

@app.route('/api/patient/visits')
def api_patient_visits():
    """患者端 - 根据手机号查询就诊记录"""
    phone = request.args.get('phone', '').strip()
    if not phone:
        return jsonify([])
    
    patient = Patient.query.filter_by(phone=phone).first()
    if not patient:
        return jsonify([])
    
    visits = Visit.query.filter_by(patient_id=patient.id).order_by(Visit.visit_date.desc()).all()
    return jsonify([v.to_dict() for v in visits])
@app.route('/patient/register', methods=['GET', 'POST'])
def register():
    """患者自助挂号（手机端）"""
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', '').strip()
        gender = data.get('gender', '男')
        age = int(data.get('age', 0))
        phone = data.get('phone', '')
        department = data.get('department', '全科')
        doctor_name = data.get('doctor_name', '')
        
        # 查找或创建患者
        patient = Patient.query.filter_by(phone=phone).first() if phone else None
        if not patient:
            patient = Patient(name=name, gender=gender, age=age, phone=phone)
            db.session.add(patient)
            db.session.flush()
        
        # 创建就诊记录
        visit = Visit(
            patient_id=patient.id,
            department=department,
            doctor_name=doctor_name,
            status='就诊中'
        )
        db.session.add(visit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'visit_id': visit.id,
            'patient_name': patient.name,
            'department': department,
            'doctor_name': doctor_name
        })
    
    return render_template('register.html', hospital=DEMO_HOSPITAL)

@app.route('/api/departments')
def api_departments():
    """获取科室列表"""
    return jsonify(list(DEMO_HOSPITAL['departments'].keys()))

@app.route('/api/doctors/<department>')
def api_doctors(department):
    """获取指定科室的医生列表"""
    doctors = DEMO_HOSPITAL['departments'].get(department, [])
    return jsonify(doctors)
def init_database():
    with app.app_context():
        db.create_all()
        if Patient.query.count() > 0:
            return
        demo_patients = [
            Patient(name='张伟', gender='男', age=45, phone='13800138001', allergy_history='青霉素过敏'),
            Patient(name='李娜', gender='女', age=32, phone='13800138002', allergy_history=''),
            Patient(name='王建国', gender='男', age=68, phone='13800138003', allergy_history='磺胺类药物过敏'),
            Patient(name='赵敏', gender='女', age=28, phone='13800138004', allergy_history=''),
            Patient(name='刘洋', gender='男', age=55, phone='13800138005', allergy_history='海鲜过敏'),
            Patient(name='陈静', gender='女', age=41, phone='13800138006', allergy_history=''),
            Patient(name='杨帆', gender='男', age=23, phone='13800138007', allergy_history=''),
            Patient(name='周雪', gender='女', age=37, phone='13800138008', allergy_history='花粉过敏'),
        ]
        for p in demo_patients:
            db.session.add(p)
        db.session.commit()
        today = datetime.now()
        demo_visits = [
            Visit(patient_id=1, visit_date=today - timedelta(days=5), department='呼吸内科', doctor_name='王志明', chief_complaint='发热咳嗽3天', present_illness='患者3天前无明显诱因出现发热，体温38.5度，伴咳嗽、咳少量白痰', symptoms='["发热","咳嗽","咳痰"]', diagnosis='上呼吸道感染', diagnosis_icd10='J06.9', status='已完成'),
            Visit(patient_id=2, visit_date=today - timedelta(days=4), department='消化内科', doctor_name='张强', chief_complaint='腹痛腹泻1天', present_illness='患者昨日进食不洁食物后出现腹痛、腹泻，大便5次/日', symptoms='["腹痛","腹泻","恶心"]', diagnosis='急性胃肠炎', diagnosis_icd10='A09', status='已完成'),
            Visit(patient_id=3, visit_date=today - timedelta(days=3), department='心血管内科', doctor_name='赵伟', chief_complaint='头晕2周', present_illness='患者近2周反复头晕，测血压偏高，最高160/100mmHg', symptoms='["头晕","头痛","耳鸣"]', diagnosis='高血压', diagnosis_icd10='I10', status='已完成'),
            Visit(patient_id=4, visit_date=today - timedelta(days=2), department='耳鼻喉科', doctor_name='何平', chief_complaint='鼻塞流涕反复发作', present_illness='患者近1月鼻塞、流涕、打喷嚏，接触花粉后加重', symptoms='["鼻塞","流涕","打喷嚏","鼻痒"]', diagnosis='过敏性鼻炎', diagnosis_icd10='J30.4', status='已完成'),
            Visit(patient_id=5, visit_date=today - timedelta(days=1), department='内分泌科', doctor_name='周明', chief_complaint='多饮多尿3月', present_illness='患者近3月出现多饮、多尿，体重下降5kg', symptoms='["多饮","多尿","体重下降","乏力"]', diagnosis='2型糖尿病', diagnosis_icd10='E11', status='已完成'),
            Visit(patient_id=6, visit_date=today - timedelta(hours=3), department='全科', doctor_name='陈建国', chief_complaint='', symptoms='[]', diagnosis='', status='就诊中'),
            Visit(patient_id=7, visit_date=today - timedelta(hours=1), department='全科', doctor_name='陈建国', chief_complaint='', symptoms='[]', diagnosis='', status='就诊中'),
        ]
        for v in demo_visits:
            db.session.add(v)
        db.session.commit()
        demo_prescriptions = [
            Prescription(visit_id=1, drug_name='对乙酰氨基酚片', dosage='0.5g', frequency='每日3次', quantity='9片'),
            Prescription(visit_id=1, drug_name='复方甘草片', dosage='3片', frequency='每日3次', quantity='18片'),
            Prescription(visit_id=2, drug_name='蒙脱石散', dosage='1袋', frequency='每日3次', quantity='6袋'),
            Prescription(visit_id=2, drug_name='口服补液盐', dosage='1袋', frequency='冲服', quantity='6袋'),
            Prescription(visit_id=3, drug_name='氨氯地平片', dosage='5mg', frequency='每日1次', quantity='14片'),
            Prescription(visit_id=4, drug_name='氯雷他定片', dosage='10mg', frequency='每日1次', quantity='7片'),
            Prescription(visit_id=4, drug_name='布地奈德鼻喷剂', dosage='1喷', frequency='每日2次', quantity='1瓶'),
            Prescription(visit_id=5, drug_name='二甲双胍片', dosage='0.5g', frequency='每日2次', quantity='28片'),
        ]
        for rx in demo_prescriptions:
            db.session.add(rx)
        db.session.commit()
        print('Demo data initialized!')

if __name__ == '__main__':
    init_database()
    print('========================================')
    print('  Smart Clinic - 智能门诊医生工作站')
    print('  访问地址: http://127.0.0.1:5000')
    print('  演示账号: admin / admin123')
    print('========================================')
    app.run(debug=True, host='0.0.0.0', port=5000)
