import os
import mysql.connector

# 取得 MySQL 資料庫連線
# 連線參數皆從環境變數取得，方便 Docker 部署
def get_db_conn():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'petshop'),
        password=os.environ.get('MYSQL_PASSWORD', 'petshoppw'),
        database=os.environ.get('MYSQL_DATABASE', 'petshop'),
        charset='utf8mb4'
    )
