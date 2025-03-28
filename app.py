from flask import Flask, render_template, request, url_for, session, redirect
import re
from sympy.parsing.sympy_parser import parse_expr
from sympy import sympify
import os

# O sistema de "session" (ver import) do Flask foi projetado especificamente para este propósito: 
# manter dados isolados entre diferentes utilizadores enquanto mantém persistência para um mesmo utilizador.
# Esta funcionalidade permite que cada utilizador tenha o seu próprio histórico de cálculos
# sem interferir nos dados de outros utilizadores.

app = Flask(__name__)  # Cria a aplicação Flask, utilizando o nome do módulo atual
app.secret_key = os.urandom(24)  # Chave secreta necessária para a sessão
# A linha app.secret_key = os.urandom(24) gera uma chave aleatória
# Esta chave é usada para assinar os cookies, impedindo manipulação
# Sendo que O Flask cria um cookie único no navegador de cada utilizador
# Este cookie contém um identificador de sessão criptografado
# Todas as requisições subsequentes do mesmo navegador incluem este cookie
# A geração de uma chave aleatória é importante para a segurança da aplicação

@app.route("/", methods=["GET", "POST"])
def calculatormain():
    # Inicializar histórico se não existir na sessão
    if 'history' not in session:
        session['history'] = []
    
    # Inicializar o modo angular (radianos por padrão)
    if 'angle_mode' not in session:
        session['angle_mode'] = 'rad'
    
    # Processar alteração do modo angular se solicitado
    if request.args.get('toggle_angle_mode'):
        if session['angle_mode'] == 'rad':
            session['angle_mode'] = 'deg'
        else:
            session['angle_mode'] = 'rad'
        # Redirecionar para remover parâmetro da URL
        return redirect(url_for('calculatormain'))
        
    result = ""
    if request.method == "POST":
        try:
            # Obtém a expressão matemática submetida pelo utilizador através do formulário
            expression = request.form["expression"]
            
            # Converte representação de números complexos para o formato reconhecido pelo SymPy
            # Substitui expressões como '3j' ou '5i' por '3*I' ou '5*I' que o SymPy consegue interpretar
            expression = re.sub(r'(\d+)[ji]', r'\1*I', expression)
            
            # Verifica se o modo angular atual é graus e adapta as funções trigonométricas adequadamente
            if session['angle_mode'] == 'deg':
                # Converte os argumentos das funções trigonométricas diretas de graus para radianos
                # Multiplica os argumentos por pi/180 para converter graus em radianos
                expression = re.sub(r'sin\((.*?)\)', r'sin((pi/180)*(\1))', expression)
                expression = re.sub(r'cos\((.*?)\)', r'cos((pi/180)*(\1))', expression)
                expression = re.sub(r'tan\((.*?)\)', r'tan((pi/180)*(\1))', expression)
    
                # Converte os resultados das funções trigonométricas inversas de radianos para graus
                # Multiplica os resultados por 180/pi para converter radianos em graus
                expression = re.sub(r'asin\((.*?)\)', r'(180/pi)*asin(\1)', expression)
                expression = re.sub(r'acos\((.*?)\)', r'(180/pi)*acos(\1)', expression)
                expression = re.sub(r'atan\((.*?)\)', r'(180/pi)*atan(\1)', expression)
            
            # Processa a expressão matemática utilizando o SymPy para cálculo simbólico
            sympy_result = parse_expr(expression)
            # Avalia numericamente a expressão com 10 dígitos significativos
            computed = sympy_result.evalf(10)

            # Formata o resultado para exibição conforme o tipo de número
            if computed.is_real:
                # Se o resultado for um número real, verifica se é inteiro ou decimal
                if computed.is_integer or float(computed) == int(float(computed)):
                    # Se for inteiro ou tiver apenas zeros na parte decimal, exibe como inteiro
                    result = str(int(float(computed)))
                else:
                    # Para números decimais, mantém até 8 casas decimais e remove zeros à direita
                    result = f"{float(computed):.8f}".rstrip('0').rstrip('.')
            else:
                # Para números complexos, formata as partes real e imaginária separadamente
                real_part = float(computed.as_real_imag()[0])
                imag_part = float(computed.as_real_imag()[1])
    
                # Verifica se a parte real é um número inteiro
                if real_part == int(real_part):
                    real_str = str(int(real_part))
                else:
                    # Formata a parte real com até 8 casas decimais, removendo zeros à direita
                    real_str = f"{real_part:.8f}".rstrip('0').rstrip('.')
        
                # Verifica se a parte imaginária é um número inteiro
                if imag_part == int(imag_part):
                    imag_str = str(int(imag_part))
                else:
                    # Formata a parte imaginária com até 8 casas decimais, removendo zeros à direita
                    imag_str = f"{imag_part:.8f}".rstrip('0').rstrip('.')
    
                # Formata o número complexo completo com as partes real e imaginária
                if imag_part >= 0:
                    result = f"{real_str} + {imag_str}i" # Utiliza 'i' como unidade imaginária
                else:
                    result = f"{real_str} {imag_str}i"

            # Adiciona o cálculo ao histórico do utilizador
            history_entry = {'expression': expression, 'result': result}
            # Insere o novo cálculo no início do histórico para mostrar os mais recentes primeiro
            history = session['history']
            history.insert(0, history_entry)
            # Limita o histórico aos 20 cálculos mais recentes para evitar consumo excessivo de memória
            if len(history) > 20:
                history = history[:20]
            # Atualiza o histórico na sessão do utilizador
            session['history'] = history
            
        except Exception as e:
            # Em caso de erro durante o processamento, exibe uma mensagem de erro
            result = f"Erro: {str(e)}"

    # Prepara os dados para renderização do template
    history = session.get('history', [])
    angle_mode = session.get('angle_mode', 'rad')
    # Renderiza o template HTML com os dados preparados
    return render_template("calculator.html", result=result, history=history, angle_mode=angle_mode)

