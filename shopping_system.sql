CREATE DATABASE shopping_system;
USE shopping_system;

-- SELLERS
CREATE TABLE sellers(
shopid VARCHAR(20) PRIMARY KEY,
shopname VARCHAR(100),
password VARCHAR(100)
);

-- BUYERS
CREATE TABLE buyers(
buyerid VARCHAR(20) PRIMARY KEY,
uname VARCHAR(100),
address VARCHAR(200),
password VARCHAR(100)
);

-- PRODUCTS
CREATE TABLE products(
product_id VARCHAR(20) PRIMARY KEY,
product_name VARCHAR(100),
category VARCHAR(50),
subcategory1 VARCHAR(20),
subcategory2 VARCHAR(20),
total_quantity INT,
current_quantity INT,
price DECIMAL(10,2),
shopid VARCHAR(20)
);

-- ORDERS
CREATE TABLE orders(
order_id INT AUTO_INCREMENT PRIMARY KEY,
buyerid VARCHAR(20),
product_id VARCHAR(20),
quantity INT,
total_price DECIMAL(10,2),
order_date DATE DEFAULT (CURRENT_DATE)
);

-- SELLER HISTORY
CREATE TABLE seller_history(
id INT AUTO_INCREMENT PRIMARY KEY,
shopid VARCHAR(20),
product_id VARCHAR(20),
quantity INT,
total_amount DECIMAL(10,2),
date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

show tables;

select * from buyers;

SELECT * FROM sellers;

SELECT * FROM products;

SELECT * FROM orders;

SELECT * FROM seller_history;

