from flask import Flask, render_template, request, url_for, session, redirect
import re
import numpy as np
import os
import math
from hypercomplex import Quaternion, parse_quaternion_expr


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

# Dicionário global para mapear funções matemáticas aos métodos do NumPy
# Isso permitirá avaliar expressões com funções de forma segura sem usar eval()
NUMPY_FUNCTIONS = {
    'sin': np.sin,
    'cos': np.cos,
    'tan': np.tan,
    'asin': np.arcsin,
    'acos': np.arccos,
    'atan': np.arctan,
    'sinh': np.sinh,
    'cosh': np.cosh,
    'tanh': np.tanh,
    'asinh': np.arcsinh,
    'acosh': np.arccosh,
    'atanh': np.arctanh,
    'sqrt': np.sqrt,
    'abs': np.abs,
    'log': np.log10,
    'ln': np.log,
    'exp': np.exp,
    'pi': np.pi,
    'e': np.e,
    'real': np.real,
    'imag': np.imag,
    'conj': np.conj,
    'arg': np.angle,
    'mod': np.mod,
}

def parse_complex_expr(expression):
    """
    Converte uma expressão matemática em formato adequado para o NumPy,
    tratando números complexos e substituindo funções.
    """
    # Substituir 'i' e 'j' por '1j' quando forem a unidade imaginária isolada
    expression = re.sub(r'(?<![0-9a-zA-Z])i(?![0-9a-zA-Z_(])', '1j', expression)
    #expression = re.sub(r'(?<![0-9])j(?![0-9a-zA-Z_(])', '1j', expression)
    
    # Substituir notações como 3i ou 5j por 3j ou 5j (formato NumPy)
    expression = re.sub(r'(\d+)i(?![a-zA-Z0-9_(])', r'\1j', expression)
    
    # Substituir espaços entre números e 'j' (ex: "3 j" para "3j")
    expression = re.sub(r'(\d+)\s+j', r'\1j', expression)
    
    # Substituir função mod(x, y) por np.mod(x, y)
    expression = re.sub(r'mod\s*\(([^,]+),([^)]+)\)', r'np.mod(\1,\2)', expression)
    
    # Substituir operadores de potência
    expression = re.sub(r'(\d+|[a-zA-Z_]+|\))\s*\*\*\s*(\d+|[a-zA-Z_]+|\()', r'\1**\2', expression)
    
    return expression

def safe_eval_expr(expression, angle_mode='rad'):
    """
    Avalia expressões matemáticas de forma segura usando NumPy,
    com suporte para diferentes modos angulares.
    
    Args:
        expression: A expressão matemática a ser avaliada
        angle_mode: 'rad' para radianos, 'deg' para graus
    
    Returns:
        O resultado da avaliação da expressão
    """
    # Preparar ambiente seguro para avaliação
    safe_env = {
        'np': np,
        'pi': np.pi,
        'e': np.e,
        'j': 1j,  # j é a unidade imaginária no NumPy
    }
    
    # Adicionar funções matemáticas ao ambiente
    for func_name, func in NUMPY_FUNCTIONS.items():
        safe_env[func_name] = func
    
    # Processar expressões trigonométricas para o modo angular correto
    if angle_mode == 'deg':
        # Para funções trigonométricas diretas, converter entrada de grau para radiano
        expression = re.sub(r'sin\((.*?)\)', r'sin((pi/180)*(\1))', expression)
        expression = re.sub(r'cos\((.*?)\)', r'cos((pi/180)*(\1))', expression)
        expression = re.sub(r'tan\((.*?)\)', r'tan((pi/180)*(\1))', expression)
        
        # Para funções trigonométricas inversas, converter saída de radiano para grau
        expression = re.sub(r'asin\((.*?)\)', r'(180/pi)*asin(\1)', expression)
        expression = re.sub(r'acos\((.*?)\)', r'(180/pi)*acos(\1)', expression)
        expression = re.sub(r'atan\((.*?)\)', r'(180/pi)*atan(\1)', expression)
    
    # Substituir funções específicas pelo equivalente NumPy
    parsed_expr = parse_complex_expr(expression)
    
    # Avaliar a expressão no ambiente seguro
    try:
        return eval(parsed_expr, {"__builtins__": {}}, safe_env)
    except Exception as e:
        raise ValueError(f"Erro ao avaliar expressão: {str(e)}")

def format_result(value):
    """
    Formata o resultado para exibição, processando números complexos
    e reais com formatação apropriada, garantindo que o resultado seja JSON serializável.
    
    Returns:
        tuple: (formatted_value, original_value) onde formatted_value é a string formatada
               e original_value é o valor original em formato adequado para reutilização
    """
    # Para números complexos
    if isinstance(value, complex):
        # Converter para string formatada
        formatted = str(value).replace('j', 'i')
        # Manter o valor original como uma forma serializável
        original = {'type': 'complex', 'real': value.real, 'imag': value.imag}
        return formatted, original
    
    # Para arrays NumPy ou outros tipos NumPy
    elif isinstance(value, np.ndarray) or isinstance(value, np.number):
        formatted = str(value)
        # Converter para lista ou float para serialização
        if isinstance(value, np.ndarray):
            original = {'type': 'ndarray', 'value': value.tolist()}
        else:
            original = {'type': 'number', 'value': float(value)}
        return formatted, original
    
    # Para quaterniões, usamos a representação em string, mas mantemos os componentes
    elif hasattr(value, 'a') and hasattr(value, 'b') and hasattr(value, 'c') and hasattr(value, 'd'):
        formatted = str(value)
        original = {'type': 'quaternion', 'a': value.a, 'b': value.b, 'c': value.c, 'd': value.d}
        return formatted, original
    
    # Para outros tipos, converter para string
    else:
        formatted = str(value)
        # Tentar converter para float se for número
        try:
            original = {'type': 'float', 'value': float(value)}
        except (ValueError, TypeError):
            # Se não for possível converter para float, manter como string
            original = {'type': 'string', 'value': formatted}
        return formatted, original

