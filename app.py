from flask import Flask, render_template, request, url_for, session, redirect
import re
import numpy as np
import os
import math
from hypercomplex import Quaternion, Coquaternion, parse_quaternion_expr, parse_coquaternion_expr

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Dicionário global para mapear funções matemáticas aos métodos do NumPy
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
    processando números complexos e substituindo funções.
    
    Args:
        expression (str): Expressão matemática a ser processada
    
    Returns:
        str: Expressão processada e formatada para NumPy
    """
    # Substituir 'i' e 'j' por '1j' quando forem a unidade imaginária isolada
    expression = re.sub(r'(?<![0-9a-zA-Z])i(?![0-9a-zA-Z_(])', '1j', expression)
    
    # Substituir notações como 3i ou 5j por 3j (formato NumPy)
    expression = re.sub(r'(\d+)i(?![a-zA-Z0-9_(])', r'\1j', expression)
    
    # Substituir espaços entre números e 'j'
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
        expression (str): A expressão matemática a ser avaliada
        angle_mode (str): 'rad' para radianos, 'deg' para graus
    
    Returns:
        O resultado da avaliação da expressão
    
    Raises:
        ValueError: Se ocorrer erro na avaliação da expressão
    """
    # Preparar ambiente seguro para avaliação
    safe_env = {
        'np': np,
        'pi': np.pi,
        'e': np.e,
        'j': 1j,
    }
    
    # Adicionar funções matemáticas ao ambiente
    for func_name, func in NUMPY_FUNCTIONS.items():
        safe_env[func_name] = func
    
    # Processar expressões trigonométricas para o modo angular correto
    if angle_mode == 'deg':
        # Para funções trigonométricas directas, converter entrada de grau para radiano
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
    e reais com formatação apropriada.
    
    Args:
        value: Valor a ser formatado (complexo, real, array NumPy, etc.)
    
    Returns:
        str: Resultado formatado como string
    """
    # Para números complexos
    if isinstance(value, complex):
        return str(value).replace('j', 'i')
    
    # Para arrays NumPy ou outros tipos NumPy
    elif isinstance(value, np.ndarray) or isinstance(value, np.number):
        return str(value)
    
    # Para outros tipos, converter para string
    return str(value)

@app.route("/", methods=["GET", "POST"])
def calculatormain():
    """
    Rota principal da calculadora de números reais e complexos.
    Gere cálculos, histórico e modo angular.
    
    Returns:
        str: Template HTML renderizado com os resultados
    """
    # Inicializar histórico se não existir na sessão
    if 'history' not in session:
        session['history'] = []
    
    # Inicializar o modo angular (radianos por defeito)
    if 'angle_mode' not in session:
        session['angle_mode'] = 'rad'
    
    # Processar alteração do modo angular se solicitado
    if request.args.get('toggle_angle_mode'):
        if session['angle_mode'] == 'rad':
            session['angle_mode'] = 'deg'
        else:
            session['angle_mode'] = 'rad'
        return redirect(url_for('calculatormain'))
        
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            
            # Avaliar a expressão usando a função segura com NumPy
            computed = safe_eval_expr(expression, session['angle_mode'])

            # Formatar o resultado para exibição
            result = format_result(computed)
            
            # Adicionar o cálculo ao histórico do utilizador
            history_entry = {'expression': expression, 'result': result}
            history = session['history']
            history.insert(0, history_entry)
            # Limitar o histórico aos 20 cálculos mais recentes
            if len(history) > 20:
                history = history[:20]
            session['history'] = history
            
        except Exception as e:
            result = f"Erro: {str(e)}"

    # Preparar os dados para renderização do template
    history = session.get('history', [])
    angle_mode = session.get('angle_mode', 'rad')
    return render_template("calculator.html", result=result, history=history, angle_mode=angle_mode)

@app.route("/toggle_angle_mode")
def toggle_angle_mode():
    """
    Alterna entre modos de ângulo (radianos/graus).
    
    Returns:
        Redirecionamento para a página anterior
    """
    if session.get('angle_mode') == 'rad':
        session['angle_mode'] = 'deg'
    else:
        session['angle_mode'] = 'rad'
    return redirect(request.referrer or '/')

@app.route("/quaternions", methods=["GET", "POST"])
def quaternions():
    """
    Rota da calculadora de quaterniões.
    Gere cálculos específicos de quaterniões e respectivo histórico.
    
    Returns:
        str: Template HTML renderizado com os resultados de quaterniões
    """
    if 'quaternion_history' not in session:
        session['quaternion_history'] = []
        
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            
            # Avaliar a expressão usando a função de parse de quaterniões
            computed = parse_quaternion_expr(expression)
            
            result = str(computed)
            
            # Adicionar o cálculo ao histórico de quaterniões
            history_entry = {'expression': expression, 'result': result}
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
    """
    Rota da calculadora de coquaterniões.
    Gere cálculos específicos de coquaterniões e respectivo histórico.
    
    Returns:
        str: Template HTML renderizado com os resultados de coquaterniões
    """
    if 'coquaternion_history' not in session:
        session['coquaternion_history'] = []
        
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            
            # Usar parse_coquaternion_expr em vez de eval()
            computed = parse_coquaternion_expr(expression)
            
            result = str(computed)
            
            # Adicionar o cálculo ao histórico de coquaterniões
            history_entry = {'expression': expression, 'result': result}
            history = session['coquaternion_history']
            history.insert(0, history_entry)
            if len(history) > 20:
                history = history[:20]
            session['coquaternion_history'] = history
            
        except Exception as e:
            result = f"Erro: {str(e)}"
            
    history = session.get('coquaternion_history', [])
    return render_template("coquaternion.html", result=result, history=history)

@app.route("/clear_history/<calculator_type>")
def clear_history(calculator_type):
    """
    Limpa o histórico de cálculos com base no tipo de calculadora.
    
    Args:
        calculator_type (str): Tipo de calculadora ('standard', 'quaternion', 'coquaternion')
    
    Returns:
        Redirecionamento para a página anterior
    """
    if calculator_type == 'standard':
        session['history'] = []
    elif calculator_type == 'quaternion':
        session['quaternion_history'] = []
    elif calculator_type == 'coquaternion':
        session['coquaternion_history'] = []
    return redirect(request.referrer or '/')

if __name__ == "__main__":
    # Executa a aplicação quando o script é executado directamente
    app.run(debug=True)
    # Para Docker: app.run(debug=False, host='0.0.0.0', port=5000)