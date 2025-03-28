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

@app.route("/", methods=["GET", "POST"])  # Define a rota principal (/) e os métodos HTTP permitidos
def calculatormain():
    # Inicializar histórico se não existir na sessão
    # Esta verificação é feita em cada acesso à página
    if 'history' not in session:
        session['history'] = []
        # Os dados em session['history'] são específicos para cada sessão individual
        # Nenhum utilizador pode aceder dados de outros utilizadores
        # Isto garante privacidade e isolamento dos dados entre diferentes utilizadores
        
    result = ""  # Inicializa a variável de resultado como uma string vazia
    if request.method == "POST":  # Verifica se o método da requisição é POST (formulário submetido)
        try:
            # Obtém a expressão do formulário submetido pelo utilizador
            expression = request.form["expression"]
            
            # Preparar expressão para números complexos
            # Substitui notações como "2j" por "2*I" para compatibilidade com o SymPy
            expression = re.sub(r'(\d+)j', r'\1*I', expression)
            
            # Processar a expressão
            # Converte a string da expressão para uma expressão SymPy que pode ser avaliada
            sympy_result = parse_expr(expression)
            # Calcula o valor numérico da expressão com 10 casas decimais de precisão
            computed = sympy_result.evalf(10)
            
            # Formatar resultado com base no tipo
            if computed.is_real:  # Verifica se o resultado é um número real
                # Verificar se é um número inteiro ou tem apenas zeros na parte decimal
                if computed.is_integer or float(computed) == int(float(computed)):
                    # Se for inteiro, converte para inteiro e depois para string
                    result = str(int(float(computed)))
                else:
                    # Manter 8 casas decimais para números reais não inteiros
                    # Formata o número com 8 casas decimais para melhor legibilidade
                    result = f"{float(computed):.8f}"
            else:  # Se o resultado for complexo
                # Formatar parte real e imaginária separadamente
                # Extrai a parte real e imaginária do número complexo
                real_part = float(computed.as_real_imag()[0])
                imag_part = float(computed.as_real_imag()[1])
                
                # Verificar se a parte real é inteira
                if real_part == int(real_part):
                    # Se for inteira, converte para inteiro e depois para string
                    real_str = str(int(real_part))
                else:
                    # Senão, formata com 8 casas decimais
                    real_str = f"{real_part:.8f}"
                    
                # Verificar se a parte imaginária é inteira
                if imag_part == int(imag_part):
                    # Se for inteira, converte para inteiro e depois para string
                    imag_str = str(int(imag_part))
                else:
                    # Senão, formata com 8 casas decimais
                    imag_str = f"{imag_part:.8f}"
                
                # Formatação do número complexo
                # Constrói uma string formatada adequadamente para representar o número complexo
                if imag_part >= 0:
                    result = f"{real_str} + {imag_str}j"
                else:
                    result = f"{real_str} {imag_str}j"
            
            # Adicionar ao histórico (formato: expressão = resultado)
            # Cria um dicionário com a expressão e o resultado calculado
            history_entry = {'expression': expression, 'result': result}
            # Adicionar ao início para ter os mais recentes primeiro
            history = session['history']
            history.insert(0, history_entry)  # Insere no início da lista
            # Manter apenas os 20 últimos cálculos
            # Isto evita que o histórico cresça indefinidamente e ocupe muita memória
            if len(history) > 20:
                history = history[:20]  # Mantém apenas os primeiros 20 elementos
            session['history'] = history  # Atualiza o histórico na sessão
            
        except Exception as e:
            # Em caso de erro na expressão ou cálculo, cria uma mensagem de erro
            result = f"Erro: {str(e)}"

    # Passar histórico para o template
    # Obtém o histórico da sessão atual ou uma lista vazia se não existir
    history = session.get('history', [])
    # Renderiza o template HTML com o resultado e o histórico
    return render_template("calculator.html", result=result, history=history)


@app.route("/quaternions", methods=["GET", "POST"])
def quaternions():
    # Inicializa o histórico de cálculos de quaterniões se não existir
    if 'quaternion_history' not in session:
        session['quaternion_history'] = []
        
    result = ""  # Inicializa a variável de resultado
    if request.method == "POST":  # Se o formulário foi submetido
        try:
            # Obtém a expressão do formulário
            expression = request.form["expression"]
            # Avalia a expressão diretamente - cuidado com segurança em produção!
            result = eval(expression)  # Cuidado com eval() em ambiente de produção!
            
            # Adicionar ao histórico
            # Cria um registo com a expressão e o resultado
            history_entry = {'expression': expression, 'result': str(result)}
            history = session['quaternion_history']
            history.insert(0, history_entry)  # Adiciona ao início da lista
            if len(history) > 20:
                history = history[:20]  # Limita a 20 entradas
            session['quaternion_history'] = history  # Atualiza o histórico na sessão
            
        except Exception as e:
            # Em caso de erro, cria uma mensagem de erro
            result = f"Erro: {str(e)}"
            
    # Obtém o histórico atual ou uma lista vazia
    history = session.get('quaternion_history', [])
    # Renderiza o template com o resultado e histórico
    return render_template("quaternion.html", result=result, history=history)

@app.route("/coquaternions", methods=["GET", "POST"])
def coquaternions():
    # Inicializa o histórico de cálculos de coquaterniões se não existir
    if 'coquaternion_history' not in session:
        session['coquaternion_history'] = []
        
    result = ""  # Inicializa a variável de resultado
    if request.method == "POST":  # Se o formulário foi submetido
        try:
            # Obtém a expressão do formulário
            expression = request.form["expression"]
            # Avalia a expressão diretamente - cuidado com segurança em produção!
            result = eval(expression)  # Cuidado com eval() em ambiente de produção!
            
            # Adicionar ao histórico
            # Cria um registo com a expressão e o resultado
            history_entry = {'expression': expression, 'result': str(result)}
            history = session['coquaternion_history']
            history.insert(0, history_entry)  # Adiciona ao início da lista
            if len(history) > 20:
                history = history[:20]  # Limita a 20 entradas
            session['coquaternion_history'] = history  # Atualiza o histórico na sessão
            
        except Exception as e:
            # Em caso de erro, cria uma mensagem de erro
            result = f"Erro: {str(e)}"
            
    # Obtém o histórico atual ou uma lista vazia
    history = session.get('coquaternion_history', [])
    # Renderiza o template com o resultado e histórico
    return render_template("coquaternion.html", result=result, history=history)

# Adicionar rota para limpar histórico
@app.route("/clear_history/<calculator_type>")
def clear_history(calculator_type):
    # Esta função limpa o histórico de cálculos com base no tipo de calculadora
    if calculator_type == 'standard':
        session['history'] = []  # Limpa o histórico da calculadora padrão
    elif calculator_type == 'quaternion':
        session['quaternion_history'] = []  # Limpa o histórico da calculadora de quaterniões
    elif calculator_type == 'coquaternion':
        session['coquaternion_history'] = []  # Limpa o histórico da calculadora de coquaterniões
    # Redireciona para a página de onde veio o pedido ou para a página inicial
    return redirect(request.referrer or '/')

if __name__ == "__main__":
    # Executa a aplicação quando o script é executado diretamente
    # O modo debug permite recarregar automaticamente quando há alterações no código
    app.run(debug=True)

# Perguntar se os professores querem que seja possível utilizar a calculadora com o teclado
# Esta funcionalidade permitiria uma interação mais rápida e intuitiva para utilizadores
# habituados a utilizar teclado em calculadoras

# Reminders:
# Ter cuidado com a alteração dos botões de mover o cursor porque causa de apagar ou não o resultado 