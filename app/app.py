import os
from flask import Flask
# 匯入各功能 blueprint
from blueprints.main import main_bp
from blueprints.news import news_bp
from blueprints.services import services_bp
from blueprints.about import about_bp

# 建立 Flask 應用實例
app = Flask(__name__)

# 設定 session 加密金鑰（flash、登入等功能需用）
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

# 設定 MySQL 連線參數（從 docker-compose.yml 的環境變數取得）
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'petshop')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'petshoppw')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE', 'petshop')
app.config['MYSQL_CHARSET'] = 'utf8mb4'

# 註冊 blueprint，將各功能模組化
app.register_blueprint(main_bp)  # 首頁、聯絡表單
app.register_blueprint(news_bp, url_prefix='/news')  # 最新消息
app.register_blueprint(services_bp, url_prefix='/services')  # 服務介紹
app.register_blueprint(about_bp, url_prefix='/about')  # 關於我們
