from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/soma/<int:num1>+<int:num2>")
def soma(num1, num2):
    try:
        return f"a soma de {num1} + {num2} é {num1 + num2}"
    except TypeError:
        return f"Ocorreu um erro ao tentar somar "

@app.route("/subtracao/<int:num1>-<int:num2>")
def subtracao(num1, num2):
    try:
        return f"a subtração de {num1} - {num2} é {num1 - num2}"
    except TypeError:
        return f"Ocorreu um erro ao tentar subtrair "

@app.route("/multiplicacao/<int:num1>*<int:num2>")
def multiplicacao(num1, num2):
    try:
        return f"a multiplicação de {num1} X {num2} é {num1 * num2}"
    except TypeError:
        return f"Ocorreu um erro ao tentar multiplicar "

@app.route("/divisao/<int:num1>/<int:num2>")
def divisao(num1, num2):
    try:
        return f"a divisão de {num1} / {num2} é {num1 / num2}"
    except TypeError:
        return f"Ocorreu um erro ao tentar dividir "
    except ZeroDivisionError:
        return f"Não ha divisão por 0 "

@app.route("/parouimpar/<int:num1>")
def parouimpar(num1):
    try:
        if num1 % 2 == 0:
            return f"{num1} esse numero é par"
        else:
            return f"{num1} é impar"
    except TypeError:
        return f"valor invalido"



if __name__ == "__main__":
    app.run(debug=True)