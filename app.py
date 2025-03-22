from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Inicializa o app Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Modelo de dados para a tabela LIVROS


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    imagem_url = db.Column(db.String(200), nullable=False)

# Função para criar o banco de dados e a tabela LIVROS (executada antes da primeira requisição)


@app.before_request
def criar_banco():
    # Cria todas as tabelas no banco de dados, caso não existam
    db.create_all()

# Rota inicial que exibe uma mensagem personalizada


@app.route('/')
def index():
    return "Bem-vindo à API de Livros! Doe seu livro e ajude a espalhar conhecimento!"

# Rota para cadastrar um novo livro


@app.route('/doar', methods=['POST'])
def doar_livro():
    try:
        data = request.get_json()

        # Verifica se todos os campos estão presentes
        if not all(key in data for key in ("titulo", "categoria", "autor", "imagem_url")):
            return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

        # Cria um novo livro
        novo_livro = Livro(
            titulo=data['titulo'],
            categoria=data['categoria'],
            autor=data['autor'],
            imagem_url=data['imagem_url']
        )

        # Adiciona ao banco de dados
        db.session.add(novo_livro)
        db.session.commit()

        return jsonify({"message": "Livro cadastrado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para listar todos os livros cadastrados


@app.route('/livros', methods=['GET'])
def listar_livros():
    livros = Livro.query.all()

    # Organiza os livros no formato JSON
    livros_lista = [{
        "id": livro.id,
        "titulo": livro.titulo,
        "categoria": livro.categoria,
        "autor": livro.autor,
        "imagem_url": livro.imagem_url
    } for livro in livros]

    return jsonify(livros_lista)


# Roda a aplicação
if __name__ == '__main__':
    app.run(debug=True)
