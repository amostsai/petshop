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
│   ├── app.py            # Flask application factory + feature 註冊
│   ├── config.py         # 分環境設定與秘密讀取邏輯
│   ├── features/         # 依網站功能分組的模組
│   │   ├── main/         # 首頁
│   │   ├── news/         # 最新消息
│   │   ├── contact/      # 聯絡我們
│   │   ├── services/     # 服務介紹
│   │   └── about/        # 關於我們
│   ├── lib/              # 共用工具（資料庫、快取、錯誤類別等）
│   ├── static/           # 靜態檔案（CSS, JS, 圖片）
│   └── templates/        # 共用模板（如 base.html）
├── env/
│   ├── flask/            # Dockerfile
│   ├── mysql/            # 資料庫初始化 SQL
│   └── nginx/            # Nginx 設定
├── docker-compose.yml    # 一鍵啟動所有服務
└── README.md             # 專案說明
```

- 每個 feature 資料夾集中該功能所需的 Blueprint (`__init__.py`)、路由 (`routes.py`)、服務與資料存取層（視需求提供 `service.py`、`repository.py`）、以及對應模板 (`templates/`)。

---

## 學習重點

- **Blueprint 分層**：如何將不同功能模組化，方便維護與擴充。
- **資料庫連線**：如何用 Python 連接 MySQL，並安全寫入資料。
- **表單處理**：前端驗證 + 後端驗證 + 資料寫入 DB。
- **靜態檔案與模板**：Nginx 如何直接服務 /static，Flask 如何渲染 Jinja2 模板。
- **Docker volume**：程式碼即時同步到 container，開發方便。
- **一鍵啟動**：用 docker compose up 即可啟動所有服務。

---

## 商品販售體驗

- `/products` 顯示商品分類、列表與詳細頁，可將有庫存的商品加入購物車。
- 購物車支援調整數量、移除商品與查看訂單摘要，並在導覽列顯示件數徽章。
- 結帳流程會寫入訂單與明細至 MySQL，並在成功後顯示訂單編號供後續追蹤。

---

## 進階練習建議

- 嘗試新增一個「留言板」功能，練習 blueprint、資料庫設計、模板渲染。
- 修改 Nginx 設定，體驗靜態檔案快取。
