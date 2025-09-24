# 毛孩樂園寵物店範例網站

本專案是一個以 Flask + MySQL + Nginx + Docker Compose 打造的寵物店網站範例，適合學習網站全端開發與容器化部署。

---

## 注意事項

本網站圖片都是從網路上隨機取得，教學使用
根據本範例修改爲其他商業網站，請記得更換圖片！

---

## 專案技術架構

```
[使用者瀏覽器]
        │
        ▼
    [Nginx]  ← 靜態檔案（圖片、CSS、JS）
        │
        ▼
    [Flask (app.py)]
        │
        ▼
    [MySQL 資料庫]
```

- **Nginx**：反向代理，負責接收外部請求，將 API 請求轉發給 Flask，並直接提供靜態檔案（/static）。
- **Flask**：Python Web 框架，負責處理動態頁面、路由、表單、資料庫互動。
- **MySQL**：關聯式資料庫，儲存網站資料（最新消息、服務、聯絡表單等）。
- **Docker Compose**：一鍵啟動所有服務，並用 volume 掛載本機程式碼，方便開發與同步。

---

## 下載與執行步驟

1. **下載專案**
   ```bash
   git clone git@github.com:amostsai/petshop.git
   cd petshop
   ```

2. **準備 Docker Secrets**
   - 編輯 `secrets/` 目錄內的三個檔案：
     - `mysql_root_password.txt`
     - `mysql_user_password.txt`
     - `flask_secret_key.txt`
   - 將內容改成自己的安全密碼／金鑰。範例值僅供教學使用。

3. **啟動服務**
   ```bash
   docker compose up
   ```
   - 第一次啟動會自動建立資料庫與 seed 假資料。
   - 預設網站入口：http://localhost

4. **關閉服務**
   ```bash
   docker compose down
   ```
5. **若修改靜態檔案(html, css, js, jpg, png, gif等檔案)**
   ```bash
   docker compose down
   docker compose up
   ```

---

## 目錄結構說明

```
petshop/
├── app/                  # Flask 主程式
│   ├── __init__.py       # 匯出 create_app 供 flask run 使用
│   ├── app.py            # Flask application factory + blueprint 註冊
│   ├── config.py         # 分環境設定與秘密讀取邏輯
│   ├── blueprints/       # 各功能 blueprint（main, news, services, about）
│   ├── lib/              # 共用工具（資料庫、快取、錯誤類別）
│   ├── repositories/     # SQL 存取層，封裝資料庫操作
│   ├── services/         # 業務邏輯層，提供快取與錯誤處理
│   ├── static/           # 靜態檔案（CSS, JS, 圖片）
│   └── templates/        # Jinja2 HTML 模板
├── env/
│   ├── flask/            # Dockerfile
│   ├── mysql/            # 資料庫初始化 SQL
│   └── nginx/            # Nginx 設定
├── docker-compose.yml    # 一鍵啟動所有服務
└── README.md             # 專案說明
```

---

## 學習重點

- **Blueprint 分層**：如何將不同功能模組化，方便維護與擴充。
- **資料庫連線**：如何用 Python 連接 MySQL，並安全寫入資料。
- **表單處理**：前端驗證 + 後端驗證 + 資料寫入 DB。
- **靜態檔案與模板**：Nginx 如何直接服務 /static，Flask 如何渲染 Jinja2 模板。
- **Docker volume**：程式碼即時同步到 container，開發方便。
- **一鍵啟動**：用 docker compose up 即可啟動所有服務。

---

## 進階練習建議

- 嘗試新增一個「留言板」功能，練習 blueprint、資料庫設計、模板渲染。
- 修改 Nginx 設定，體驗靜態檔案快取。
