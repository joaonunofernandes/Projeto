from flask import Flask, render_template, request, url_for
import re
from sympy.parsing.sympy_parser import parse_expr
from sympy import sympify

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
            
            # Preparar expressão para números complexos
            expression = re.sub(r'(\d+)j', r'\1*I', expression)
            
            # Processar a expressão
            sympy_result = parse_expr(expression)
            computed = sympy_result.evalf(10)
            
            # Formatar resultado com base no tipo
            if computed.is_real:
                # Verificar se é um número inteiro
                if computed.is_integer:
                    result = str(int(computed))  # Formato inteiro sem decimais
                else:
                    # Sempre 8 casas decimais
                    result = f"{float(computed):.8f}"
            else:
                # Formatar parte real e imaginária separadamente
                real_part = float(computed.as_real_imag()[0])
                imag_part = float(computed.as_real_imag()[1])
                
                # Verificar se cada parte é inteira
                if real_part.is_integer():
                    real_str = str(int(real_part))
                else:
                    real_str = f"{real_part:.8f}"
                    
                if imag_part.is_integer():
                    imag_str = str(int(imag_part))
                else:
                    imag_str = f"{imag_part:.8f}"
                
                # Formatação do número complexo
                if imag_part >= 0:
                    result = f"{real_str} + {imag_str}j"
                else:
                    # Se a parte imaginária for negativa, o sinal já estará incluído
                    result = f"{real_str} {imag_str}j"
                    
        except Exception as e:
            result = f"Erro: {str(e)}"
            

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

#Tratar das casa decimais, se tiver apenas 0, aparecer o numero inteiro/a unidade, senão 8 casas decimais
#Imaginários muda para complexos
#Adicionar backspace
#Adicionar função de mover o cursor (quer via rato, quer via setinhas na calculadora)