"""
数据库模型定义
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Patient(db.Model):
    """患者信息表"""
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20))
    id_card = db.Column(db.String(20))
    allergy_history = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关联
    visits = db.relationship('Visit', backref='patient', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'phone': self.phone,
            'id_card': self.id_card,
            'allergy_history': self.allergy_history,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'visit_count': len(self.visits)
        }


class Visit(db.Model):
    """门诊就诊记录表"""
    __tablename__ = 'visits'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    visit_date = db.Column(db.DateTime, default=datetime.now)
    department = db.Column(db.String(50), default='全科')
    doctor_name = db.Column(db.String(50), default='')

    # 病历信息
    chief_complaint = db.Column(db.Text, default='')        # 主诉
    present_illness = db.Column(db.Text, default='')         # 现病史
    past_history = db.Column(db.Text, default='')            # 既往史
    physical_exam = db.Column(db.Text, default='')           # 体格检查
    symptoms = db.Column(db.Text, default='')                # 症状（JSON字符串）
    diagnosis = db.Column(db.String(200), default='')        # 诊断
    diagnosis_icd10 = db.Column(db.String(20), default='')   # ICD-10编码
    examinations = db.Column(db.Text, default='')               # 检查项目（JSON字符串）

    # 处方信息
    prescriptions = db.relationship('Prescription', backref='visit', lazy=True)

    status = db.Column(db.String(20), default='就诊中')      # 就诊中/已完成

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else '',
            'visit_date': self.visit_date.strftime('%Y-%m-%d %H:%M'),
            'department': self.department,
            'doctor_name': self.doctor_name,
            'chief_complaint': self.chief_complaint,
            'present_illness': self.present_illness,
            'past_history': self.past_history,
            'physical_exam': self.physical_exam,
            'symptoms': self.symptoms,
            'diagnosis': self.diagnosis,
            'diagnosis_icd10': self.diagnosis_icd10,
            'examinations': self.examinations,
            'status': self.status,
            'prescriptions': [p.to_dict() for p in self.prescriptions]
        }


class Prescription(db.Model):
    """处方表"""
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey('visits.id'), nullable=False)
    drug_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), default='')            # 剂量
    frequency = db.Column(db.String(50), default='')         # 用法
    quantity = db.Column(db.String(50), default='')          # 数量
    remarks = db.Column(db.String(200), default='')          # 备注

    def to_dict(self):
        return {
            'id': self.id,
            'drug_name': self.drug_name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'quantity': self.quantity,
            'remarks': self.remarks
        }
