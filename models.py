from datetime import datetime
from app import db

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    # 项目大类
    category = db.Column(db.String(50), nullable=False)  # 如：无人机足球、机器人格斗等
    # 具体任务
    task = db.Column(db.String(100), nullable=False)  # 如：5v5、3v3、个人赛等
    # 学段
    education_level = db.Column(db.String(20), nullable=False)  # 如：小学、中学、大学
    # 人数
    participant_count = db.Column(db.Integer, nullable=False)
    
    # 学校信息
    school_name = db.Column(db.String(100), nullable=False)
    school_region = db.Column(db.String(100))  # 省/自治区/直辖市
    school_city = db.Column(db.String(100))  # 市
    school_district = db.Column(db.String(100))  # 区县

    # 指导老师信息
    teacher_name = db.Column(db.String(50))
    teacher_phone_encrypted = db.Column(db.Text)
    teacher_phone_hash = db.Column(db.String(64), index=True)

    # 领队信息
    leader_name = db.Column(db.String(50))
    leader_phone_encrypted = db.Column(db.Text)

    # 参赛人信息（手机号/邮箱）
    participant_phone_encrypted = db.Column(db.Text)
    participant_email_encrypted = db.Column(db.Text)
    
    # 联系人信息（加密存储）
    contact_name = db.Column(db.String(50), nullable=False)
    contact_phone_encrypted = db.Column(db.Text, nullable=False)
    contact_email_encrypted = db.Column(db.Text, nullable=False)
    
    # 添加哈希字段用于查询
    contact_phone_hash = db.Column(db.String(64), nullable=False, index=True)

    # 报名人 openid（用于学生端权限控制）
    openid = db.Column(db.String(64), index=True)
    
    # 参赛号（管理员导入）
    match_no = db.Column(db.String(50))
    
    # 获奖信息（管理员导入）
    award_level = db.Column(db.String(20))  # 如：一等奖、二等奖等

    # 审核信息（管理员操作）
    rejected_reason = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.String(50))
    
    # 状态和时间
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联的选手
    participants = db.relationship('ApplicationParticipant', backref='application', lazy=True, cascade='all, delete-orphan')
    
    @property
    def contact_phone(self):
        from app import decrypt_data
        return decrypt_data(self.contact_phone_encrypted)
    
    @contact_phone.setter
    def contact_phone(self, value):
        from app import encrypt_data
        import hashlib
        self.contact_phone_encrypted = encrypt_data(value)
        self.contact_phone_hash = hashlib.sha256(value.encode()).hexdigest()
    
    @property
    def contact_email(self):
        from app import decrypt_data
        return decrypt_data(self.contact_email_encrypted)
    
    @contact_email.setter
    def contact_email(self, value):
        from app import encrypt_data
        self.contact_email_encrypted = encrypt_data(value)
    
    @property
    def contact_phone_masked(self):
        from app import mask_phone
        return mask_phone(self.contact_phone)
    
    @property
    def contact_email_masked(self):
        from app import mask_email
        return mask_email(self.contact_email)

    @property
    def teacher_phone(self):
        from app import decrypt_data
        return decrypt_data(self.teacher_phone_encrypted)

    @teacher_phone.setter
    def teacher_phone(self, value):
        from app import encrypt_data
        import hashlib
        self.teacher_phone_encrypted = encrypt_data(value)
        try:
            v = str(value or '').strip()
            self.teacher_phone_hash = hashlib.sha256(v.encode()).hexdigest() if v else None
        except Exception:
            self.teacher_phone_hash = None

    @property
    def leader_phone(self):
        from app import decrypt_data
        return decrypt_data(self.leader_phone_encrypted)

    @leader_phone.setter
    def leader_phone(self, value):
        from app import encrypt_data
        self.leader_phone_encrypted = encrypt_data(value)

    @property
    def participant_phone(self):
        from app import decrypt_data
        return decrypt_data(self.participant_phone_encrypted)

    @participant_phone.setter
    def participant_phone(self, value):
        from app import encrypt_data
        self.participant_phone_encrypted = encrypt_data(value)

    @property
    def participant_email(self):
        from app import decrypt_data
        return decrypt_data(self.participant_email_encrypted)

    @participant_email.setter
    def participant_email(self, value):
        from app import encrypt_data
        self.participant_email_encrypted = encrypt_data(value)

    @property
    def teacher_phone_masked(self):
        from app import mask_phone
        return mask_phone(self.teacher_phone)

    @property
    def leader_phone_masked(self):
        from app import mask_phone
        return mask_phone(self.leader_phone)

    @property
    def participant_phone_masked(self):
        from app import mask_phone
        return mask_phone(self.participant_phone)

    @property
    def participant_email_masked(self):
        from app import mask_email
        return mask_email(self.participant_email)
    
    def to_dict(self, include_sensitive=False):
        result = {
            'id': self.id,
            'openid': self.openid,
            'category': self.category,
            'task': self.task,
            'education_level': self.education_level,
            'participant_count': self.participant_count,
            'school_name': self.school_name,
            'school_region': self.school_region,
            'school_city': self.school_city,
            'school_district': self.school_district,
            'teacher_name': self.teacher_name,
            'leader_name': self.leader_name,
            'contact_name': self.contact_name,
            'match_no': self.match_no,
            'award_level': self.award_level,
            'rejected_reason': self.rejected_reason,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'participants': [p.to_dict() for p in self.participants]
        }
        
        if include_sensitive:
            try:
                result['contact_phone'] = self.contact_phone
                result['contact_email'] = self.contact_email
                result['teacher_phone'] = self.teacher_phone
                result['leader_phone'] = self.leader_phone
                result['participant_phone'] = self.participant_phone
                result['participant_email'] = self.participant_email
            except:
                result['contact_phone'] = '解密失败'
                result['contact_email'] = '解密失败'
                result['teacher_phone'] = '解密失败'
                result['leader_phone'] = '解密失败'
                result['participant_phone'] = '解密失败'
                result['participant_email'] = '解密失败'
        else:
            try:
                result['contact_phone'] = self.contact_phone_masked
                result['contact_email'] = self.contact_email_masked
                result['teacher_phone'] = self.teacher_phone_masked
                result['leader_phone'] = self.leader_phone_masked
                result['participant_phone'] = self.participant_phone_masked
                result['participant_email'] = self.participant_email_masked
            except:
                result['contact_phone'] = '***'
                result['contact_email'] = '***'
                result['teacher_phone'] = '***'
                result['leader_phone'] = '***'
                result['participant_phone'] = '***'
                result['participant_email'] = '***'
            
        return result

