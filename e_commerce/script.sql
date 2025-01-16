-- Primeiro, limpar dados existentes para evitar conflitos
DELETE FROM carts_cartproduct;
DELETE FROM orders_order;
DELETE FROM carts_cart;
DELETE FROM products_productimage;
DELETE FROM products_product;
DELETE FROM categories_category;
DELETE FROM tags_tag_products;
DELETE FROM tags_tag;
DELETE FROM accounts_user;

-- Inserir categorias
INSERT INTO categories_category (id, name, slug, image, description, active, timestamp) VALUES
(1, 'Calçados', 'calcados', 'categories/calcados.jpg', 'Categoria de calçados', 1, datetime('now')),
(2, 'Roupas', 'roupas', 'categories/roupas.jpg', 'Categoria de roupas', 1, datetime('now')),
(3, 'Acessórios', 'acessorios', 'categories/acessorios.jpg', 'Categoria de acessórios', 1, datetime('now')),
(4, 'Eletrônicos', 'eletronicos', 'categories/eletronicos.jpg', 'Categoria de eletrônicos', 1, datetime('now')),
(5, 'Móveis', 'moveis', 'categories/moveis.jpg', 'Categoria de móveis', 1, datetime('now')),
(6, 'Decoração', 'decoracao', 'categories/decoracao.jpg', 'Categoria de decoração', 1, datetime('now'));

-- Inserir produtos
INSERT INTO products_product (id, title, slug, description, price, discount_price, stock, sku, featured, active, timestamp, updated, category_id) VALUES
(1, 'Tênis Esportivo', 'tenis-esportivo', 'Tênis confortável e durável.', 199.99, 149.99, 50, 'SKU001', 1, 1, datetime('now'), datetime('now'), 1),
(2, 'Camiseta Casual', 'camiseta-casual', 'Camiseta ideal para o dia a dia.', 79.99, 59.99, 100, 'SKU002', 0, 1, datetime('now'), datetime('now'), 2),
(3, 'Jaqueta de Couro', 'jaqueta-de-couro', 'Jaqueta de couro premium.', 499.99, 399.99, 20, 'SKU003', 1, 1, datetime('now'), datetime('now'), 2),
(4, 'Relógio Clássico', 'relogio-classico', 'Relógio elegante.', 899.99, 799.99, 30, 'SKU004', 1, 1, datetime('now'), datetime('now'), 3),
(5, 'Bolsa de Couro', 'bolsa-de-couro', 'Bolsa espaçosa e resistente.', 699.99, 599.99, 25, 'SKU005', 0, 1, datetime('now'), datetime('now'), 3),
(6, 'Smartphone Android', 'smartphone-android', 'Smartphone de alta performance.', 2499.99, 2199.99, 80, 'SKU006', 1, 1, datetime('now'), datetime('now'), 4),
(7, 'Mesa de Escritório', 'mesa-de-escritorio', 'Mesa funcional para escritório.', 399.99, 299.99, 15, 'SKU007', 0, 1, datetime('now'), datetime('now'), 5),
(8, 'Abajur Moderno', 'abajur-moderno', 'Abajur com design moderno.', 149.99, 129.99, 60, 'SKU008', 0, 1, datetime('now'), datetime('now'), 6),
(9, 'Cadeira Gamer', 'cadeira-gamer', 'Cadeira ergonômica para jogos.', 899.99, 799.99, 10, 'SKU009', 0, 1, datetime('now'), datetime('now'), 5),
(10, 'Quadro Abstrato', 'quadro-abstrato', 'Arte moderna para sua parede.', 299.99, 249.99, 30, 'SKU010', 0, 1, datetime('now'), datetime('now'), 6),
(11, 'Fone de Ouvido Bluetooth', 'fone-de-ouvido-bluetooth', 'Som de alta qualidade sem fio.', 399.99, 349.99, 40, 'SKU011', 0, 1, datetime('now'), datetime('now'), 4),
(12, 'Óculos de Sol', 'oculos-de-sol', 'Proteção UV com estilo.', 199.99, 179.99, 45, 'SKU012', 0, 1, datetime('now'), datetime('now'), 3),
(13, 'Smartwatch Fitness', 'smartwatch-fitness', 'Monitore suas atividades.', 599.99, 499.99, 35, 'SKU013', 0, 1, datetime('now'), datetime('now'), 4),
(14, 'Tênis de Corrida', 'tenis-de-corrida', 'Para corridas de alta performance.', 299.99, 259.99, 55, 'SKU014', 0, 1, datetime('now'), datetime('now'), 1);

