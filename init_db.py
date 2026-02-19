#!/usr/bin/env python3
"""
数据库初始化脚本
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@localhost/competition_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 导入模型
from models import Application, ApplicationParticipant, CertificateTemplate, ImportLog
from config import COMPETITION_RULES

def init_database():
    """初始化数据库"""
    print("正在初始化数据库...")
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✓ 数据库表创建成功")
        
        # 创建默认证书模板
        create_default_templates()
        print("✓ 默认证书模板创建成功")
        
        print("数据库初始化完成！")

def create_default_templates():
    """创建默认证书模板"""
    generator = CertificateGenerator()
    
    for category, tasks in COMPETITION_RULES.items():
        for task, rule in tasks.items():
            for award_level in ['一等奖', '二等奖', '三等奖', '优秀奖']:
                # 检查是否已存在
                existing = CertificateTemplate.query.filter(
                    CertificateTemplate.category == category,
                    CertificateTemplate.award_level == award_level
                ).first()
                
                if not existing:
                    template = CertificateTemplate(
                        name=f"{category}-{award_level}模板",
                        category=category,
                        award_level=award_level
                    )
                    template.set_config(generator.create_default_template(category, award_level))
                    db.session.add(template)
    
    db.session.commit()

class CertificateGenerator:
    """证书生成器（简化版）"""
    
    def create_default_template(self, category, award_level):
        """创建默认模板配置"""
        return {
            "background_color": None,
            "text_color": "#000000",
            "title": {
                "text": "获奖证书",
                "x": 50,
                "y": 200,
                "width": 100,
                "max_font_size": 32,
                "min_font_size": 16
            },
            "name": {
                "x": 50,
                "y": 160,
                "width": 100,
                "max_font_size": 24,
                "min_font_size": 12
            },
            "school": {
                "x": 50,
                "y": 130,
                "width": 100,
                "max_font_size": 20,
                "min_font_size": 10
            },
            "project": {
                "x": 50,
                "y": 100,
                "width": 100,
                "max_font_size": 18,
                "min_font_size": 10
            },
            "award": {
                "x": 50,
                "y": 70,
                "width": 100,
                "max_font_size": 22,
                "min_font_size": 12
            },
            "date": {
                "x": 50,
                "y": 40,
                "width": 100,
                "max_font_size": 14,
                "min_font_size": 8
            },
            "match_no": {
                "x": 140,
                "y": 40,
                "width": 40,
                "max_font_size": 12,
                "min_font_size": 8
            }
        }

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit(1)
