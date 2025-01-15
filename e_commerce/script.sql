-- Insert Categories
INSERT INTO categories_category (name, slug, image, active, timestamp) 
VALUES ('Calçados', 'calcados', 'categories/calcados.jpg', 1, NOW());
INSERT INTO categories_category (name, slug, image, active, timestamp) 
VALUES ('Roupas', 'roupas', 'categories/roupas.jpg', 1, NOW());
INSERT INTO categories_category (name, slug, image, active, timestamp) 
VALUES ('Acessórios', 'acessorios', 'categories/acessorios.jpg', 1, NOW());
INSERT INTO categories_category (name, slug, image, active, timestamp) 
VALUES ('Eletrônicos', 'eletronicos', 'categories/eletronicos.jpg', 1, NOW());
INSERT INTO categories_category (name, slug, image, active, timestamp) 
VALUES ('Móveis', 'moveis', 'categories/moveis.jpg', 1, NOW());
INSERT INTO categories_category (name, slug, image, active, timestamp) 
VALUES ('Decoração', 'decoracao', 'categories/decoracao.jpg', 1, NOW());

-- Insert Products
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Tênis Esportivo', 'tenis-esportivo', 299.90, 50, (SELECT id FROM categories_category WHERE slug = 'calcados'), 'products/tenis-esportivo.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Camiseta Casual', 'camiseta-casual', 89.90, 100, (SELECT id FROM categories_category WHERE slug = 'roupas'), 'products/camiseta-casual.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Jaqueta de Couro', 'jaqueta-de-couro', 599.90, 30, (SELECT id FROM categories_category WHERE slug = 'roupas'), 'products/jaqueta-de-couro.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Relógio Clássico', 'relogio-classico', 199.90, 40, (SELECT id FROM categories_category WHERE slug = 'acessorios'), 'products/relogio-classico.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Bolsa de Couro', 'bolsa-de-couro', 399.90, 25, (SELECT id FROM categories_category WHERE slug = 'acessorios'), 'products/bolsa-de-couro.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Óculos de Sol', 'oculos-de-sol', 159.90, 60, (SELECT id FROM categories_category WHERE slug = 'acessorios'), 'products/oculos-de-sol.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Notebook Gamer', 'notebook-gamer', 5999.90, 10, (SELECT id FROM categories_category WHERE slug = 'eletronicos'), 'products/notebook-gamer.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Smartphone Android', 'smartphone-android', 1999.90, 15, (SELECT id FROM categories_category WHERE slug = 'eletronicos'), 'products/smartphone-android.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Fone de Ouvido Bluetooth', 'fone-de-ouvido-bluetooth', 299.90, 75, (SELECT id FROM categories_category WHERE slug = 'eletronicos'), 'products/fone-de-ouvido-bluetooth.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Smartwatch Fitness', 'smartwatch-fitness', 499.90, 35, (SELECT id FROM categories_category WHERE slug = 'eletronicos'), 'products/smartwatch-fitness.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Mesa de Escritório', 'mesa-de-escritorio', 799.90, 20, (SELECT id FROM categories_category WHERE slug = 'moveis'), 'products/mesa-de-escritorio.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Cadeira Gamer', 'cadeira-gamer', 999.90, 15, (SELECT id FROM categories_category WHERE slug = 'moveis'), 'products/cadeira-gamer.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Abajur Moderno', 'abajur-moderno', 149.90, 40, (SELECT id FROM categories_category WHERE slug = 'decoracao'), 'products/abajur-moderno.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Quadro Abstrato', 'quadro-abstrato', 259.90, 25, (SELECT id FROM categories_category WHERE slug = 'decoracao'), 'products/quadro-abstrato.jpg', 1, 0, NOW());
INSERT INTO products_product (title, slug, price, stock, category_id, image, active, featured, timestamp) 
VALUES ('Tênis de Corrida', 'tenis-de-corrida', 349.90, 45, (SELECT id FROM categories_category WHERE slug = 'calcados'), 'products/tenis-de-corrida.jpg', 1, 0, NOW());
