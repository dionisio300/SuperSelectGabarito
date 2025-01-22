from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dev:1234@localhost/superselectgabarito'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    ID = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    Senha = db.Column(db.String(255), nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    Tipo = db.Column(db.Enum('admin', 'cliente'), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Telefone = db.Column(db.String(20))

class Produto(db.Model):
    __tablename__ = 'Produto'
    ID = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    Descricao = db.Column(db.Text)
    Categoria = db.Column(db.String(50))
    Preco = db.Column(db.Numeric(10, 2), nullable=False)
    Validade = db.Column(db.Date, nullable=True)
    Quantidade = db.Column(db.Integer, nullable=False)
    Disponibilidade = db.Column(db.Boolean, default=True, nullable=False)

class Comentario(db.Model):
    __tablename__ = 'Comentario'
    ID = db.Column(db.Integer, primary_key=True)
    Comentario = db.Column(db.Text, nullable=False)
    ProdutoID = db.Column(db.Integer, db.ForeignKey('Produto.ID'), nullable=False)
    UsuarioID = db.Column(db.Integer, db.ForeignKey('Usuario.ID'), nullable=False)
    DataHora = db.Column(db.DateTime, default=db.func.current_timestamp())


produto = {}
produtos = []


app.secret_key = 'chave'




@app.route('/', methods = ['GET', 'POST'])
def index():
    user = ''
    senha = ''
    usuarios = Usuario.query.all()
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('senha')

        print(user,senha)

    for usuario in usuarios:
        print(usuario.Email)
        if usuario.Email == user and usuario.Senha == senha and usuario.Tipo == 'admin':
            session['autenticado'] = True
            session['nome'] = usuario.Nome
            session['tipo'] = usuario.Tipo
            return redirect(url_for('paginaAdm'))
        
        if usuario.Email == user and usuario.Senha == senha and usuario.Tipo == 'cliente':
            session['autenticado'] = True
            session['nome'] = usuario.Nome
            session['tipo'] = usuario.Tipo
            return redirect(url_for('paginaUsuarioComum'))
    return render_template('index.html')

#flask login
@app.route('/logout')
def logout():
    session.pop('autenticado', None)
    session.pop('nome', None)
    session.pop('tipo', None)
    return redirect(url_for('index'))

@app.route('/paginaAdm')
def paginaAdm():
    if not session.get('autenticado'):
        return redirect(url_for('index'))
    
    nome = session['nome']
    tipo = session['tipo']
    return render_template('paginaAdm.html',nome=nome,tipo=tipo)

@app.route('/paginaCadastroProduto', methods = ['GET', 'POST'])
def paginaCadastroProduto():

    if not session.get('autenticado'):
        return redirect(url_for('index'))
    
    nome = 'Olá'
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        categoria = request.form.get('categoria')
        preco = request.form.get('preco')
        data_validade = request.form.get('data_validade')
        quantidade = request.form.get('quantidade')
        produto = {'nome':nome, 'descricao':descricao,'categoria':categoria, 'preco':preco,'data_validade':data_validade}
        produtos.append(produto)
        print(produtos)

        novo_produto = Produto(
            Nome = nome,
            Descricao = descricao,
            Categoria = categoria,
            Preco = preco,
            Validade = data_validade,
            Quantidade = quantidade,
        )
        db.session.add(novo_produto)
        db.session.commit()
        
    return render_template('paginaCadastroProduto.html',produtos=produtos)


@app.route('/consultarProdutos', methods = ['GET', 'POST'])
def consultarProdutos():
    if not session.get('autenticado'):
        return redirect(url_for('index'))

    produtos = Produto.query.all()
    tipo = session['tipo']
        

    return render_template('consultarProdutos.html',produtos = produtos, tipo=tipo)

