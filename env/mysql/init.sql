SET NAMES utf8mb4;
-- 建立資料表
CREATE DATABASE IF NOT EXISTS petshop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE petshop;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product_images;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS product_categories;
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

DROP TABLE IF EXISTS product_categories;
CREATE TABLE product_categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) NOT NULL UNIQUE,
  description TEXT
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  category_id INT NOT NULL,
  name VARCHAR(120) NOT NULL,
  slug VARCHAR(140) NOT NULL UNIQUE,
  description TEXT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  is_published TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES product_categories(id)
);

DROP TABLE IF EXISTS product_images;
CREATE TABLE product_images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  image_url VARCHAR(255) NOT NULL,
  is_primary TINYINT(1) NOT NULL DEFAULT 0,
  sort_order INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_product_images_product FOREIGN KEY (product_id) REFERENCES products(id)
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_number VARCHAR(20) NOT NULL UNIQUE,
  customer_name VARCHAR(100) NOT NULL,
  customer_email VARCHAR(150) NOT NULL,
  customer_phone VARCHAR(20) NOT NULL,
  fulfillment_method ENUM('pickup','delivery') NOT NULL,
  notes TEXT,
  total_amount DECIMAL(10,2) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  product_name VARCHAR(120) NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  quantity INT NOT NULL,
  line_total DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders(id),
  CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES products(id)
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

-- 新增商品分類 seed
INSERT INTO product_categories (name, slug, description) VALUES
('寵物主食', 'pet-food', '熱銷主食罐、乾糧，均衡營養好安心'),
('玩具配件', 'toys-accessories', '互動玩具與外出配件，滿足毛孩玩樂需求'),
('美容清潔', 'grooming', '洗澡、美容、清潔用品，維持最佳狀態'),
('保健保養', 'health-care', '營養補充與保健品，強化免疫與活力');

-- 新增商品資料 seed
INSERT INTO products (category_id, name, slug, description, price, stock, is_published) VALUES
((SELECT id FROM product_categories WHERE slug = 'pet-food'), '有機鮮肉主食餐 (狗)', 'organic-dog-meal', '採用人食等級鮮肉與蔬菜製成，適合所有成犬日常主食。', 420.00, 25, 1),
((SELECT id FROM product_categories WHERE slug = 'toys-accessories'), '逗貓智能球', 'smart-cat-ball', '內建感應模式的逗貓球，可自動感測並變換速度，讓貓咪持續保持興趣。', 680.00, 18, 1),
((SELECT id FROM product_categories WHERE slug = 'grooming'), '植萃舒敏洗毛乳', 'calming-pet-shampoo', '低敏植萃配方，溫和清潔並補水保濕，適合敏感肌膚犬貓。', 550.00, 30, 1),
((SELECT id FROM product_categories WHERE slug = 'health-care'), '關節保健軟骨素', 'joint-care-supplement', '嚴選葡萄糖胺與軟骨素成分，支撐老年毛孩關節活動力。', 750.00, 12, 1);

-- 新增商品圖片 seed
INSERT INTO product_images (product_id, image_url, is_primary, sort_order) VALUES
((SELECT id FROM products WHERE slug = 'organic-dog-meal'), '/static/images/dog1.png', 1, 1),
((SELECT id FROM products WHERE slug = 'smart-cat-ball'), '/static/images/dog1.png', 1, 1),
((SELECT id FROM products WHERE slug = 'calming-pet-shampoo'), '/static/images/dog1.png', 1, 1),
((SELECT id FROM products WHERE slug = 'joint-care-supplement'), '/static/images/dog1.png', 1, 1);
