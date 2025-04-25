# importar biblioteca
from flask import Flask, jsonify, render_template
# importe para documentacao
from flask_pydantic_spec import FlaskPydanticSpec
import datetime
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# [flask routes] para listar rotas da api

# criar variavel para receber a classe Flask
app = Flask(__name__)

#   documentacao OpenAPI
spec = FlaskPydanticSpec('flask',
                         title='First API - SENAI',
                         version='1.0.0')
spec.register(app)

@app.route('/')
def index():
    return 'hello world'

@app.route('/validade/<dia>/<mes>/<ano>')
def validado(dia, mes, ano):
    prazo = 12
    meses = datetime.now()+relativedelta(months=prazo)
    # years=
    anos = datetime.now()+relativedelta(years=prazo)
    # weeks=
    semanas = datetime.now()+relativedelta(weeks=prazo)
    # days=
    dias = datetime.now()+relativedelta(days=prazo)

    ano = int(ano)
    mes = int(mes)
    dia = int(dia)

    data_fabricacao = date(ano, mes, dia)
    data_atual = datetime.now()
    data_composta = data_atual.strftime('%d/%m/%Y')

    validade_dia = data_fabricacao + dias
    validade_semana = data_fabricacao + semanas
    validade_mes = data_fabricacao + meses
    validade_anos = data_fabricacao + anos

    return jsonify({"antes": datetime.now().strftime('%d/%m/%Y'),
            "data de fabricacao": data_fabricacao,
            "dias": validade_dia,
            "semanas": validade_semana,
            "meses": validade_mes,
            "anos": validade_anos})


# iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)