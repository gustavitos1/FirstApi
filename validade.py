from flask import Flask, jsonify
from flask_pydantic_spec import FlaskPydanticSpec
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

# Documentação OpenAPI
spec = FlaskPydanticSpec('flask', title='API Validade de Produtos', version='1.0.0')
spec.register(app)

@app.route('/')
def index():
    return 'mencione uma data de cadastro de produtos para determinar a validade'


@app.route('/validadeprodutos/<produto>/<dia>/<mes>/<ano>', methods=['GET'])
def validadeprodutos(produto, dia, mes, ano):
    '''
    API para calcular a validade de produtos de acordo com a data da fabricacão e os tipos de validade com o tempo.
    ## Endpoint:
    `GET/produto/dia/mes/ano`

    ## Parâmetros:
    - `data_str` (str): Data no formato "DD/MM/YYYY"** (exemplo: "12-03-2030").
    - **Qualquer outro formato resultará em erro.**

    #Resposta (JSON):
    ```json
    {
        "situação": Esta no periodo da validade,
        "produto": Lichia,
        "data de fabricação": 12-03-2030,
        "data de validade": 12-03-2031,
        "dias": 2175,
        "semanas": 310,
        "mes": 31,
        "anos": 5,
    }
    ```
    ## Erros possíveis:
    - Se `data_str`não estiver no formato correto, retorna erro **400 Bad Request**:
    ```
    '''
    try:
        produto = str(produto)
        dia = int(dia)
        mes = int(mes)
        ano = int(ano)
        data_fabricacao = datetime(ano, mes, dia).date()
        data_atual = datetime.now().date()

        validade_prazo = 12
        data_validade = data_fabricacao + relativedelta(months=validade_prazo)

        diferenca = relativedelta(data_validade, data_atual)

        validade_dias = (data_validade - data_atual).days
        validade_dias = abs(validade_dias)
        validade_semanas = abs(validade_dias) // 7
        validade_meses = abs(diferenca.months) + (abs(diferenca.years) * 12)
        validade_anos = abs(diferenca.years)

        if data_validade > data_atual:
            situacao = 'esta no periodo de validade'
        elif validade_dias < validade_semanas:
            situacao = 'passou do periodo da validade'
        else:
            situacao = 'hoje a validade acaba'

        return jsonify({
            "situacao": situacao,
            "produto": produto,
            "fabricacao": data_fabricacao.strftime("%d-%m-%Y"),
            "validade": data_validade.strftime("%d-%m-%Y"),
            "dias": validade_dias,
            "semanas": validade_semanas,
            "meses": validade_meses,
            "anos": validade_anos})

    except ValueError:
        return {"erro": "Formato de data inválido. Use DD-MM-YYYY."}, 400


if __name__ == '__main__':
    app.run(debug=True)