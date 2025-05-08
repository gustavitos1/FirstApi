# Documentação das Rotas da API

"""Documentação das rotas da API.

Esta documentação descreve as rotas disponíveis na API, seus métodos HTTP, parâmetros e respostas.
"""

# Rotas de Livros

# POST /r_livro
"""Cadastra um novo livro.

Métodos: POST

Parâmetros (JSON):
    ISBN (string, obrigatório): ISBN do livro.
    Titulo (string, obrigatório): Título do livro.
    Autor (string, obrigatório): Autor do livro.
    Resumo (string, obrigatório): Resumo do livro.

Resposta (JSON):
    Em caso de sucesso: {"mensagem": "livro cadastrado com sucesso"}
    Em caso de erro: {"mensagem": "Preencha todos os campos"} ou {"mensagem": "Resultado Invalido"}
"""
def cadastrar_livro():
    ...

# GET /livros
"""Retorna a lista de todos os livros.

Métodos: GET

Parâmetros: Nenhum.

Resposta (JSON): Um array de objetos JSON, cada um representando um livro com seus atributos (ISBN, Título, Autor, Resumo).
"""
def livros():
    ...

# PUT /editar_livro/<int:id_livro>
"""Edita um livro existente.

Métodos: PUT

Parâmetros (JSON):
    id_livro (inteiro, obrigatório): ID do livro a ser editado.
    ISBN (string, obrigatório): ISBN do livro.
    Titulo (string, obrigatório): Título do livro.
    Autor (string, obrigatório): Autor do livro.
    Resumo (string, obrigatório): Resumo do livro.

Resposta (JSON):
    Em caso de sucesso: {"mensagem": "livro editado com sucesso"}
    Em caso de erro: {"mensagem": "Livro não encontrado"}
"""
def editar_livro(id_livro):
    ...

# Rotas de Empréstimos

# POST /cadastrar_emprestimo
"""Cadastra um novo empréstimo.

Métodos: POST

Parâmetros (JSON):
    Data_Emprestimo (data, obrigatório): Data do empréstimo.
    Data_Devolucao (data, obrigatório): Data de devolução.
    id_usuario (inteiro, obrigatório): ID do usuário.
    id_livro (inteiro, obrigatório): ID do livro.

Resposta (JSON):
    Em caso de sucesso: {"mensagem": "emprestimo cadastrado com sucesso"}
    Em caso de erro: {"mensagem": "Preencha todos os campos"} ou {"mensagem": "Resultado Invalido"}
"""
def cadastrar_emprestimo():
    ...

# GET /emprestimos
"""Retorna a lista de todos os empréstimos.

Métodos: GET

Parâmetros: Nenhum.

Resposta (JSON): Um array de objetos JSON, cada um representando um empréstimo com seus atributos (Data de Empréstimo, Data de Devolução, ID do Usuário, ID do Livro).
"""
def emprestimos():
    ...

# PUT /editar_emprestimo/<int:id_emprestimo>
"""Edita um empréstimo existente.

Métodos: PUT

Parâmetros (JSON):
    id_emprestimo (inteiro, obrigatório): ID do empréstimo a ser editado.
    Data_Emprestimo (data, obrigatório): Data do empréstimo.
    Data_Devolucao (data, obrigatório): Data de devolução.
    id_usuario (inteiro, obrigatório): ID do usuário.
    id_livro (inteiro, obrigatório): ID do livro.

Resposta (JSON):
    Em caso de sucesso: {"mensagem": "emprestimo editado com sucesso"}
    Em caso de erro: {"mensagem": "emprestimo não encontrado"}
"""
def editar_emprestimo(id_emprestimo):
    ...

# Rotas de Usuários

# GET /usuarios
"""Retorna a lista de todos os usuários.

Métodos: GET

Parâmetros: Nenhum.

Resposta (JSON): Um array de objetos JSON, cada um representando um usuário com seus atributos (Nome, CPF, Endereço).
"""
def usuarios():
    ...

# PUT /editar_usuario/<int:id_usuario>
"""Edita um usuário existente.

Métodos: PUT

Parâmetros (JSON):
    id_usuario (inteiro, obrigatório): ID do usuário a ser editado.
    Nome (string, obrigatório): Nome do usuário.
    CPF (string, obrigatório): CPF do usuário.
    Endereco (string, obrigatório): Endereço do usuário.

Resposta (JSON):
    Em caso de sucesso: {"mensagem": "usuario editado com sucesso"}
    Em caso de erro: {"mensagem": "Usuario não encontrado"}
"""
def editar_usuario(id_usuario):
    ...
