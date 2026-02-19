# 快速开始指南

## 1. 环境准备

### 安装Python依赖
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 配置MySQL数据库
```sql
-- 创建数据库
CREATE DATABASE competition_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（可选）
CREATE USER 'competition'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON competition_db.* TO 'competition'@'localhost';
FLUSH PRIVILEGES;
```

### 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件
DATABASE_URL=mysql+pymysql://username:password@localhost/competition_db
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
```

## 2. 初始化数据库

```bash
# 运行初始化脚本
python init_db.py
```

## 3. 启动后端服务

```bash
# 启动Flask应用
python app.py
```

服务将在 `http://localhost:5000` 启动

## 4. 测试API

```bash
# 运行API测试
python test_api.py
```

## 5. 前端开发

### 使用HBuilderX
1. 打开HBuilderX
2. 文件 → 打开目录 → 选择 `frontend` 文件夹
3. 运行 → 运行到浏览器 → Chrome
4. 或运行 → 运行到小程序模拟器

### 使用CLI
```bash
cd frontend
npm install
npm run dev:h5        # H5开发
npm run dev:mp-weixin # 微信小程序
```

## 6. 常见问题

### 数据库连接失败
- 检查MySQL服务是否启动
- 确认数据库连接信息正确
- 检查防火墙设置

### 前端无法访问后端
- 确认后端服务正在运行
- 检查CORS设置（如需要）
- 确认API地址配置正确

### 证书生成失败
- 确认中文字体文件存在
- 检查reportlab库是否正确安装
- 确认模板配置格式正确

## 7. 开发建议

### 后端开发
- 使用 `flask shell` 进行调试
- 查看 `logs/` 目录下的日志文件
- 使用 `python -m pytest` 运行测试

### 前端开发
- 使用浏览器开发者工具调试
- 查看网络请求确认API调用
- 使用真机调试测试小程序

## 8. 部署

### 开发环境
直接运行 `python app.py`

### 生产环境
```bash
# 使用Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 使用Docker
docker build -t competition-system .
docker run -p 5000:5000 competition-system
```

## 9. API文档

主要接口：
- `GET /api/competition-rules` - 获取竞赛规则
- `POST /api/register` - 提交报名
- `GET /api/my-applications` - 查询我的报名
- `POST /api/admin/import-match-no` - 导入参赛号
- `POST /api/admin/import-awards` - 导入获奖信息
- `GET /api/certificate/generate/{id}` - 生成证书

详细文档请参考 `README.md`
