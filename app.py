from flask import Flask, render_template, request, url_for
import re
# Flask : framework web que permite criar aplicações web em Python
# render_template : permite carregar páginas HTML dinâmicas
# request : utilizado para obter dados enviados pelo utilizador (calculadora)

app = Flask(__name__)
# Cria instâncias do Flask (base da aplicação) 

@app.route("/", methods = ["GET", "POST"]) 
# "/" - serve para indicar que estamos na página inicial, logo até nova route tudo para baixo é o que é feito na main page
# "methods = ["GET", "POST"]" - Especifica que esta rota pode aceitar requisições HTTP tanto do tipo GET quanto POST
# "GET" - Usado quando o navegador solicita uma página (carregar a página)
# "POST" - Usado quando o utilizador envia dados ao servidor (enviar as "contas")

def calculatormain():
    result = ""
    if request.method == "POST": # Se o método for POST significa que o utilizador submeteu um cálculo
        try:
            expression = request.form["expression"]
            nums = re.findall(r'\(|(\d+(\.\d+)?)|\)', expression)
            oper = re.findall(r'[+-*/]', expression)
            for i in range(len(nums)):
                if nums[i] == "(":
                    num1 = nums[i+1]
                    num2 = nums[i+2]
        except:
            result = "Erro"
            

    return render_template("calculator.html", result=result)
    # Carrega o ficheiro calculator.html e passa o resultado do cálculo

@app.route("/quaternions", methods=["GET", "POST"])
def quaternions():
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            result = eval(expression)
        except:
            result = "Erro"
            
    return render_template("quaternion.html", result=result)
    # Carrega o ficheiro quaternion.html e passa o resultado do cálculo

@app.route("/coquaternions", methods=["GET", "POST"])
def coquaternions():
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            result = eval(expression)
        except:
            result = "Erro"
            
    return render_template("coquaternion.html", result=result)
    # Carrega o ficheiro coquaternion.html e passa o resultado do cálculo


# Garante que a aplicação só corre se for exectutada diretamente (python app.py)
if __name__ == "__main__":
    # Ativa o modo de debug
    app.run(debug=True)
