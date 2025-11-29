from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configuração da Aplicação
app = Flask(__name__)
# Configura o banco de dados SQLite (o arquivo será criado automaticamente)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    nota = db.Column(db.Integer)


@app.route('/')
def index():
    lista_livros = Livro.query.all()
    return render_template('index.html', livros=lista_livros)


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        nota = request.form['nota']

        novo_livro = Livro(titulo=titulo, autor=autor, nota=nota)
        db.session.add(novo_livro)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('cadastro.html')

@app.route('/deletar/<int:id>')
def deletar(id):
    livro_para_deletar = Livro.query.get(id)
    if livro_para_deletar:
        db.session.delete(livro_para_deletar)
        db.session.commit()

    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)