from flask import Flask, jsonify, request
from sqlalchemy import Select, select
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
        nome = dados_usuario['Nome']
        cpf = dados_usuario['CPF']
        endereco = dados_usuario['Endereco']
        if nome not in dados_usuario and cpf not in dados_usuario and endereco not in dados_usuario:
            return jsonify({"mensagem": "Preencha todos os campos"})
        form_evento = Usuario(
            cpf=cpf,
            Nome=nome,
            Endereco=endereco
        )
        form_evento.save()
        return jsonify({"mensagem": "usuario cadastrado com sucesso"})
    except TypeError:
        return jsonify({"mensagem": "Resultado Invalido"})

@app.route("/cadastrar_livro", methods=['POST'])
def cadastrar_livro():
    try:
        dados_livro = request.get_json()
        ISBN = dados_livro['ISBN']
        titulo = dados_livro['Titulo']
        autor = dados_livro['Autor']
        resumo = dados_livro['Resumo']
        if ISBN not in dados_livro and titulo not in dados_livro and autor not in dados_livro and resumo not in dados_livro:
            return jsonify({"mensagem": "Preencha todos os campos"})

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
        dados_emprestimo = request.get_json()
        data_emprestimo = dados_emprestimo['Data_Emprestimo']
        data_devolucao = dados_emprestimo['Data_Devolucao']
        id_usuario = dados_emprestimo['id_usuario']
        id_livro = dados_emprestimo['id_livro']
        if data_emprestimo not in dados_emprestimo and data_devolucao not in dados_emprestimo and id_usuario not in dados_emprestimo and id_livro not in dados_emprestimo:
            return jsonify({"mensagem": "Preencha todos os campos"})
        form_evento = Emprestimo(
                    Data_Emprestimo=data_emprestimo,
                    Data_Devolucao=data_devolucao,
                    id_livro=id_livro,
                    id_usuario=id_usuario
                )
        form_evento.save()
        return jsonify({"mensagem": "emprestimo cadastrado com sucesso"})
    except TypeError:
        return jsonify({"mensagem": "Resultado Invalido"})



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

@app.route("/emprestimos", methods=['GET'])
def emprestimos():
    sql_emprestimos = Select(Emprestimo)
    lista_emprestimos = db_session.execute(sql_emprestimos).scalars().all()
    print(lista_emprestimos)
    resultado = []
    for emprestimo in lista_emprestimos:
        resultado.append(emprestimo.serialize())
    print(resultado)
    return jsonify(resultado), 200

@app.route("/editar_usuario/<int:id_usuario>", methods=['PUT'])
def editar_usuario(id_usuario):
    usuario = db_session.execute(select(Usuario).where(Usuario.id_usuario == id_usuario)).scalar()

    if usuario is None:
        return jsonify({"mensagem": "Usuario nõo encontrado"})

    dados_usuario = request.get_json()
    nome = dados_usuario['Nome']
    cpf = dados_usuario['CPF']
    Endereco = dados_usuario['Endereco']

    usuario.Nome = nome
    usuario.cpf = cpf
    usuario.Endereco = Endereco

    usuario.save()
    return jsonify({"mensagem": "usuario editado com sucesso"})

@app.route("/editar_livro/<int:id_livro>", methods=['PUT'])
def editar_livro(id_livro):
    livro = db_session.execute(select(Livro).where(Livro.id_livro == id_livro)).scalar()

    if livro is None:
        return jsonify({"mensagem": "Livro nõo encontrado"})

    dados_livro = request.get_json()
    ISBN = dados_livro['ISBN']
    titulo = dados_livro['Titulo']
    autor = dados_livro['Autor']
    resumo = dados_livro['Resumo']

    livro.ISBN = ISBN
    livro.Titulo = titulo
    livro.Autor = autor
    livro.Resumo = resumo

    livro.save()
    return jsonify({"mensagem": "livro editado com sucesso"})

@app.route("/editar_emprestimo/<int:id_emprestimo>", methods=['PUT'])
def editar_emprestimo(id_emprestimo):
    emprestimo = db_session.execute(select(Emprestimo).where(Livro.id_livro == id_emprestimo)).scalar()

    if emprestimo is None:
        return jsonify({"mensagem": "Usuario nõo encontrado"})

    dados_emprestimo = request.get_json()
    datas_emprestimo = dados_emprestimo['Data_Emprestimo']
    data_devolucao = dados_emprestimo['Data_Devolucao']
    id_livro = dados_emprestimo['id_livro']
    id_usuario = dados_emprestimo['id_usuario']

    emprestimo.Data_Emprestimo = datas_emprestimo
    emprestimo.Data_Devolucao = data_devolucao
    emprestimo.id_livro = id_livro
    emprestimo.id_usuario = id_usuario

    emprestimo.save()
    return jsonify({"mensagem": "emprestimo nõo encontrado"})

@app.route("/deletar_usuario/<int:id_usuario>", methods=['DELETE'])
def deletar_usuario(id_usuario):
    try:
        usuario = db_session.query(Usuario).get(id_usuario)
        if not usuario:
            return jsonify({"message": "Usuário não encontrado"}), 404

        db_session.delete(usuario)
        db_session.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir usuário: {str(e)}"}), 500










if __name__ == '__main__':
    app.run(debug=True)