# Rota para alternar entre modos de ângulo (radianos/graus)
@app.route("/toggle_angle_mode")
def toggle_angle_mode():
    # Alterna entre os modos de ângulo: radianos (rad) e graus (deg)
    if session.get('angle_mode') == 'rad':
        session['angle_mode'] = 'deg'
    else:
        session['angle_mode'] = 'rad'
    # Redireciona o utilizador de volta à página anterior ou à página inicial
    return redirect(request.referrer or '/')

@app.route("/quaternions", methods=["GET", "POST"])
def quaternions():
    # Inicializa o histórico de cálculos de quaterniões se não existir na sessão
    if 'quaternion_history' not in session:
        session['quaternion_history'] = []
        
    result = ""  # Inicializa a variável de resultado
    if request.method == "POST":  # Verifica se o pedido é do tipo POST (submissão de formulário)
        try:
            # Obtém a expressão matemática submetida pelo utilizador
            expression = request.form["expression"]
            # Avalia a expressão diretamente utilizando eval()
            # Nota: O uso de eval() pode apresentar riscos de segurança em ambiente de produção
            result = eval(expression)
            
            # Adiciona o cálculo ao histórico de quaterniões
            # Cria um registo contendo a expressão e o resultado
            history_entry = {'expression': expression, 'result': str(result)}
            history = session['quaternion_history']
            history.insert(0, history_entry)  # Adiciona o novo cálculo no início da lista
            if len(history) > 20:
                history = history[:20]  # Limita o histórico a 20 entradas
            session['quaternion_history'] = history  # Atualiza o histórico na sessão
            
        except Exception as e:
            # Em caso de erro durante o processamento, exibe uma mensagem de erro
            result = f"Erro: {str(e)}"
            
    # Obtém o histórico atual de cálculos de quaterniões ou inicializa uma lista vazia
    history = session.get('quaternion_history', [])
    # Renderiza o template HTML para a calculadora de quaterniões
    return render_template("quaternion.html", result=result, history=history)

@app.route("/coquaternions", methods=["GET", "POST"])
def coquaternions():
    # Inicializa o histórico de cálculos de coquaterniões se não existir na sessão
    if 'coquaternion_history' not in session:
        session['coquaternion_history'] = []
        
    result = ""  # Inicializa a variável de resultado
    if request.method == "POST":  # Verifica se o pedido é do tipo POST (submissão de formulário)
        try:
            # Obtém a expressão matemática submetida pelo utilizador
            expression = request.form["expression"]
            # Avalia a expressão diretamente utilizando eval()
            # Nota: O uso de eval() pode apresentar riscos de segurança em ambiente de produção
            result = eval(expression)
            
            # Adiciona o cálculo ao histórico de coquaterniões
            # Cria um registo contendo a expressão e o resultado
            history_entry = {'expression': expression, 'result': str(result)}
            history = session['coquaternion_history']
            history.insert(0, history_entry)  # Adiciona o novo cálculo no início da lista
            if len(history) > 20:
                history = history[:20]  # Limita o histórico a 20 entradas
            session['coquaternion_history'] = history  # Atualiza o histórico na sessão
            
        except Exception as e:
            # Em caso de erro durante o processamento, exibe uma mensagem de erro
            result = f"Erro: {str(e)}"
            
    # Obtém o histórico atual de cálculos de coquaterniões ou inicializa uma lista vazia
    history = session.get('coquaternion_history', [])
    # Renderiza o template HTML para a calculadora de coquaterniões
    return render_template("coquaternion.html", result=result, history=history)

# Rota para limpar o histórico de cálculos
@app.route("/clear_history/<calculator_type>")
def clear_history(calculator_type):
    # Esta função limpa o histórico de cálculos com base no tipo de calculadora
    if calculator_type == 'standard':
        session['history'] = []  # Limpa o histórico da calculadora padrão
    elif calculator_type == 'quaternion':
        session['quaternion_history'] = []  # Limpa o histórico da calculadora de quaterniões
    elif calculator_type == 'coquaternion':
        session['coquaternion_history'] = []  # Limpa o histórico da calculadora de coquaterniões
    # Redireciona o utilizador de volta à página anterior ou à página inicial
    return redirect(request.referrer or '/')

if __name__ == "__main__":
    # Executa a aplicação quando o script é executado diretamente
    # O modo debug permite recarregar automaticamente quando há alterações no código
    # Facilita o desenvolvimento pois não é necessário reiniciar manualmente o servidor
    app.run(debug=True)

# Questões para consideração:
# Perguntar se os professores querem que seja possível utilizar a calculadora com o teclado
# Perguntar qual ângulo preferem como predefinição (radianos ou graus)
# Perguntar se devemos meter o imaginário com i ou j (sendo que j é a notação python
# Perguntar se há botões a mais e quais faltam

# Lembretes:
# Ter cuidado com a alteração dos botões de mover o cursor porque pode causar problemas com apagar ou manter o resultado
# Quando utilizamos asin(2) na parte imaginária aparece 'j' em vez de 'i'