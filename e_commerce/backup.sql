PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO django_migrations VALUES(1,'accounts','0001_initial','2025-01-21 02:34:56.971163');
INSERT INTO django_migrations VALUES(2,'billing','0001_initial','2025-01-21 02:34:57.413237');
INSERT INTO django_migrations VALUES(3,'addresses','0001_initial','2025-01-21 02:34:57.620238');
INSERT INTO django_migrations VALUES(4,'contenttypes','0001_initial','2025-01-21 02:34:57.769240');
INSERT INTO django_migrations VALUES(5,'admin','0001_initial','2025-01-21 02:34:58.036242');
INSERT INTO django_migrations VALUES(6,'admin','0002_logentry_remove_auto_add','2025-01-21 02:34:58.141243');
INSERT INTO django_migrations VALUES(7,'admin','0003_logentry_add_action_flag_choices','2025-01-21 02:34:58.301243');
INSERT INTO django_migrations VALUES(8,'contenttypes','0002_remove_content_type_name','2025-01-21 02:34:58.462248');
INSERT INTO django_migrations VALUES(9,'analytics','0001_initial','2025-01-21 02:34:59.050251');
INSERT INTO django_migrations VALUES(10,'auth','0001_initial','2025-01-21 02:34:59.351254');
INSERT INTO django_migrations VALUES(11,'auth','0002_alter_permission_name_max_length','2025-01-21 02:34:59.485256');
INSERT INTO django_migrations VALUES(12,'auth','0003_alter_user_email_max_length','2025-01-21 02:34:59.639259');
INSERT INTO django_migrations VALUES(13,'auth','0004_alter_user_username_opts','2025-01-21 02:34:59.776264');
INSERT INTO django_migrations VALUES(14,'auth','0005_alter_user_last_login_null','2025-01-21 02:34:59.941259');
INSERT INTO django_migrations VALUES(15,'auth','0006_require_contenttypes_0002','2025-01-21 02:35:00.186263');
INSERT INTO django_migrations VALUES(16,'auth','0007_alter_validators_add_error_messages','2025-01-21 02:35:00.306263');
INSERT INTO django_migrations VALUES(17,'auth','0008_alter_user_username_max_length','2025-01-21 02:35:00.426264');
INSERT INTO django_migrations VALUES(18,'auth','0009_alter_user_last_name_max_length','2025-01-21 02:35:00.536265');
INSERT INTO django_migrations VALUES(19,'auth','0010_alter_group_name_max_length','2025-01-21 02:35:00.666269');
INSERT INTO django_migrations VALUES(20,'auth','0011_update_proxy_permissions','2025-01-21 02:35:00.847270');
INSERT INTO django_migrations VALUES(21,'auth','0012_alter_user_first_name_max_length','2025-01-21 02:35:00.955269');
INSERT INTO django_migrations VALUES(22,'categories','0001_initial','2025-01-21 02:35:01.415278');
INSERT INTO django_migrations VALUES(23,'products','0001_initial','2025-01-21 02:35:01.775278');
INSERT INTO django_migrations VALUES(24,'carts','0001_initial','2025-01-21 02:35:02.082282');
INSERT INTO django_migrations VALUES(25,'orders','0001_initial','2025-01-21 02:35:02.453284');
INSERT INTO django_migrations VALUES(26,'sessions','0001_initial','2025-01-21 02:35:02.958291');
INSERT INTO django_migrations VALUES(27,'tags','0001_initial','2025-01-21 02:35:03.342292');
CREATE TABLE IF NOT EXISTS "accounts_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "full_name" varchar(255) NULL, "email" varchar(255) NOT NULL UNIQUE, "active" bool NOT NULL, "staff" bool NOT NULL, "admin" bool NOT NULL, "is_verified" bool NOT NULL, "timestamp" datetime NOT NULL);
INSERT INTO accounts_user VALUES(1,'pbkdf2_sha256$320000$somehash',NULL,'Admin User','admin@example.com',1,1,1,1,'2025-01-21 02:35:13');
INSERT INTO accounts_user VALUES(2,'pbkdf2_sha256$320000$somehash',NULL,'Guest User','guest@example.com',1,0,0,0,'2025-01-21 02:35:13');
INSERT INTO accounts_user VALUES(3,'pbkdf2_sha256$320000$somehash',NULL,'Test User','test@example.com',1,0,0,1,'2025-01-21 02:35:13');
INSERT INTO accounts_user VALUES(4,'pbkdf2_sha256$720000$Bk3xvTgpy3itatUxj36ywf$NTkliJV14+osEtBFjNfL73AiU58HkKr9Vvcvr6dOoD8=','2025-01-21 02:36:31.083852',NULL,'admin@mail.com',1,1,1,1,'2025-01-21 02:36:05.137508');
CREATE TABLE IF NOT EXISTS "accounts_guestemail" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email" varchar(254) NOT NULL, "active" bool NOT NULL, "update" datetime NOT NULL, "timestamp" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "billing_billingprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email" varchar(254) NOT NULL, "active" bool NOT NULL, "update" datetime NOT NULL, "timestamp" datetime NOT NULL, "customer_id" varchar(120) NULL, "user_id" bigint NULL UNIQUE REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO billing_billingprofile VALUES(1,'admin@mail.com',1,'2025-01-21 02:36:07.447057','2025-01-21 02:36:07.447057','cus_RcmtfC8gZkkqss',4);
CREATE TABLE IF NOT EXISTS "addresses_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address_type" varchar(120) NOT NULL, "street" varchar(255) NOT NULL, "complement" varchar(255) NULL, "neighborhood" varchar(255) NULL, "number" varchar(10) NULL, "city" varchar(100) NOT NULL, "state" varchar(100) NOT NULL, "country" varchar(100) NOT NULL, "postal_code" varchar(20) NOT NULL, "billing_profile_id" bigint NULL REFERENCES "billing_billingprofile" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
INSERT INTO django_admin_log VALUES(1,'14','T├¬nis de Corrida',2,'[{"changed": {"fields": ["Title"]}}]',15,4,'2025-01-21 02:36:51.831591');
INSERT INTO django_admin_log VALUES(2,'1','T├¬nis Esportivo',2,'[{"changed": {"fields": ["Title", "Description"]}}]',15,4,'2025-01-21 02:37:13.539773');
INSERT INTO django_admin_log VALUES(3,'12','├ôculos de Sol',2,'[{"changed": {"fields": ["Title", "Description"]}}]',15,4,'2025-01-21 02:38:06.610849');
INSERT INTO django_admin_log VALUES(4,'5','M├│veis',2,'[{"changed": {"fields": ["Name", "Description"]}}]',18,4,'2025-01-21 02:38:20.056978');
INSERT INTO django_admin_log VALUES(5,'6','Decora├º├úo',2,'[{"changed": {"fields": ["Name", "Description"]}}]',18,4,'2025-01-21 02:38:44.005255');
INSERT INTO django_admin_log VALUES(6,'4','Eletr├┤nicos',2,'[{"changed": {"fields": ["Name", "Description"]}}]',18,4,'2025-01-21 02:38:58.795420');
INSERT INTO django_admin_log VALUES(7,'3','Acess├│rios',2,'[{"changed": {"fields": ["Name", "Description"]}}]',18,4,'2025-01-21 02:39:15.611952');
INSERT INTO django_admin_log VALUES(8,'1','Cal├ºados',2,'[{"changed": {"fields": ["Name", "Description"]}}]',18,4,'2025-01-21 02:39:29.785057');
INSERT INTO django_admin_log VALUES(9,'4','Rel├│gio Cl?ssico',2,'[{"changed": {"fields": ["Title", "Description"]}}]',15,4,'2025-01-21 02:39:56.293775');
INSERT INTO django_admin_log VALUES(10,'4','Rel├│gio Cl├íssico',2,'[{"changed": {"fields": ["Title"]}}]',15,4,'2025-01-21 02:40:09.319304');
INSERT INTO django_admin_log VALUES(11,'1','T├¬nis Esportivo',2,'[{"changed": {"fields": ["Description"]}}, {"changed": {"name": "product image", "object": "Image for T\u00eanis Esportivo", "fields": ["Alt text"]}}]',15,4,'2025-01-21 02:40:37.404450');
INSERT INTO django_admin_log VALUES(12,'14','T├¬nis de Corrida',2,'[{"changed": {"name": "product image", "object": "Image for T\u00eanis de Corrida", "fields": ["Alt text"]}}]',15,4,'2025-01-21 02:40:52.470632');
INSERT INTO django_admin_log VALUES(13,'14','T├¬nis de Corrida',2,'[{"changed": {"name": "product image", "object": "Image for T\u00eanis de Corrida", "fields": ["Alt text"]}}]',15,4,'2025-01-21 02:41:13.529834');
INSERT INTO django_admin_log VALUES(14,'12','├ôculos de Sol',2,'[{"changed": {"name": "product image", "object": "Image for \u00d3culos de Sol", "fields": ["Alt text"]}}]',15,4,'2025-01-21 02:41:30.189005');
INSERT INTO django_admin_log VALUES(15,'7','Mesa de Escrit├│rio',2,'[{"changed": {"fields": ["Title", "Description"]}}, {"changed": {"name": "product image", "object": "Image for Mesa de Escrit\u00f3rio", "fields": ["Alt text"]}}]',15,4,'2025-01-21 02:41:53.964233');
INSERT INTO django_admin_log VALUES(16,'9','Cadeira Gamer',2,'[{"changed": {"fields": ["Description"]}}]',15,4,'2025-01-21 02:43:00.993888');
INSERT INTO django_admin_log VALUES(17,'5','Bolsa de Couro',2,'[{"changed": {"fields": ["Description"]}}]',15,4,'2025-01-21 02:43:40.162998');
INSERT INTO django_admin_log VALUES(18,'4','Rel├│gio Cl├íssico',2,'[{"changed": {"name": "product image", "object": "Image for Rel\u00f3gio Cl\u00e1ssico", "fields": ["Alt text"]}}]',15,4,'2025-01-21 02:43:56.489670');
INSERT INTO django_admin_log VALUES(19,'1','T├¬nis Esportivo',2,'[{"changed": {"name": "product image", "object": "Image for T\u00eanis Esportivo", "fields": ["Alt text"]}}]',15,4,'2025-01-21 02:44:24.930037');
INSERT INTO django_admin_log VALUES(20,'5','Decora├º├úo',2,'[{"changed": {"fields": ["Title"]}}]',17,4,'2025-01-21 02:44:41.501194');
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO django_content_type VALUES(1,'admin','logentry');
INSERT INTO django_content_type VALUES(2,'auth','permission');
INSERT INTO django_content_type VALUES(3,'auth','group');
INSERT INTO django_content_type VALUES(4,'contenttypes','contenttype');
INSERT INTO django_content_type VALUES(5,'sessions','session');
INSERT INTO django_content_type VALUES(6,'addresses','address');
INSERT INTO django_content_type VALUES(7,'analytics','objectviewed');
INSERT INTO django_content_type VALUES(8,'analytics','usersession');
INSERT INTO django_content_type VALUES(9,'billing','billingprofile');
INSERT INTO django_content_type VALUES(10,'accounts','user');
INSERT INTO django_content_type VALUES(11,'accounts','guestemail');
INSERT INTO django_content_type VALUES(12,'carts','cart');
INSERT INTO django_content_type VALUES(13,'carts','cartproduct');
INSERT INTO django_content_type VALUES(14,'orders','order');
INSERT INTO django_content_type VALUES(15,'products','product');
INSERT INTO django_content_type VALUES(16,'products','productimage');
INSERT INTO django_content_type VALUES(17,'tags','tag');
INSERT INTO django_content_type VALUES(18,'categories','category');
CREATE TABLE IF NOT EXISTS "analytics_objectviewed" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ip_address" varchar(220) NULL, "object_id" integer unsigned NOT NULL CHECK ("object_id" >= 0), "timestamp" datetime NOT NULL, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "analytics_usersession" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ip_address" varchar(220) NULL, "session_key" varchar(100) NULL, "timestamp" datetime NOT NULL, "active" bool NOT NULL, "ended" bool NOT NULL, "user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO auth_permission VALUES(1,1,'add_logentry','Can add log entry');
INSERT INTO auth_permission VALUES(2,1,'change_logentry','Can change log entry');
INSERT INTO auth_permission VALUES(3,1,'delete_logentry','Can delete log entry');
INSERT INTO auth_permission VALUES(4,1,'view_logentry','Can view log entry');
INSERT INTO auth_permission VALUES(5,2,'add_permission','Can add permission');
INSERT INTO auth_permission VALUES(6,2,'change_permission','Can change permission');
INSERT INTO auth_permission VALUES(7,2,'delete_permission','Can delete permission');
INSERT INTO auth_permission VALUES(8,2,'view_permission','Can view permission');
INSERT INTO auth_permission VALUES(9,3,'add_group','Can add group');
INSERT INTO auth_permission VALUES(10,3,'change_group','Can change group');
INSERT INTO auth_permission VALUES(11,3,'delete_group','Can delete group');
INSERT INTO auth_permission VALUES(12,3,'view_group','Can view group');
INSERT INTO auth_permission VALUES(13,4,'add_contenttype','Can add content type');
INSERT INTO auth_permission VALUES(14,4,'change_contenttype','Can change content type');
INSERT INTO auth_permission VALUES(15,4,'delete_contenttype','Can delete content type');
INSERT INTO auth_permission VALUES(16,4,'view_contenttype','Can view content type');
INSERT INTO auth_permission VALUES(17,5,'add_session','Can add session');
INSERT INTO auth_permission VALUES(18,5,'change_session','Can change session');
INSERT INTO auth_permission VALUES(19,5,'delete_session','Can delete session');
INSERT INTO auth_permission VALUES(20,5,'view_session','Can view session');
INSERT INTO auth_permission VALUES(21,6,'add_address','Can add address');
INSERT INTO auth_permission VALUES(22,6,'change_address','Can change address');
INSERT INTO auth_permission VALUES(23,6,'delete_address','Can delete address');
INSERT INTO auth_permission VALUES(24,6,'view_address','Can view address');
INSERT INTO auth_permission VALUES(25,7,'add_objectviewed','Can add Object viewed');
INSERT INTO auth_permission VALUES(26,7,'change_objectviewed','Can change Object viewed');
INSERT INTO auth_permission VALUES(27,7,'delete_objectviewed','Can delete Object viewed');
INSERT INTO auth_permission VALUES(28,7,'view_objectviewed','Can view Object viewed');
INSERT INTO auth_permission VALUES(29,8,'add_usersession','Can add user session');
INSERT INTO auth_permission VALUES(30,8,'change_usersession','Can change user session');
INSERT INTO auth_permission VALUES(31,8,'delete_usersession','Can delete user session');
INSERT INTO auth_permission VALUES(32,8,'view_usersession','Can view user session');
INSERT INTO auth_permission VALUES(33,9,'add_billingprofile','Can add billing profile');
INSERT INTO auth_permission VALUES(34,9,'change_billingprofile','Can change billing profile');
INSERT INTO auth_permission VALUES(35,9,'delete_billingprofile','Can delete billing profile');
INSERT INTO auth_permission VALUES(36,9,'view_billingprofile','Can view billing profile');
INSERT INTO auth_permission VALUES(37,10,'add_user','Can add user');
INSERT INTO auth_permission VALUES(38,10,'change_user','Can change user');
INSERT INTO auth_permission VALUES(39,10,'delete_user','Can delete user');
INSERT INTO auth_permission VALUES(40,10,'view_user','Can view user');
INSERT INTO auth_permission VALUES(41,11,'add_guestemail','Can add guest email');
INSERT INTO auth_permission VALUES(42,11,'change_guestemail','Can change guest email');
INSERT INTO auth_permission VALUES(43,11,'delete_guestemail','Can delete guest email');
INSERT INTO auth_permission VALUES(44,11,'view_guestemail','Can view guest email');
INSERT INTO auth_permission VALUES(45,12,'add_cart','Can add cart');
INSERT INTO auth_permission VALUES(46,12,'change_cart','Can change cart');
INSERT INTO auth_permission VALUES(47,12,'delete_cart','Can delete cart');
INSERT INTO auth_permission VALUES(48,12,'view_cart','Can view cart');
INSERT INTO auth_permission VALUES(49,13,'add_cartproduct','Can add cart product');
INSERT INTO auth_permission VALUES(50,13,'change_cartproduct','Can change cart product');
INSERT INTO auth_permission VALUES(51,13,'delete_cartproduct','Can delete cart product');
INSERT INTO auth_permission VALUES(52,13,'view_cartproduct','Can view cart product');
INSERT INTO auth_permission VALUES(53,14,'add_order','Can add order');
INSERT INTO auth_permission VALUES(54,14,'change_order','Can change order');
INSERT INTO auth_permission VALUES(55,14,'delete_order','Can delete order');
INSERT INTO auth_permission VALUES(56,14,'view_order','Can view order');
INSERT INTO auth_permission VALUES(57,15,'add_product','Can add product');
INSERT INTO auth_permission VALUES(58,15,'change_product','Can change product');
INSERT INTO auth_permission VALUES(59,15,'delete_product','Can delete product');
INSERT INTO auth_permission VALUES(60,15,'view_product','Can view product');
INSERT INTO auth_permission VALUES(61,16,'add_productimage','Can add product image');
INSERT INTO auth_permission VALUES(62,16,'change_productimage','Can change product image');
INSERT INTO auth_permission VALUES(63,16,'delete_productimage','Can delete product image');
INSERT INTO auth_permission VALUES(64,16,'view_productimage','Can view product image');
INSERT INTO auth_permission VALUES(65,17,'add_tag','Can add tag');
INSERT INTO auth_permission VALUES(66,17,'change_tag','Can change tag');
INSERT INTO auth_permission VALUES(67,17,'delete_tag','Can delete tag');
INSERT INTO auth_permission VALUES(68,17,'view_tag','Can view tag');
INSERT INTO auth_permission VALUES(69,18,'add_category','Can add Category');
INSERT INTO auth_permission VALUES(70,18,'change_category','Can change Category');
INSERT INTO auth_permission VALUES(71,18,'delete_category','Can delete Category');
INSERT INTO auth_permission VALUES(72,18,'view_category','Can view Category');
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "categories_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(120) NOT NULL UNIQUE, "slug" varchar(50) NOT NULL UNIQUE, "description" text NULL, "image" varchar(100) NULL, "active" bool NOT NULL, "timestamp" datetime NOT NULL, "parent_id" bigint NULL REFERENCES "categories_category" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO categories_category VALUES(1,'Cal├ºados','calcados','Categoria de cal├ºados','categories/calcados.jpg',1,'2025-01-21 02:35:12',NULL);
INSERT INTO categories_category VALUES(2,'Roupas','roupas','Categoria de roupas','categories/roupas.jpg',1,'2025-01-21 02:35:12',NULL);
INSERT INTO categories_category VALUES(3,'Acess├│rios','acessorios','Categoria de acess├│rios','categories/acessorios.jpg',1,'2025-01-21 02:35:12',NULL);
INSERT INTO categories_category VALUES(4,'Eletr├┤nicos','eletronicos','Categoria de eletr├┤nicos','categories/eletronicos.jpg',1,'2025-01-21 02:35:12',NULL);
INSERT INTO categories_category VALUES(5,'M├│veis','moveis','Categoria de m├│veis','categories/moveis.jpg',1,'2025-01-21 02:35:12',NULL);
INSERT INTO categories_category VALUES(6,'Decora├º├úo','decoracao','Categoria de decora├º├úo','categories/decoracao.jpg',1,'2025-01-21 02:35:12',NULL);
CREATE TABLE IF NOT EXISTS "products_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(120) NOT NULL, "slug" varchar(50) NOT NULL UNIQUE, "description" text NOT NULL, "price" decimal NOT NULL, "discount_price" decimal NULL, "stock" integer unsigned NOT NULL CHECK ("stock" >= 0), "sku" varchar(20) NULL UNIQUE, "featured" bool NOT NULL, "updated" datetime NOT NULL, "active" bool NOT NULL, "timestamp" datetime NOT NULL, "category_id" bigint NULL REFERENCES "categories_category" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO products_product VALUES(1,'T├¬nis Esportivo','tenis-esportivo','T├¬nis confort├ível e dur├ível.',199.99000000000000554,149.99000000000000554,50,'SKU001',1,'2025-01-21 02:44:24.921035',1,'2025-01-21 02:35:12',1);
INSERT INTO products_product VALUES(2,'Camiseta Casual','camiseta-casual','Camiseta ideal para o dia a dia.',79.98999999999999666,59.990000000000005542,100,'SKU002',0,'2025-01-21 02:35:12',1,'2025-01-21 02:35:12',2);
INSERT INTO products_product VALUES(3,'Jaqueta de Couro','jaqueta-de-couro','Jaqueta de couro premium.',499.9900000000000233,399.9900000000000233,20,'SKU003',1,'2025-01-21 02:35:12',1,'2025-01-21 02:35:12',2);
INSERT INTO products_product VALUES(4,'Rel├│gio Cl├íssico','relogio-classico','Rel├│gio elegante.',899.9900000000000233,799.9900000000000233,30,'SKU004',1,'2025-01-21 02:43:56.480671',1,'2025-01-21 02:35:12',3);
INSERT INTO products_product VALUES(5,'Bolsa de Couro','bolsa-de-couro','Bolsa espa├ºosa e resistente.',699.9900000000000233,599.9900000000000233,25,'SKU005',0,'2025-01-21 02:43:40.155999',1,'2025-01-21 02:35:12',3);
INSERT INTO products_product VALUES(6,'Smartphone Android','smartphone-android','Smartphone de alta performance.',2499.9899999999999344,2199.989999999999668,80,'SKU006',1,'2025-01-21 02:35:12',1,'2025-01-21 02:35:12',4);
INSERT INTO products_product VALUES(7,'Mesa de Escrit├│rio','mesa-de-escritorio','Mesa funcional para escrit├│rio.',399.9900000000000233,299.9900000000000233,15,'SKU007',0,'2025-01-21 02:41:53.950234',1,'2025-01-21 02:35:12',5);
INSERT INTO products_product VALUES(8,'Abajur Moderno','abajur-moderno','Abajur com design moderno.',149.99000000000000554,129.99000000000000554,60,'SKU008',0,'2025-01-21 02:35:12',1,'2025-01-21 02:35:12',6);
INSERT INTO products_product VALUES(9,'Cadeira Gamer','cadeira-gamer','Cadeira ergon├┤mica para jogos.',899.9900000000000233,799.9900000000000233,10,'SKU009',0,'2025-01-21 02:43:00.984887',1,'2025-01-21 02:35:12',5);
INSERT INTO products_product VALUES(10,'Quadro Abstrato','quadro-abstrato','Arte moderna para sua parede.',299.9900000000000233,249.9900000000000233,30,'SKU010',0,'2025-01-21 02:35:12',1,'2025-01-21 02:35:12',6);
INSERT INTO products_product VALUES(11,'Fone de Ouvido Bluetooth','fone-de-ouvido-bluetooth','Som de alta qualidade sem fio.',399.9900000000000233,349.9900000000000233,40,'SKU011',0,'2025-01-21 02:35:12',1,'2025-01-21 02:35:12',4);
INSERT INTO products_product VALUES(12,'├ôculos de Sol','oculos-de-sol','Prote├º├úo UV com estilo.',199.99000000000000554,179.99000000000000554,45,'SKU012',0,'2025-01-21 02:41:30.180005',1,'2025-01-21 02:35:12',3);
INSERT INTO products_product VALUES(13,'Smartwatch Fitness','smartwatch-fitness','Monitore suas atividades.',599.9900000000000233,499.9900000000000233,35,'SKU013',0,'2025-01-21 02:35:12',1,'2025-01-21 02:35:12',4);
INSERT INTO products_product VALUES(14,'T├¬nis de Corrida','tenis-de-corrida','Para corridas de alta performance.',299.9900000000000233,259.98999999999998777,55,'SKU014',0,'2025-01-21 02:41:13.521830',1,'2025-01-21 02:35:12',1);
CREATE TABLE IF NOT EXISTS "products_productimage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "image" varchar(100) NOT NULL, "alt_text" varchar(255) NULL, "is_featured" bool NOT NULL, "order" integer unsigned NOT NULL CHECK ("order" >= 0), "timestamp" datetime NOT NULL, "product_id" bigint NOT NULL REFERENCES "products_product" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO products_productimage VALUES(1,'products/tenis-esportivo.jpg','Tenis esportivo',1,0,'2025-01-21 02:35:12',1);
INSERT INTO products_productimage VALUES(2,'products/camiseta-casual.jpg','Camiseta casual',1,0,'2025-01-21 02:35:12',2);
INSERT INTO products_productimage VALUES(3,'products/jaqueta-de-couro.jpg','Jaqueta de couro',1,0,'2025-01-21 02:35:12',3);
INSERT INTO products_productimage VALUES(4,'products/relogio-classico.jpg','Rel├│gio cl├íssico',1,0,'2025-01-21 02:35:12',4);
INSERT INTO products_productimage VALUES(5,'products/bolsa-de-couro.jpg','Bolsa de couro',1,0,'2025-01-21 02:35:12',5);
INSERT INTO products_productimage VALUES(6,'products/smartphone-android.jpg','Smartphone Android',1,0,'2025-01-21 02:35:12',6);
INSERT INTO products_productimage VALUES(7,'products/mesa-de-escritorio.jpg','Mesa de escrit├│rio',1,0,'2025-01-21 02:35:12',7);
INSERT INTO products_productimage VALUES(8,'products/abajur-moderno.jpg','Abajur moderno',1,0,'2025-01-21 02:35:12',8);
INSERT INTO products_productimage VALUES(9,'products/cadeira-gamer.jpg','Cadeira gamer',1,0,'2025-01-21 02:35:12',9);
INSERT INTO products_productimage VALUES(10,'products/quadro-abstrato.jpg','Quadro abstrato',1,0,'2025-01-21 02:35:12',10);
INSERT INTO products_productimage VALUES(11,'products/fone-de-ouvido-bluetooth.jpg','Fone de ouvido bluetooth',1,0,'2025-01-21 02:35:12',11);
INSERT INTO products_productimage VALUES(12,'products/oculos-de-sol.jpg','├ôculos de sol',1,0,'2025-01-21 02:35:12',12);
INSERT INTO products_productimage VALUES(13,'products/smartwatch-fitness.jpg','Smartwatch fitness',1,0,'2025-01-21 02:35:12',13);
INSERT INTO products_productimage VALUES(14,'products/tenis-de-corrida.jpg','Tenis de corrida',1,0,'2025-01-21 02:35:12',14);
CREATE TABLE IF NOT EXISTS "carts_cartproduct" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "cart_id" bigint NOT NULL REFERENCES "carts_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "products_product" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO carts_cartproduct VALUES(1,2,1,1);
INSERT INTO carts_cartproduct VALUES(2,1,1,2);
INSERT INTO carts_cartproduct VALUES(3,1,2,3);
INSERT INTO carts_cartproduct VALUES(4,1,3,4);
INSERT INTO carts_cartproduct VALUES(5,1,3,6);
CREATE TABLE IF NOT EXISTS "carts_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "subtotal" decimal NOT NULL, "total" decimal NOT NULL, "updated" datetime NOT NULL, "timestamp" datetime NOT NULL, "user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO carts_cart VALUES(1,349.9800000000000022,369.98000000000001996,'2025-01-21 02:35:13','2025-01-21 02:35:13',NULL);
INSERT INTO carts_cart VALUES(2,189.9900000000000233,199.99000000000000554,'2025-01-21 02:35:13','2025-01-21 02:35:13',NULL);
INSERT INTO carts_cart VALUES(3,949.98000000000004661,999.98000000000004661,'2025-01-21 02:35:13','2025-01-21 02:35:13',NULL);
INSERT INTO carts_cart VALUES(4,0,0,'2025-01-21 02:37:16.057334','2025-01-21 02:37:16.057334',4);
CREATE TABLE IF NOT EXISTS "orders_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "order_id" varchar(120) NOT NULL, "status" varchar(120) NOT NULL, "shipping_total" decimal NOT NULL, "total" decimal NOT NULL, "active" bool NOT NULL, "billing_address_id" bigint NULL REFERENCES "addresses_address" ("id") DEFERRABLE INITIALLY DEFERRED, "billing_profile_id" bigint NULL REFERENCES "billing_billingprofile" ("id") DEFERRABLE INITIALLY DEFERRED, "cart_id" bigint NULL REFERENCES "carts_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "shipping_address_id" bigint NULL REFERENCES "addresses_address" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO orders_order VALUES(1,'ORD001','completed',20,369.98000000000001996,1,NULL,NULL,1,NULL);
INSERT INTO orders_order VALUES(2,'ORD002','pending',10,199.99000000000000554,1,NULL,NULL,2,NULL);
INSERT INTO orders_order VALUES(3,'ORD003','shipped',50,999.98000000000004661,1,NULL,NULL,3,NULL);
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO django_session VALUES('y3cy9slvb84lmxyf8gdg4bscupo3c9f1','.eJxVjssOwiAURP-FtSFCedWl-34DudxepGoggXZl_HeL6UK3c85M5sU8bGvyW6Pql5ldmGKn3ywAPih3MN8h3wrHkte6BN4VftDGpzLT83q4fwMJWupti1E6izJSJIUkxaDMKMRgtdWClBuDQa3PwkgIEEZL2sRdIyUdoMN9FKGu34_q_QGfiDvH:1ta48i:SKYF5Pg7qDjQIfpt0KzOW9UIa7G2-V3un7JdCJlIaY4','2025-02-04 02:37:16.333336');
CREATE TABLE IF NOT EXISTS "tags_tag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(120) NOT NULL, "slug" varchar(50) NOT NULL, "timestamp" datetime NOT NULL, "active" bool NOT NULL);
INSERT INTO tags_tag VALUES(1,'Esporte','esporte','2025-01-21 02:35:12',1);
INSERT INTO tags_tag VALUES(2,'Casual','casual','2025-01-21 02:35:12',1);
INSERT INTO tags_tag VALUES(3,'Elegante','elegante','2025-01-21 02:35:12',1);
INSERT INTO tags_tag VALUES(4,'Tecnologia','tecnologia','2025-01-21 02:35:12',1);
INSERT INTO tags_tag VALUES(5,'Decora├º├úo','decoracao','2025-01-21 02:35:12',1);
INSERT INTO tags_tag VALUES(6,'Conforto','conforto','2025-01-21 02:35:12',1);
INSERT INTO tags_tag VALUES(7,'Moderno','moderno','2025-01-21 02:35:12',1);
INSERT INTO tags_tag VALUES(8,'Premium','premium','2025-01-21 02:35:12',1);
CREATE TABLE IF NOT EXISTS "tags_tag_products" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "tag_id" bigint NOT NULL REFERENCES "tags_tag" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "products_product" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO tags_tag_products VALUES(1,1,1);
INSERT INTO tags_tag_products VALUES(2,2,2);
INSERT INTO tags_tag_products VALUES(3,3,4);
INSERT INTO tags_tag_products VALUES(4,4,6);
INSERT INTO tags_tag_products VALUES(5,5,8);
INSERT INTO tags_tag_products VALUES(6,6,9);
INSERT INTO tags_tag_products VALUES(7,7,10);
INSERT INTO tags_tag_products VALUES(8,8,3);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('django_migrations',27);
INSERT INTO sqlite_sequence VALUES('django_admin_log',20);
INSERT INTO sqlite_sequence VALUES('django_content_type',18);
INSERT INTO sqlite_sequence VALUES('auth_permission',72);
INSERT INTO sqlite_sequence VALUES('auth_group',0);
INSERT INTO sqlite_sequence VALUES('carts_cart',4);
INSERT INTO sqlite_sequence VALUES('categories_category',6);
INSERT INTO sqlite_sequence VALUES('products_product',14);
INSERT INTO sqlite_sequence VALUES('products_productimage',14);
INSERT INTO sqlite_sequence VALUES('tags_tag',8);
INSERT INTO sqlite_sequence VALUES('accounts_user',4);
INSERT INTO sqlite_sequence VALUES('orders_order',3);
INSERT INTO sqlite_sequence VALUES('carts_cartproduct',5);
INSERT INTO sqlite_sequence VALUES('tags_tag_products',8);
INSERT INTO sqlite_sequence VALUES('billing_billingprofile',1);
CREATE INDEX "addresses_address_billing_profile_id_115cdf27" ON "addresses_address" ("billing_profile_id");
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE INDEX "analytics_objectviewed_content_type_id_35d996a4" ON "analytics_objectviewed" ("content_type_id");
CREATE INDEX "analytics_objectviewed_user_id_b1e9cf2a" ON "analytics_objectviewed" ("user_id");
CREATE INDEX "analytics_usersession_user_id_548abc25" ON "analytics_usersession" ("user_id");
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE INDEX "categories_category_parent_id_f141de59" ON "categories_category" ("parent_id");
CREATE INDEX "products_product_category_id_9b594869" ON "products_product" ("category_id");
CREATE INDEX "products_productimage_product_id_e747596a" ON "products_productimage" ("product_id");
CREATE INDEX "carts_cartproduct_cart_id_11343bd6" ON "carts_cartproduct" ("cart_id");
CREATE INDEX "carts_cartproduct_product_id_334ec44f" ON "carts_cartproduct" ("product_id");
CREATE INDEX "carts_cart_user_id_bd0756c7" ON "carts_cart" ("user_id");
CREATE INDEX "orders_order_billing_address_id_deb02e83" ON "orders_order" ("billing_address_id");
CREATE INDEX "orders_order_billing_profile_id_0e11b610" ON "orders_order" ("billing_profile_id");
CREATE INDEX "orders_order_cart_id_7e0252e3" ON "orders_order" ("cart_id");
CREATE INDEX "orders_order_shipping_address_id_c4f8227a" ON "orders_order" ("shipping_address_id");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE INDEX "tags_tag_slug_78c2b8d8" ON "tags_tag" ("slug");
CREATE UNIQUE INDEX "tags_tag_products_tag_id_product_id_ed6e4461_uniq" ON "tags_tag_products" ("tag_id", "product_id");
CREATE INDEX "tags_tag_products_tag_id_7ed0fcd2" ON "tags_tag_products" ("tag_id");
CREATE INDEX "tags_tag_products_product_id_f64ffb65" ON "tags_tag_products" ("product_id");
COMMIT;
