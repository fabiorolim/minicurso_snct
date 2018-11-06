from flask import Flask, render_template, request, redirect
import sqlite3
from flask_restful import Resource, Api
from flask_cors import CORS
from contato import Contato
from carro import Carro

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configurações do banco de dados
DATABASE = 'agenda.db'

# @app.route('/')
# def index():
#     return redirect('/listar')


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Contato')


@app.route('/salvar_novo', methods=['POST'])
def salvar_novo():
    nome = request.form['nome']
    cel = request.form['cel']
    email = request.form['email']
    tipo = request.form['tipo']
    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()
    sql = "INSERT INTO contatos ('nome', 'cel', 'email', 'tipo') VALUES ('%s', '%s', '%s', '%s')" % (
        nome, cel, email, tipo)
    cursor.execute(sql)
    conexao.commit()
    return redirect('/listar')


@app.route('/listar')
def listar():
    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()
    sql = "SELECT * FROM contatos"
    cursor.execute(sql)
    contatos = cursor.fetchall()
    return render_template('listar.html', contatos=contatos, titulo='Todos os Contatos')


@app.route('/excluir<int:id>')
def excluir(id):
    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()
    sql = "DELETE FROM contatos WHERE id = %d" % id
    print(sql)
    cursor.execute(sql)
    conexao.commit()
    return redirect('/listar')


@app.route('/alterar<int:id>')
def alterar(id):
    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()
    sql = "SELECT * FROM contatos WHERE id=%d" % id
    cursor.execute(sql)
    contato = cursor.fetchone()
    return render_template('alterar.html', contato=contato, titulo='Alterar Contato')


@app.route('/salvar_alteracao', methods=['POST'])
def salvar_ateracao():
    id = int(request.form['id'])
    nome = request.form['nome']
    cel = request.form['cel']
    email = request.form['email']
    tipo = request.form['tipo']
    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()
    sql = "UPDATE contatos SET nome='%s', cel='%s', email='%s', tipo='%s' WHERE id=%d" % (
        nome, cel, email, tipo, id)
    cursor.execute(sql)
    conexao.commit()
    return redirect('/listar')


@app.route('/buscar_nome')
def buscar_nome():
    return render_template('buscar_nome.html', titulo='Buscar por Nome')


@app.route('/buscando_nome', methods=['POST'])
def buscando_nome():
    nome = request.form['nome'] + '%'
    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()
    sql = "SELECT * FROM contatos WHERE nome LIKE '%s'" % nome
    cursor.execute(sql)
    contatos = cursor.fetchall()
    return render_template('listar.html', contatos=contatos, titulo='Contatos por Nome')


@app.route('/buscar_tipo')
def buscar_tipo():
    return render_template('buscar_tipo.html', titulo='Buscar por Tipo')


@app.route('/buscando_tipo', methods=['POST'])
def buscando_tipo():
    tipo = request.form['tipo']
    conexao = sqlite3.connect(DATABASE)
    cursor = conexao.cursor()
    sql = "SELECT * FROM contatos WHERE tipo = '%s'" % tipo
    cursor.execute(sql)
    contatos = cursor.fetchall()
    return render_template('listar.html', contatos=contatos, titulo='Contatos por Tipo')


# API
api = Api(app)


class TesteApi(Resource):

    def get(self):
        conexao = sqlite3.connect(DATABASE)
        cursor = conexao.cursor()
        sql = "SELECT id, nome, cel FROM contatos"
        cursor.execute(sql)
        contatos = cursor.fetchall()
        dic_contatos = {}
        array = []
        for contato in contatos:
            c = Contato(contato[0], contato[1], contato[2])
            array.append({ 'id': c.id, 'nome': c.nome, 'telefone': c.telefone})
        return array


class TesteApi2(Resource):

    def get(self, id):
        conexao = sqlite3.connect(DATABASE)
        cursor = conexao.cursor()
        sql = "SELECT id, nome, cel FROM contatos WHERE id=%s" %id
        cursor.execute(sql)
        contato = cursor.fetchone()
        array = []
        c = Contato(contato[0], contato[1], contato[2])
        array.append({ 'id': c.id, 'nome': c.nome, 'telefone': c.telefone})
        return array


api.add_resource(TesteApi, '/api/')
api.add_resource(TesteApi2, '/api_id/<int:id>')
app.run(debug=True)
