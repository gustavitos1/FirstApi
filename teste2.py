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
        if not all(key in dados_usuario for key in ("Nome", "cpf", "Endereco")):
            return jsonify({"message": "Preencha todos os campos necessários"}), 400

        novo_usuario = Usuario(
            Nome=dados_usuario['Nome'],
            cpf=dados_usuario['cpf'],
            Endereco=dados_usuario['Endereco']
        )
        db_session.add(novo_usuario)
        db_session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso", "usuario": novo_usuario.serialize()}), 201
    except Exception as e:
        return jsonify({"message": f"Erro ao cadastrar usuário: {str(e)}"}), 500

@app.route("/cadastrar_livro", methods=['POST'])
def cadastrar_livro():
    try:
        dados_livro = request.get_json()
        if not all(key in dados_livro for key in ("ISBN", "Titulo", "Autor", "Resumo")):
            return jsonify({"message": "Preencha todos os campos necessários"}), 400

        novo_livro = Livro(
            ISBN=dados_livro['ISBN'],
            Titulo=dados_livro['Titulo'],
            Autor=dados_livro['Autor'],
            Resumo=dados_livro['Resumo']
        )
        db_session.add(novo_livro)
        db_session.commit()
        return jsonify({"message": "Livro cadastrado com sucesso", "livro": novo_livro.serialize()}), 201
    except Exception as e:
        return jsonify({"message": f"Erro ao cadastrar livro: {str(e)}"}), 500

@app.route("/cadastrar_emprestimo", methods=['POST'])
def cadastrar_emprestimo():
    try:
        dados_emprestimo = request.get_json()
        if not all(key in dados_emprestimo for key in ("Data_Emprestimo", "Data_Devolucao", "id_livro", "id_usuario")):
            return jsonify({"message": "Preencha todos os campos necessários"}), 400

        novo_emprestimo = Emprestimo(
            Data_Emprestimo=dados_emprestimo['Data_Emprestimo'],
            Data_Devolucao=dados_emprestimo['Data_Devolucao'],
            id_livro=dados_emprestimo['id_livro'],
            id_usuario=dados_emprestimo['id_usuario']
        )
        db_session.add(novo_emprestimo)
        db_session.commit()
        return jsonify({"message": "Empréstimo cadastrado com sucesso", "emprestimo": novo_emprestimo.serialize()}), 201
    except Exception as e:
        return jsonify({"message": f"Erro ao cadastrar empréstimo: {str(e)}"}), 500



@app.route("/livros", methods=['GET'])
def livros():
    try:
        sql_livros = Select(Livro)
        lista_livros = db_session.execute(sql_livros).scalars().all()
        resultado = [livro.serialize() for livro in lista_livros]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao buscar livros: {str(e)}"}), 500

@app.route("/usuarios", methods=['GET'])
def usuarios():
    try:
        sql_usuarios = Select(Usuario)
        lista_usuarios = db_session.execute(sql_usuarios).scalars().all()
        resultado = [usuario.serialize() for usuario in lista_usuarios]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao buscar usuários: {str(e)}"}), 500

