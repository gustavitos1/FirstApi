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
    """
    Cadastrar Usuario

    Endpoint:
    POST /cadastrar_usuario

    Parameters:
    none

    resposta JSON:
    {
        "nome": douglas,
        "cpf": 128202523,
        "endereco": Rua cabral
    }
    :return:
    """
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
    """
    Cadastrar Livro

    Endpoint:
    POST /cadastrar_livro

    parametros:
    none

    resposta JSON:
    {
        "ISBN": douglas,
        "titulo": A arte da guerra,
        "autor": Sun Tzu,
        "resumo": dicas de guerra para a vida,
    }
    :return:
    """
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
    """
    Cadastrar Emprestimo

    Endpoint:
    POST /cadastrar_emprestimo

    parametros:
    none

    resposta JSON:
    {
        "data_emprestimo": 12/04/2020,
        "data_devolucao": 27/04/2020,
        "id_usuario": 1,
        "id_livro": 2,
    }
    :return:
    """
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
    """
    Listar Livros

    Endpoint:
    GET /livros

    parametros:
    none

    resposta JSON:

    :return:
    """
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
    """
    listar Usuarios

    Endpoint:
    GET /usuarios

    parametros:
    none

    resposta JSON:

    :return:
    """
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
    """
    listar Emprestimos

    Endpoint:
    GET /emprestimos

    parametros:
    none

    resposta JSON:

    :return:
    """
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
    """
    Editar Usuario

    Endpoint:
    PUT /editar_usuario/<id_usuario>

    parametros:
    id_usuario

    resposta JSON:

    :param id_usuario:
    :return:
    """
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
    """
    Editar Livro

    Endpoint:
    PUT /editar_livro/<id_livro>

    parametros:
    id_livro

    resposta JSON:

    :param id_livro:
    :return:
    """
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
    """
    Editar Emprestimo

    Endpoint:
    PUT /editar_emprestimo/<id_emprestimo>

    parametros:
    id_emprestimo

    resposta JSON:

    :param id_emprestimo:
    :return:
    """
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

@app.route("/deletar_livro/<int:id_livro>", methods=['DELETE'])
def deletar_livro(id_livro):
    try:
        livro = db_session.query(Livro).get(id_livro)
        if not livro:
            return jsonify({"message": "Livro não encontrado"}), 404

        db_session.delete(livro)
        db_session.commit()
        return jsonify({"message": "Livro excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir o livro: {str(e)}"}), 500

@app.route("/deletar_emprestimo/<int:id_emprestimo>", methods=['DELETE'])
def deletar_emprestimo(id_emprestimo):
    try:
        emprestimo = db_session.query(Usuario).get(id_emprestimo)
        if not emprestimo:
            return jsonify({"message": "Emprestimo não encontrado"}), 404

        db_session.delete(emprestimo)
        db_session.commit()
        return jsonify({"message": "Emprestimo excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir emprestimo: {str(e)}"}), 500










if __name__ == '__main__':
    app.run(debug=True)