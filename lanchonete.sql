-- 1. Criação do Banco e Usuário
CREATE DATABASE lanchonete;

CREATE USER user_admin WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE lanchonete TO user_admin;

-- *************************************************************
-- troque para public@lanchonete
-- *************************************************************

GRANT ALL ON SCHEMA public TO user_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO user_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO user_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO user_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO user_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO user_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO user_admin;

-- criando tabelas 
-- 1. tabela usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(20) DEFAULT 'cliente'
);


-- 2. tabela de categorias 
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(50) NOT NULL,
    descricao TEXT
);


-- 3. tabela de produtos 
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco NUMERIC(10,2) NOT NULL,
    imagem_url TEXT,
    ingredientes TEXT,
    categoria_id INT REFERENCES categorias(id) ON DELETE SET NULL
);


-- 4. tabela de pedidos
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'novo', 
    total NUMERIC(10,2) DEFAULT 0,
    observacoes TEXT
);


-- 5. tabela de itens_pedido 
CREATE TABLE itens_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id) ON DELETE CASCADE,
    produto_id INT REFERENCES produtos(id),
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) GENERATED ALWAYS AS (quantidade * preco_unitario) STORED
);


-- 6. tabela de estoque 
CREATE TABLE estoque (
    id SERIAL PRIMARY KEY,
    produto_id INT REFERENCES produtos(id) ON DELETE CASCADE,
    quantidade INT NOT NULL CHECK (quantidade >= 0)
);


-- carga de dados
INSERT INTO categorias (nome_categoria, descricao) VALUES
('Hambúrgueres Clássicos', 'Os favoritos da casa'),      -- ID 1
('Hambúrgueres Gourmet', 'Seleção especial do chef'),    -- ID 2
('Acompanhamentos', 'Porções e Bebidas');                -- ID 3


INSERT INTO produtos (nome_produto, descricao, preco, imagem_url, ingredientes, categoria_id) VALUES
-- CATEGORIA 1: CLÁSSICOS (4 Itens)
('X-Burger Tradicional', 'Hambúrguer artesanal 180g, queijo, alface, tomate e molho especial', 22.00, 'url_img', 'Pão, carne, queijo, salada', 1),
('X-Bacon Especial', 'Hambúrguer 180g, queijo, bacon crocante, cebola caramelizada', 26.00, 'url_img', 'Pão, carne, queijo, bacon', 1),
('Cheese Duplo', 'Dois hambúrgueres 180g, queijo cheddar, picles e molho especial', 28.00, 'url_img', 'Pão, 2x carne, cheddar, picles', 1),
('X-Salada Premium', 'Hambúrguer 180g, queijo, alface, tomate, cebola roxa e maionese', 24.00, 'url_img', 'Pão, carne, queijo, salada completa', 1),

-- CATEGORIA 2: GOURMET (4 Itens)
('Burger Barbecue', 'Hambúrguer 200g, queijo cheddar, bacon, onion rings e molho BBQ', 32.00, 'url_img', 'Pão, carne 200g, cheddar, bacon, onion rings', 2),
('Smash Burger Premium', 'Dois smash burgers, queijo americano, picles e molho especial', 35.00, 'url_img', 'Pão, 2x smash, americano, picles', 2),
('Burger Artesanal', 'Hambúrguer angus 200g, queijo brie, rúcula e geleia de pimenta', 38.00, 'url_img', 'Pão, angus, brie, rúcula', 2),
('Chicken Gourmet', 'Frango empanado, queijo, alface, tomate e molho ranch', 30.00, 'url_img', 'Pão, frango, queijo, salada', 2),

-- CATEGORIA 3: ACOMPANHAMENTOS (4 Itens)
('Batata Frita', 'Porção de batatas fritas crocantes', 8.00, 'url_img', 'Batata, sal', 3),
('Onion Rings', 'Anéis de cebola empanados e fritos', 12.00, 'url_img', 'Cebola', 3),
('Nuggets', 'Nuggets de frango crocantes', 15.00, 'url_img', 'Frango', 3),
('Refrigerante', 'Lata 350ml - diversos sabores', 6.00, 'url_img', 'Refrigerante', 3);

-- inserir quantidade de 50
INSERT INTO estoque (produto_id, quantidade)
SELECT id, 50 FROM produtos;