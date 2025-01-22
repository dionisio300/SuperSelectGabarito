CREATE DATABASE superselectGabarito;
USE superselectgabarito;
CREATE TABLE Usuario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    userName VARCHAR(50) UNIQUE NOT NULL,
    Tipo ENUM('admin', 'cliente') NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefone VARCHAR(20)
);

CREATE TABLE Produto (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Descricao TEXT,
    Categoria VARCHAR(50),
    Preco DECIMAL(10, 2) NOT NULL,
    Validade DATE,
    Quantidade INT NOT NULL,
    Disponibilidade BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE Comentario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Comentario TEXT NOT NULL,
    ProdutoID INT NOT NULL,
    UsuarioID INT NOT NULL,
    DataHora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ProdutoID) REFERENCES Produto(ID) ON DELETE CASCADE,
    FOREIGN KEY (UsuarioID) REFERENCES Usuario(ID) ON DELETE CASCADE
);

INSERT INTO Usuario (Nome, Senha, userName, Tipo, Email, Telefone)
VALUES 
('João Silva', 'senha123', 'joaosilva', 'cliente', 'joao@email.com', '11999999999'),
('Maria Oliveira', 'senha456', 'mariaoliveira', 'cliente', 'maria@email.com', '11988888888'),
('Carlos Pereira', 'senha789', 'carlospereira', 'admin', 'carlos@email.com', '11977777777'),
('Ana Souza', 'senha101', 'anasouza', 'cliente', 'ana@email.com', '11966666666'),
('Paulo Lima', 'senha202', 'paulolima', 'admin', 'paulo@email.com', '11955555555');

INSERT INTO Produto (Nome, Descricao, Categoria, Preco, Validade, Quantidade, Disponibilidade)
VALUES 
('Arroz Integral', 'Arroz integral orgânico', 'Alimentos', 15.00, '2026-12-31', 30, 1),
('Feijão Preto', 'Feijão preto tipo 1', 'Alimentos', 8.00, '2026-12-31', 25, 1),
('Macarrão de Trigo', 'Macarrão de trigo 500g', 'Alimentos', 4.50, '2025-12-31', 40, 1),
('Cerveja Heineken', 'Cerveja Heineken lata 350ml', 'Bebidas', 7.00, '2025-12-31', 50, 1),
('Refrigerante Coca-Cola', 'Refrigerante Coca-Cola 2L', 'Bebidas', 6.50, '2025-12-31', 60, 1),
('Suco de Laranja', 'Suco de laranja natural 1L', 'Bebidas', 5.00, '2025-12-31', 35, 1),
('Sabonete Dove', 'Sabonete Dove hidratante 90g', 'Higiene Pessoal', 3.00, NULL, 100, 1),
('Shampoo Pantene', 'Shampoo Pantene 400ml', 'Higiene Pessoal', 12.00, NULL, 75, 1),
('Pasta de Dente Colgate', 'Pasta de dente Colgate 90g', 'Higiene Pessoal', 5.00, NULL, 120, 1),
('Desinfetante Pinho Sol', 'Desinfetante Pinho Sol 500ml', 'Produtos de limpeza', 4.00, NULL, 80, 1);


INSERT INTO Comentario (Comentario, ProdutoID, UsuarioID, DataHora)
VALUES 
('Ótimo produto, entrega rápida!', 1, 1, '2025-01-06 10:30:00'),
('Produto com excelente custo-benefício.', 2, 2, '2025-01-06 11:00:00'),
('Qualidade acima do esperado, recomendo!', 3, 3, '2025-01-06 12:15:00'),
('Muito confortável e bonito!', 4, 4, '2025-01-06 13:45:00'),
('Preço justo para o que oferece.', 5, 5, '2025-01-06 14:30:00');

use superselectgabarito;
SELECT * FROM Usuario;
SELECT * FROM Produto;
SELECT * FROM Comentario;


INSERT INTO Comentario (Comentario, ProdutoID, UsuarioID, DataHora)
VALUES
('Ótimo produto, super recomendo!', 55, 1, NOW()),
('Produto de boa qualidade, mas poderia ser mais barato.', 56, 2, NOW()),
('Não gostei muito, achei que poderia ser melhor.', 57, 3, NOW()),
('Excelente! Cumpre o que promete.', 58, 4, NOW()),
('Muito bom, atendeu minhas expectativas.', 59, 5, NOW()),
('O produto é bom, mas demorou para chegar.', 60, 1, NOW()),
('Recomendo, muito bom para o uso diário.', 61, 2, NOW()),
('A qualidade do produto é ótima, vale o preço.', 62, 3, NOW()),
('Não gostei muito, achei o produto frágil.', 63, 4, NOW()),
('Muito bom, mas poderia ter mais opções de cores.', 64, 5, NOW());


