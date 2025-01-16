-- Inserir categorias
INSERT INTO categories_category (name, slug, image, active, timestamp) VALUES
('Calçados', 'calcados', 'categories/calcados.jpg', 1, datetime('now')),
('Roupas', 'roupas', 'categories/roupas.jpg', 1, datetime('now')),
('Acessórios', 'acessorios', 'categories/acessorios.jpg', 1, datetime('now')),
('Eletrônicos', 'eletronicos', 'categories/eletronicos.jpg', 1, datetime('now')),
('Móveis', 'moveis', 'categories/moveis.jpg', 1, datetime('now')),
('Decoração', 'decoracao', 'categories/decoracao.jpg', 1, datetime('now'));

-- Inserir produtos
INSERT INTO products_product (title, slug, description, price, discount_price, stock, sku, featured, active, timestamp, category_id) VALUES
('Tênis Esportivo', 'tenis-esportivo', 'Tênis confortável e durável.', 199.99, 149.99, 50, 'SKU001', 1, 1, datetime('now'), 1),
('Camiseta Casual', 'camiseta-casual', 'Camiseta ideal para o dia a dia.', 79.99, 59.99, 100, 'SKU002', 0, 1, datetime('now'), 2),
('Jaqueta de Couro', 'jaqueta-couro', 'Jaqueta de couro premium.', 499.99, 399.99, 20, 'SKU003', 1, 1, datetime('now'), 2),
('Relógio Clássico', 'relogio-classico', 'Relógio elegante.', 899.99, 799.99, 30, 'SKU004', 1, 1, datetime('now'), 3),
('Bolsa de Couro', 'bolsa-couro', 'Bolsa espaçosa e resistente.', 699.99, 599.99, 25, 'SKU005', 0, 1, datetime('now'), 3),
('Smartphone Android', 'smartphone-android', 'Smartphone de alta performance.', 2499.99, 2199.99, 80, 'SKU006', 1, 1, datetime('now'), 4),
('Mesa de Escritório', 'mesa-escritorio', 'Mesa funcional para escritório.', 399.99, 299.99, 15, 'SKU007', 0, 1, datetime('now'), 5),
('Abajur Moderno', 'abajur-moderno', 'Abajur com design moderno.', 149.99, 129.99, 60, 'SKU008', 0, 1, datetime('now'), 6);

-- Inserir imagens dos produtos
INSERT INTO products_productimage (product_id, image, alt_text) VALUES
(1, 'products/tenis-esportivo.jpg', 'Tênis esportivo branco'),
(2, 'products/camiseta-casual.jpg', 'Camiseta casual azul'),
(3, 'products/jaqueta-couro.jpg', 'Jaqueta de couro preta'),
(4, 'products/relogio-classico.jpg', 'Relógio clássico prata'),
(5, 'products/bolsa-couro.jpg', 'Bolsa de couro marrom'),
(6, 'products/smartphone-android.jpg', 'Smartphone Android preto'),
(7, 'products/mesa-escritorio.jpg', 'Mesa de escritório compacta'),
(8, 'products/abajur-moderno.jpg', 'Abajur moderno branco');

-- Inserir tags
INSERT INTO tags_tag (title, slug, active, timestamp) VALUES
('Esporte', 'esporte', 1, datetime('now')),
('Casual', 'casual', 1, datetime('now')),
('Elegante', 'elegante', 1, datetime('now')),
('Tecnologia', 'tecnologia', 1, datetime('now')),
('Decoração', 'decoracao', 1, datetime('now'));

-- Associar tags aos produtos
INSERT INTO tags_tag_products (tag_id, product_id) VALUES
(1, 1), -- Tênis Esportivo com tag Esporte
(2, 2), -- Camiseta Casual com tag Casual
(3, 4), -- Relógio Clássico com tag Elegante
(4, 6), -- Smartphone Android com tag Tecnologia
(5, 8); -- Abajur Moderno com tag Decoração

-- Inserir usuários
INSERT INTO accounts_user (full_name, email, password, active, staff, admin, is_verified, timestamp) VALUES
('Admin User', 'admin@example.com', 'pbkdf2_sha256$320000$somehash', 1, 1, 1, 1, datetime('now')),
('Guest User', 'guest@example.com', 'pbkdf2_sha256$320000$somehash', 1, 0, 0, 0, datetime('now'));

-- Inserir pedidos
INSERT INTO orders_order (order_id, status, shipping_total, total, active, billing_profile_id, cart_id, billing_address_id, shipping_address_id) VALUES
('ORD001', 'completed', 20.00, 369.98, 1, NULL, 1, NULL, NULL),
('ORD002', 'pending', 10.00, 199.99, 1, NULL, 2, NULL, NULL);

-- Associar produtos aos pedidos
INSERT INTO carts_cartproduct (cart_id, product_id, quantity) VALUES
(1, 1, 2), -- Carrinho 1 com 2 Tênis Esportivo
(1, 2, 1), -- Carrinho 1 com 1 Camiseta Casual
(2, 3, 1); -- Carrinho 2 com 1 Jaqueta de Couro