@app.route('/deletarProduto', methods = ['GET', 'POST'])
def deletarProduto():
    if not session.get('autenticado'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        id_deletar = request.form.get('id_deletar')
        if id_deletar != None:
            produto = Produto.query.get(id_deletar)
            db.session.delete(produto)
            db.session.commit()
            print(produto)
            return redirect(url_for('consultarProdutos',produto = produto))
        
    return redirect(url_for('consultarProdutos'))

@app.route('/editarProduto', methods = ['GET', 'POST'])
def editarProduto():
    if not session.get('autenticado'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        id_editar = request.form.get('id_editar')
        produtoAnterior = Produto.query.get(id_editar)
        if request.method == 'POST':
            if id_editar != None:
                produtoAnterior.Nome = request.form.get('nome')
                produtoAnterior.Descricao = request.form.get('descricao')
                produtoAnterior.Categoria = request.form.get('categoria')
                produtoAnterior.Preco = request.form.get('preco')
                produtoAnterior.Validade = request.form.get('data_validade')
                
                if produtoAnterior.Validade == '' or produtoAnterior.Categoria == 'Produtos de limpeza':
                    produtoAnterior.Validade = None
                produtoAnterior.Quantidade = request.form.get('quantidade')
                print(produtoAnterior.Nome)
                print(produtoAnterior.Descricao)
                print(produtoAnterior.Categoria)
                print(produtoAnterior.Preco)
                print(produtoAnterior.Validade)
                print(produtoAnterior.Quantidade)
                db.session.commit()
                


        return redirect(url_for('consultarProdutos'))
    return redirect(url_for('consultarProdutos',produto = produto))

@app.route('/paginaUsuarioComum')
def paginaUsuarioComum():
    if not session.get('autenticado'):
        return redirect(url_for('index'))
    
    nome = session['nome']
    print(nome)
    return render_template('paginaUsuarioComum.html',nome=nome)


@app.route('/paginaComentario', methods=['GET', 'POST'])
def paginaComentario():
    if not session.get('autenticado'):
        return redirect(url_for('index'))
    
    prodComentario = []
    produtos = Produto.query.all()
    usuarios = Usuario.query.all()

    # Montando os produtos com seus comentários
    for produto in produtos:
        comentarios = Comentario.query.filter(Comentario.ProdutoID == produto.ID).all()
        dic_Comentario = {
            'nome': produto.Nome,
            'qtd': len(comentarios),
            'comentarios': comentarios,
            'id': produto.ID
        }
        prodComentario.append(dic_Comentario)
    
    comentariosProduto = []
    if request.method == 'POST':
        id = request.form.get('id_produto')
        comentarios = Comentario.query.filter_by(ProdutoID=id).all()

        # Encontrar o nome e ID do produto
        nomeProd = "Produto não encontrado"
        idProduto = None
        for produto in produtos:
            if str(produto.ID) == id:
                nomeProd = produto.Nome
                idProduto = produto.ID
                break
        
        # Processar os comentários
        for comentario in comentarios:
            user = "Usuário não encontrado"
            userId = None

            # Encontrar o usuário correspondente
            for usuario in usuarios:
                if usuario.ID == comentario.UsuarioID:
                    user = usuario.Nome
                    userId = usuario.ID
                    break

            comentario_dict = {
                'comentario': comentario.Comentario,
                'usuario': user,
                'usuarioId': userId,
                'hora': comentario.DataHora,
                'nomeProd': nomeProd,
                'idProduto': idProduto
            }
            comentariosProduto.append(comentario_dict)
            print(comentariosProduto[0])
        
        return render_template('listarComentarios.html', comentariosProduto=comentariosProduto)
    
    return render_template('paginaComentario.html', prodComentario=prodComentario, produtos=produtos)


@app.route('/fazerComentario', methods = ['GET', 'POST'])
def fazerComentario():
    if request.method == 'POST':
        comentario = request.form.get('comentario')
        idProduto =  request.form.get('id_produto')
        
        print(comentario)

        usuarios = Usuario.query.all()

        for usuario in usuarios:
            if usuario.Nome == session['nome']:
                idUduario = usuario.ID
                
                print(usuario.Nome)
                break
        print(idUduario)

        novo_comentario = Comentario(
            Comentario = comentario,
            ProdutoID = idProduto,
            UsuarioID = idUduario,
            DataHora = datetime.now()
            
        )
        
        db.session.add(novo_comentario)
        db.session.commit()



    return redirect(url_for('paginaComentario'))


@app.route('/historicoComentarios')
def historicoComentarios():
    historico = []
    produtos = Produto.query.all()
    
    for produto in produtos:
        listaComentarios = []
        comentarios = Comentario.query.filter_by(ProdutoID = produto.ID).all()
        print(comentarios)
        for comentario in comentarios:
            listaComentarios.append(comentario.Comentario)
        print(listaComentarios)
        objProduto = {
            'nomeProduto':produto.Nome,
            'comentarios':listaComentarios
        }
        historico.append(objProduto)
    
    return render_template('historicoComentarios.html',historico=historico)



app.run(debug=True)














    
