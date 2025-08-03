SET NAMES utf8mb4;
-- 建立資料表
CREATE DATABASE IF NOT EXISTS petshop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE petshop;

DROP TABLE IF EXISTS news;
CREATE TABLE news (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME NOT NULL
);

DROP TABLE IF EXISTS services;
CREATE TABLE services (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  description TEXT NOT NULL,
  image_url VARCHAR(255)
);

DROP TABLE IF EXISTS about;
CREATE TABLE about (
  id INT AUTO_INCREMENT PRIMARY KEY,
  content TEXT NOT NULL,
  image_url VARCHAR(255)
);

DROP TABLE IF EXISTS contact;
CREATE TABLE contact (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  message TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 新增最新消息 seed
INSERT INTO news (title, content, created_at) VALUES
('夏日寵物健檢優惠', '即日起至8月底，帶您的毛孩來店享受健檢8折優惠！', '2025-07-01 10:00:00'),
('寵物美容新服務上線', '全新SPA寵物美容，給毛孩最頂級的呵護，歡迎預約！', '2025-07-15 09:00:00'),
('中秋連假營業公告', '中秋連假期間正常營業，歡迎來店！', '2025-07-25 12:00:00');

-- 新增服務介紹 seed
INSERT INTO services (name, description, image_url) VALUES
('寵物美容', '專業美容師團隊，提供洗澡、剪毛、SPA等多元服務。', '/static/images/services/grooming.png'),
('寵物寄宿', '舒適安全的寄宿空間，24小時照護，讓您安心出遊。', '/static/images/services/boarding.png'),
('寵物醫療', '合作獸醫師定期駐診，健康諮詢與基礎醫療服務。', '/static/images/services/medical.png'),
('寵物商品', '嚴選飼料、玩具、保健品，滿足毛孩日常所需。', '/static/images/services/products.png');

-- 新增關於我們 seed
INSERT INTO about (content, image_url) VALUES
('我們是一群熱愛動物的專業團隊，致力於提供最優質的寵物照護與服務。', '/static/images/about/team.webp');