-- Inserir imagens dos produtos
INSERT INTO products_productimage (id, product_id, image, alt_text, is_featured, "order", timestamp) VALUES
(1, 1, 'products/tenis-esportivo.jpg', 'Tênis esportivo', 1, 0, datetime('now')),
(2, 2, 'products/camiseta-casual.jpg', 'Camiseta casual', 1, 0, datetime('now')),
(3, 3, 'products/jaqueta-de-couro.jpg', 'Jaqueta de couro', 1, 0, datetime('now')),
(4, 4, 'products/relogio-classico.jpg', 'Relógio clássico', 1, 0, datetime('now')),
(5, 5, 'products/bolsa-de-couro.jpg', 'Bolsa de couro', 1, 0, datetime('now')),
(6, 6, 'products/smartphone-android.jpg', 'Smartphone Android', 1, 0, datetime('now')),
(7, 7, 'products/mesa-de-escritorio.jpg', 'Mesa de escritório', 1, 0, datetime('now')),
(8, 8, 'products/abajur-moderno.jpg', 'Abajur moderno', 1, 0, datetime('now')),
(9, 9, 'products/cadeira-gamer.jpg', 'Cadeira gamer', 1, 0, datetime('now')),
(10, 10, 'products/quadro-abstrato.jpg', 'Quadro abstrato', 1, 0, datetime('now')),
(11, 11, 'products/fone-de-ouvido-bluetooth.jpg', 'Fone de ouvido bluetooth', 1, 0, datetime('now')),
(12, 12, 'products/oculos-de-sol.jpg', 'Óculos de sol', 1, 0, datetime('now')),
(13, 13, 'products/smartwatch-fitness.jpg', 'Smartwatch fitness', 1, 0, datetime('now')),
(14, 14, 'products/tenis-de-corrida.jpg', 'Tênis de corrida', 1, 0, datetime('now'));

-- Inserir tags
INSERT INTO tags_tag (title, slug, active, timestamp) VALUES
('Esporte', 'esporte', 1, datetime('now')),
('Casual', 'casual', 1, datetime('now')),
('Elegante', 'elegante', 1, datetime('now')),
('Tecnologia', 'tecnologia', 1, datetime('now')),
('Decoração', 'decoracao', 1, datetime('now')),
('Conforto', 'conforto', 1, datetime('now')),
('Moderno', 'moderno', 1, datetime('now')),
('Premium', 'premium', 1, datetime('now'));

-- Inserir usuários
INSERT INTO accounts_user (full_name, email, password, active, staff, admin, is_verified, timestamp) VALUES
('Admin User', 'admin@example.com', 'pbkdf2_sha256$320000$somehash', 1, 1, 1, 1, datetime('now')),
('Guest User', 'guest@example.com', 'pbkdf2_sha256$320000$somehash', 1, 0, 0, 0, datetime('now')),
('Test User', 'test@example.com', 'pbkdf2_sha256$320000$somehash', 1, 0, 0, 1, datetime('now'));

-- Inserir carrinhos
INSERT INTO carts_cart (id, total, subtotal, timestamp, updated) VALUES
(1, 369.98, 349.98, datetime('now'), datetime('now')),
(2, 199.99, 189.99, datetime('now'), datetime('now')),
(3, 999.98, 949.98, datetime('now'), datetime('now'));

-- Inserir pedidos
INSERT INTO orders_order (id, order_id, status, shipping_total, total, active, billing_profile_id, cart_id, billing_address_id, shipping_address_id) VALUES
(1, 'ORD001', 'completed', 20.00, 369.98, 1, NULL, 1, NULL, NULL),
(2, 'ORD002', 'pending', 10.00, 199.99, 1, NULL, 2, NULL, NULL),
(3, 'ORD003', 'shipped', 50.00, 999.98, 1, NULL, 3, NULL, NULL);

-- Associar produtos aos carrinhos
INSERT INTO carts_cartproduct (id, cart_id, product_id, quantity) VALUES
(1, 1, 1, 2),
(2, 1, 2, 1),
(3, 2, 3, 1),
(4, 3, 4, 1),
(5, 3, 6, 1);

-- Associar tags aos produtos
INSERT INTO tags_tag_products (id, tag_id, product_id) VALUES
(1, 1, 1),  -- Tênis Esportivo - Esporte
(2, 2, 2),  -- Camiseta Casual - Casual
(3, 3, 4),  -- Relógio Clássico - Elegante
(4, 4, 6),  -- Smartphone - Tecnologia
(5, 5, 8),  -- Abajur - Decoração
(6, 6, 9),  -- Cadeira Gamer - Conforto
(7, 7, 10), -- Quadro Abstrato - Moderno
(8, 8, 3);  -- Jaqueta de Couro - Premium