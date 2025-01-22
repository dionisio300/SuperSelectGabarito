-- Criar o banco de dados
CREATE DATABASE superselect;

-- Usar o banco de dados
USE superselect;

-- Criar a tabela de usuários
CREATE TABLE Usuario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    userName VARCHAR(50) UNIQUE NOT NULL,
    Tipo ENUM('admin', 'cliente') NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefone VARCHAR(20)
);

-- Criar a tabela de produtos
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

-- Criar a tabela de comentários
CREATE TABLE Comentario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Comentario TEXT NOT NULL,
    ProdutoID INT NOT NULL,
    UsuarioID INT NOT NULL,
    DataHora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ProdutoID) REFERENCES Produto(ID) ON DELETE CASCADE,
    FOREIGN KEY (UsuarioID) REFERENCES Usuario(ID) ON DELETE CASCADE
);
