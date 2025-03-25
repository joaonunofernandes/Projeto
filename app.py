from flask import Flask, render_template, request, url_for, session, redirect
import re
from sympy.parsing.sympy_parser import parse_expr
from sympy import sympify
import os

# O sistema de "session" (ver import) do Flask foi projetado especificamente para este propósito: 
# manter dados isolados entre diferentes utilizadores enquanto mantém persistência para um mesmo utilizador.

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta necessária para a sessão
# A linha app.secret_key = os.urandom(24) gera uma chave aleatória
# Esta chave é usada para assinar os cookies, impedindo manipulação
# Sendo que O Flask cria um cookie único no navegador de cada usuário
# Este cookie contém um identificador de sessão criptografado
# Todas as requisições subsequentes do mesmo navegador incluem este cookie

@app.route("/", methods=["GET", "POST"]) 
def calculatormain():
    # Inicializar histórico se não existir na sessão
    if 'history' not in session:
        session['history'] = []
        # Os dados em session['history'] são específicos para cada sessão individual
        # Nenhum utilizador pode aceder dados de outros utilizadores
        
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            
            # Preparar expressão para números complexos
            expression = re.sub(r'(\d+)j', r'\1*I', expression)
            
            # Processar a expressão
            sympy_result = parse_expr(expression)
            computed = sympy_result.evalf(10)
            
            # Formatar resultado com base no tipo
            if computed.is_real:
                # Verificar se é um número inteiro ou tem apenas zeros na parte decimal
                if computed.is_integer or float(computed) == int(float(computed)):
                    result = str(int(float(computed)))
                else:
                    # Manter 8 casas decimais para números reais não inteiros
                    result = f"{float(computed):.8f}"
            else:
                # Formatar parte real e imaginária separadamente
                real_part = float(computed.as_real_imag()[0])
                imag_part = float(computed.as_real_imag()[1])
                
                # Verificar se a parte real é inteira
                if real_part == int(real_part):
                    real_str = str(int(real_part))
                else:
                    real_str = f"{real_part:.8f}"
                    
                # Verificar se a parte imaginária é inteira
                if imag_part == int(imag_part):
                    imag_str = str(int(imag_part))
                else:
                    imag_str = f"{imag_part:.8f}"
                
                # Formatação do número complexo
                if imag_part >= 0:
                    result = f"{real_str} + {imag_str}j"
                else:
                    result = f"{real_str} {imag_str}j"
            
            # Adicionar ao histórico (formato: expressão = resultado)
            history_entry = {'expression': expression, 'result': result}
            # Adicionar ao início para ter os mais recentes primeiro
            history = session['history']
            history.insert(0, history_entry)
            # Manter apenas os 20 últimos cálculos
            if len(history) > 20:
                history = history[:20]
            session['history'] = history
            
        except Exception as e:
            result = f"Erro: {str(e)}"

    # Passar histórico para o template
    history = session.get('history', [])
    return render_template("calculator.html", result=result, history=history)


@app.route("/quaternions", methods=["GET", "POST"])
def quaternions():
    if 'quaternion_history' not in session:
        session['quaternion_history'] = []
        
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            result = eval(expression)  # Cuidado com eval() em ambiente de produção!
            
            # Adicionar ao histórico
            history_entry = {'expression': expression, 'result': str(result)}
            history = session['quaternion_history']
            history.insert(0, history_entry)
            if len(history) > 20:
                history = history[:20]
            session['quaternion_history'] = history
            
        except Exception as e:
            result = f"Erro: {str(e)}"
            
    history = session.get('quaternion_history', [])
    return render_template("quaternion.html", result=result, history=history)

@app.route("/coquaternions", methods=["GET", "POST"])
def coquaternions():
    if 'coquaternion_history' not in session:
        session['coquaternion_history'] = []
        
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            result = eval(expression)  # Cuidado com eval() em ambiente de produção!
            
            # Adicionar ao histórico
            history_entry = {'expression': expression, 'result': str(result)}
            history = session['coquaternion_history']
            history.insert(0, history_entry)
            if len(history) > 20:
                history = history[:20]
            session['coquaternion_history'] = history
            
        except Exception as e:
            result = f"Erro: {str(e)}"
            
    history = session.get('coquaternion_history', [])
    return render_template("coquaternion.html", result=result, history=history)

# Adicionar rota para limpar histórico
@app.route("/clear_history/<calculator_type>")
def clear_history(calculator_type):
    if calculator_type == 'standard':
        session['history'] = []
    elif calculator_type == 'quaternion':
        session['quaternion_history'] = []
    elif calculator_type == 'coquaternion':
        session['coquaternion_history'] = []
    return redirect(request.referrer or '/')

if __name__ == "__main__":
    app.run(debug=True)

# Perguntar se os professores querem que seja possivel utilizar a calculadora com o teclado