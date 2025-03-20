from datetime import datetime, date
from flask import Flask, jsonify
from flask_pydantic_spec import FlaskPydanticSpec

app = Flask(__name__)
spec = FlaskPydanticSpec('flask',
                          title = 'First API - Senai',
                          version = '1.0.0',)
spec.register(app)
tempo = datetime.now()

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/<dia>/<mes>/<ano>')
def data(dia, mes, ano):
    """
    API para calcular diferença entre duas datas

    ##Endpoint:
    data(dia, mes, ano)

    ## Parametros:
    dia, mes, ano

    ## Resposta (JSON)
    '''json
    {
        "situacao": futuro,
        "data_inserida": 12/8/2025,
        "data_atual": 20/3/2025,
        "dias de diferenca": 144,
        "meses de diferenca": 5,
        "anos de diferenca": 0
    }

    ''
    ## Erros possiveis:
    "gera erro quando a data inserida nõo segue o formato DD/MM/YYYY"
    """
    try:
        dia = int(dia)
        mes = int(mes)
        ano = int(ano)
        temporecebido = datetime(ano, mes, dia)
        data_atual = datetime.now()
        data_composta = data_atual.strftime('%d/%m/%Y')

        if temporecebido > data_atual:
            situacao = 'futuro'
        elif temporecebido < data_atual:
            situacao = 'passado'
        else:
            situacao = 'presente'

        dias_diferenca = abs(temporecebido - data_atual).days
        meses_diferenca = dias_diferenca // 30
        anos_diferenca = dias_diferenca // 365.25

        return jsonify({'situacao': situacao,
                        "data_inserida": temporecebido,
                        "data_atual": data_composta,
                        "dias de diferenca": dias_diferenca,
                        "meses de diferenca": meses_diferenca,
                        "anos de diferenca": anos_diferenca})
    except TypeError:
        return jsonify({'situacao': 'erro'})


if __name__ == '__main__':
    app.run(debug=True)