@app.route("/emprestimos", methods=['GET'])
def emprestimos():
    try:
        sql_emprestimos = Select(Emprestimo)
        lista_emprestimos = db_session.execute(sql_emprestimos).scalars().all()
        resultado = [emprestimo.serialize() for emprestimo in lista_emprestimos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao buscar empréstimos: {str(e)}"}), 500


@app.route("/editar_usuario/<int:id_usuario>", methods=['PUT'])
def editar_usuario(id_usuario):
    try:
        usuario = db_session.query(Usuario).get(id_usuario)
        if not usuario:
            return jsonify({"message": "Usuário não encontrado"}), 404

        dados_usuario = request.get_json()
        if not dados_usuario:
            return jsonify({"message": "Nenhum dado fornecido para atualização"}), 400

        # Atualiza apenas os campos fornecidos
        if "Nome" in dados_usuario:
            usuario.Nome = dados_usuario["Nome"]
        if "cpf" in dados_usuario:
            usuario.cpf = dados_usuario["cpf"]
        if "Endereco" in dados_usuario:
            usuario.Endereco = dados_usuario["Endereco"]

        db_session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso", "usuario": usuario.serialize()}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"message": f"Erro ao editar usuário: {str(e)}"}), 500



@app.route("/excluir_usuario/<int:id_usuario>", methods=['DELETE'])
def excluir_usuario(id_usuario):
    try:
        usuario = db_session.query(Usuario).get(id_usuario)
        if not usuario:
            return jsonify({"message": "Usuário não encontrado"}), 404

        db_session.delete(usuario)
        db_session.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir usuário: {str(e)}"}), 500

@app.route("/editar_livro/<int:id_livro>", methods=['PUT'])
def editar_livro(id_livro):
    try:
        livro = db_session.query(Livro).get(id_livro)
        if not livro:
            return jsonify({"message": "Livro não encontrado"}), 404

        dados_livro = request.get_json()
        if not dados_livro:
            return jsonify({"message": "Nenhum dado fornecido para atualização"}), 400

        # Atualiza apenas os campos fornecidos
        if "ISBN" in dados_livro:
            livro.ISBN = dados_livro["ISBN"]
        if "Titulo" in dados_livro:
            livro.Titulo = dados_livro["Titulo"]
        if "Autor" in dados_livro:
            livro.Autor = dados_livro["Autor"]
        if "Resumo" in dados_livro:
            livro.Resumo = dados_livro["Resumo"]

        db_session.commit()
        return jsonify({"message": "Livro atualizado com sucesso", "livro": livro.serialize()}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"message": f"Erro ao editar livro: {str(e)}"}), 500


@app.route("/excluir_livro/<int:id_livro>", methods=['DELETE'])
def excluir_livro(id_livro):
    try:
        livro = db_session.query(Livro).get(id_livro)
        if not livro:
            return jsonify({"message": "Livro não encontrado"}), 404

        db_session.delete(livro)
        db_session.commit()
        return jsonify({"message": "Livro excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir livro: {str(e)}"}), 500

@app.route("/editar_emprestimo/<int:id_emprestimo>", methods=['PUT'])
def editar_emprestimo(id_emprestimo):
    try:
        emprestimo = db_session.query(Emprestimo).get(id_emprestimo)
        if not emprestimo:
            return jsonify({"message": "Empréstimo não encontrado"}), 404

        dados_emprestimo = request.get_json()
        if not dados_emprestimo:
            return jsonify({"message": "Nenhum dado fornecido para atualização"}), 400

        # Atualiza apenas os campos fornecidos
        if "Data_Emprestimo" in dados_emprestimo:
            emprestimo.Data_Emprestimo = dados_emprestimo["Data_Emprestimo"]
        if "Data_Devolucao" in dados_emprestimo:
            emprestimo.Data_Devolucao = dados_emprestimo["Data_Devolucao"]
        if "id_livro" in dados_emprestimo:
            emprestimo.id_livro = dados_emprestimo["id_livro"]
        if "id_usuario" in dados_emprestimo:
            emprestimo.id_usuario = dados_emprestimo["id_usuario"]

        db_session.commit()
        return jsonify({"message": "Empréstimo atualizado com sucesso", "emprestimo": emprestimo.serialize()}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({"message": f"Erro ao editar empréstimo: {str(e)}"}), 500


@app.route("/excluir_emprestimo/<int:id_emprestimo>", methods=['DELETE'])
def excluir_emprestimo(id_emprestimo):
    try:
        emprestimo = db_session.query(Emprestimo).get(id_emprestimo)
        if not emprestimo:
            return jsonify({"message": "Empréstimo não encontrado"}), 404

        db_session.delete(emprestimo)
        db_session.commit()
        return jsonify({"message": "Empréstimo excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir empréstimo: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True)