class ApplicationParticipant(db.Model):
    __tablename__ = 'application_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    seq_no = db.Column(db.Integer, nullable=False)  # 顺序号，用于区分选手
    participant_name = db.Column(db.String(50), nullable=False)
    
    # 确保同一申请中的序号唯一
    __table_args__ = (db.UniqueConstraint('application_id', 'seq_no'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'seq_no': self.seq_no,
            'participant_name': self.participant_name
        }

class CertificateTemplate(db.Model):
    __tablename__ = 'certificate_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 模板名称
    category = db.Column(db.String(50), nullable=False)  # 适用类别
    award_level = db.Column(db.String(20), nullable=False)  # 获奖等级
    
    # JSON配置，包含各字段的位置和样式
    template_config = db.Column(db.Text, nullable=False)  # JSON格式
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_config(self):
        import json
        return json.loads(self.template_config)
    
    def set_config(self, config_dict):
        import json
        self.template_config = json.dumps(config_dict, ensure_ascii=False)

class ImportLog(db.Model):
    __tablename__ = 'import_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    import_type = db.Column(db.String(20), nullable=False)  # match_no, award
    total_count = db.Column(db.Integer, nullable=False)
    success_count = db.Column(db.Integer, nullable=False)
    failed_count = db.Column(db.Integer, nullable=False)
    
    # 错误日志（Base64编码的Excel内容）
    error_log_content = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'import_type': self.import_type,
            'total_count': self.total_count,
            'success_count': self.success_count,
            'failed_count': self.failed_count,
            'error_log_content': self.error_log_content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ExcellentCoach(db.Model):
    __tablename__ = 'excellent_coaches'

    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(50), nullable=False)
    teacher_phone_encrypted = db.Column(db.Text, nullable=False)
    teacher_phone_hash = db.Column(db.String(64), nullable=False, index=True)

    remark = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def teacher_phone(self):
        from app import decrypt_data
        return decrypt_data(self.teacher_phone_encrypted)

    @teacher_phone.setter
    def teacher_phone(self, value):
        from app import encrypt_data
        import hashlib
        v = str(value or '').strip()
        self.teacher_phone_encrypted = encrypt_data(v)
        self.teacher_phone_hash = hashlib.sha256(v.encode()).hexdigest() if v else ''

    def to_dict(self, include_sensitive=False):
        d = {
            'id': self.id,
            'teacher_name': self.teacher_name,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_sensitive:
            d['teacher_phone'] = self.teacher_phone
        return d