# Adicionar esta lógica em cada rota para processar o valor original de um resultado do histórico
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
    original_result = None
    
    if request.method == "POST":
        try:
            # Verificar se estamos usando um resultado original do histórico
            if 'original_value' in request.form and request.form['original_value']:
                # Usar o valor original em vez de avaliar a expressão
                try:
                    # Tenta converter a string JSON para um dicionário
                    import json
                    original_data = json.loads(request.form['original_value'])
                    
                    # Reconstruir o valor original
                    computed = reconstruct_value(original_data)
                    
                    # Formatar o resultado para exibição
                    result, original_result = format_result(computed)
                    
                    # Usar a expressão apenas para exibição no histórico
                    # (o utilizador viu esta expressão como o resultado anterior)
                    expression = request.form["expression"]
                except Exception as e:
                    # Se houver erro ao processar o valor original, volta ao fluxo normal
                    expression = request.form["expression"]
                    computed = safe_eval_expr(expression, session['angle_mode'])
                    result, original_result = format_result(computed)
            else:
                # Fluxo normal: obter e avaliar a expressão
                expression = request.form["expression"]
                computed = safe_eval_expr(expression, session['angle_mode'])
                result, original_result = format_result(computed)
            
            # Adiciona o cálculo ao histórico do utilizador
            history_entry = {
                'expression': expression, 
                'result': result,
                'original_result': original_result  # Armazenar o valor original
            }
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

@app.route("/quaternions", methods=["GET", "POST"])
def quaternions():
    # Inicializa o histórico de cálculos de quaterniões se não existir na sessão
    if 'quaternion_history' not in session:
        session['quaternion_history'] = []
        
    result = ""  # Inicializa a variável de resultado
    original_result = None
    
    if request.method == "POST":  # Verifica se o pedido é do tipo POST (submissão de formulário)
        try:
            # Verificar se estamos usando um resultado original do histórico
            if 'original_value' in request.form and request.form['original_value']:
                # Usar o valor original em vez de avaliar a expressão
                try:
                    # Tenta converter a string JSON para um dicionário
                    import json
                    original_data = json.loads(request.form['original_value'])
                    
                    # Reconstruir o valor original
                    computed = reconstruct_value(original_data)
                    
                    # Formatar o resultado para exibição
                    result, original_result = format_result(computed)
                    
                    # Usar a expressão apenas para exibição no histórico
                    expression = request.form["expression"]
                except Exception as e:
                    # Se houver erro ao processar o valor original, volta ao fluxo normal
                    expression = request.form["expression"]
                    computed = parse_quaternion_expr(expression)
                    result, original_result = format_result(computed)
            else:
                # Fluxo normal
                expression = request.form["expression"]
                computed = parse_quaternion_expr(expression)
                result, original_result = format_result(computed)
            
            # Adiciona o cálculo ao histórico de quaterniões
            history_entry = {
                'expression': expression, 
                'result': result,
                'original_result': original_result  # Armazenar o valor original
            }
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
    original_result = None
    
    if request.method == "POST":  # Verifica se o pedido é do tipo POST (submissão de formulário)
        try:
            # Verificar se estamos usando um resultado original do histórico
            if 'original_value' in request.form and request.form['original_value']:
                # Usar o valor original em vez de avaliar a expressão
                try:
                    # Tenta converter a string JSON para um dicionário
                    import json
                    original_data = json.loads(request.form['original_value'])
                    
                    # Reconstruir o valor original
                    computed = reconstruct_value(original_data)
                    
                    # Formatar o resultado para exibição
                    result, original_result = format_result(computed)
                    
                    # Usar a expressão apenas para exibição no histórico
                    expression = request.form["expression"]
                except Exception as e:
                    # Se houver erro ao processar o valor original, volta ao fluxo normal
                    expression = request.form["expression"]
                    computed = eval(expression)
                    result, original_result = format_result(computed)
            else:
                # Fluxo normal
                expression = request.form["expression"]
                computed = eval(expression)
                result, original_result = format_result(computed)
            
            # Adiciona o cálculo ao histórico de coquaterniões
            history_entry = {
                'expression': expression, 
                'result': result,
                'original_result': original_result  # Armazenar o valor original
            }
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

# Função reconstruct_value para converter o valor original de volta para o formato adequado
def reconstruct_value(original_value):
    """
    Reconstrói o valor original a partir da representação armazenada.
    
    Args:
        original_value: Dicionário com o tipo e valor(es) original(is)
    
    Returns:
        O valor reconstruído no formato apropriado
    """
    if not isinstance(original_value, dict) or 'type' not in original_value:
        # Se não for um dicionário válido, retorna o valor como está
        return original_value
    
    value_type = original_value['type']
    
    if value_type == 'complex':
        return complex(original_value['real'], original_value['imag'])
    elif value_type == 'ndarray':
        return np.array(original_value['value'])
    elif value_type == 'number':
        return original_value['value']
    elif value_type == 'quaternion':
        return Quaternion(
            original_value['a'],
            original_value['b'],
            original_value['c'],
            original_value['d']
        )
    elif value_type == 'float':
        return original_value['value']
    elif value_type == 'string':
        return original_value['value']
    else:
        # Tipo desconhecido, retorna o valor como está
        return original_value

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
