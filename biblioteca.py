from flask import Flask, jsonify, request
from sqlalchemy import Select
from models import *
from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)
app.config['SECRET_KEY'] = '<KEY>'
spec = FlaskPydanticSpec('flask', title='API Biblioteca', version='1.0.0')
spec.register(app)

@app.route('/')
def index():
    return 'Bem vindo a Biblioteca'


@app.route("/cadastrar_usuario", methods=['POST'])
def cadastrar_usuario():
    try:
        dados_usuario = request.get_json()
        if not "Nome" in dados_usuario or not "cpf" in dados_usuario or not "Endereco" in dados_usuario:
            return jsonify({"preencher os campos necessarios"})

        else:
            form_evento = Usuario(
                cpf=request.form['form.cpf'],
                Nome=request.form['form.Nome'],
                Endereco=request.form['form.Endereco']
            )
            db_session.add(form_evento)
            db_session.commit()
            return jsonify({"usuario cadastrado com sucesso"})
    except TypeError:
        return jsonify({"Resultado Invalido"})

@app.route("/cadastrar_livro", methods=['POST'])
def cadastrar_livro():
    try:
        dados_livro = request.get_json()
        ISBN = dados_livro['ISBN']
        titulo = dados_livro['Titulo']
        autor = dados_livro['Autor']
        resumo = dados_livro['Resumo']

        form_evento = Livro(
                ISBN=ISBN,
                Titulo=titulo,
                Autor=autor,
                Resumo=resumo
            )
        form_evento.save()
        return jsonify({"mensagem": "livro cadastrado com sucesso"})
    except TypeError:
        return jsonify({"mensagem": "Resultado Invalido"})

@app.route("/cadastrar_emprestimo", methods=['POST'])
def cadastrar_emprestimo():
    try:
        if request.method == 'POST':
            if not request.form['form.Data_Emprestimo'] or not request.form['form.Data_Devolucao'] or not request.form['form.id_livro']:
                return jsonify({"preencher os campos necessarios"})
            else:
                form_evento = Emprestimo(
                    Data_Emprestimo=request.form['form.Data_Emprestimo'],
                    Data_Devolucao=request.form['form.Data_Devolucao'],
                    id_livro=request.form['form.id_livro'],
                    id_usuario=request.form['form.id_usuario']
                )
                db_session.add(form_evento)
                db_session.commit()
                return jsonify({"emprestimo cadastrado com sucesso"})
    except TypeError:
        return jsonify({"Resultado Invalido"})



@app.route("/livros", methods=['GET'])
def livros():
    sql_livros = Select(Livro)
    lista_livros = db_session.execute(sql_livros).scalars().all()
    print(lista_livros)
    resultado = []
    for livro in lista_livros:
        resultado.append(livro.serialize())
    print(resultado)
    return jsonify(resultado), 200

@app.route("/usuarios", methods=['GET'])
def usuarios():
    sql_usuarios = Select(Usuario)
    lista_usuarios = db_session.execute(sql_usuarios).scalars().all()
    print(lista_usuarios)
    resultado = []
    for usuario in lista_usuarios:
        resultado.append(usuario.serialize())
    print(resultado)
    return jsonify(resultado), 200

@app.route("/emprestimos>", methods=['GET'])
def emprestimos():
    sql_emprestimos = Select(Emprestimo)
    lista_emprestimos = db_session.execute(sql_emprestimos).scalars().all()
    print(lista_emprestimos)
    resultado = []
    for emprestimo in lista_emprestimos:
        resultado.append(emprestimo.serialize())
    print(resultado)
    return jsonify(resultado), 200

# @app.route("/editar_usuario/<int:id_usuario>", methods=['GET','POST'])
# def editar_usuario():
#     usuario = db_session.query(Usuario).filter(Usuario.id_usuario == request.form['form.id_usuario']).first()
#
#     if not usuario:
#         return jsonify({"Usuario nõo encontrado"})
#
#     if request.method == 'POST':
#         usuario.nome = request.form['form.nome']
#         usuario.cpf = request.form['form.cpf']
#         usuario.Endereco = request.form['form.Endereco']
#
#     db_session.commit()
#     return jsonify(usuario.serialize())










if __name__ == '__main__':
    app.run(debug=True)