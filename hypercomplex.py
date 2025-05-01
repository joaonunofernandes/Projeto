"""
Implementação de operações com números hipercomplexos:
- Quaterniões: Extensão dos números complexos com 4 dimensões (1, i, j, k)

Este módulo será importado pelo app.py principal.
"""
import re
import math
import numpy as np

class Quaternion:
    """
    Classe que representa um quaternião q = a + bi + cj + dk
    onde a, b, c, d são números reais e i, j, k são unidades imaginárias
    
    Regras de multiplicação:
    i² = j² = k² = ijk = -1
    ij = k, ji = -k
    jk = i, kj = -i
    ki = j, ik = -j
    """

    def __init__(self, a=0, b=0, c=0, d=0):
        """
        Inicializa um quaternião com componentes a, b, c, d
        
        Args:
            a (float): Parte real (escalar)
            b (float): Coeficiente de i
            c (float): Coeficiente de j
            d (float): Coeficiente de k
        """
        self.a = float(a)  # Parte real (escalar)
        self.b = float(b)  # Coeficiente de i
        self.c = float(c)  # Coeficiente de j
        self.d = float(d)  # Coeficiente de k

    @classmethod
    def from_string(cls, s):
        """
        Cria um quaternião a partir de uma string
        
        Args:
            s (str): String representando o quaternião (ex: "1 + 2i + 3j + 4k")
            
        Returns:
            Quaternion: Objeto quaternião
        """
        # Inicializa os componentes
        a, b, c, d = 0, 0, 0, 0
        
        # Trata o caso de string vazia
        if not s or s.isspace():
            return cls(0, 0, 0, 0)
            
        # Trata o caso de um número simples (apenas escalar)
        try:
            if '+' not in s and '-' not in s[1:] and 'i' not in s and 'j' not in s and 'k' not in s:
                return cls(float(s), 0, 0, 0)
        except (ValueError, IndexError):
            pass
            
        # Remove espaços e substitui - por +-
        s = s.replace(' ', '').replace('-', '+-')
        if s.startswith('+'):
            s = s[1:]
            
        # Separa os termos
        parts = s.split('+')
        
        for part in parts:
            if not part:  # Ignora termos vazios
                continue
                
            # Verifica se tem unidade imaginária
            if 'i' in part:
                if part == 'i':
                    b = 1
                elif part == '-i':
                    b = -1
                else:
                    b = float(part.replace('i', ''))
            elif 'j' in part:
                if part == 'j':
                    c = 1
                elif part == '-j':
                    c = -1
                else:
                    c = float(part.replace('j', ''))
            elif 'k' in part:
                if part == 'k':
                    d = 1
                elif part == '-k':
                    d = -1
                else:
                    d = float(part.replace('k', ''))
            else:
                # É a parte real
                try:
                    a = float(part)
                except ValueError:
                    # Ignora partes que não podem ser convertidas para float
                    pass
                
        return cls(a, b, c, d)
    
    def __add__(self, other):
        """
        Soma dois quaterniões
        
        Args:
            other (Quaternion): Outro quaternião
            
        Returns:
            Quaternion: Resultado da soma
        """
        if isinstance(other, (int, float)):
            # Soma com escalar
            return Quaternion(self.a + other, self.b, self.c, self.d)
        else:
            # Soma componente a componente
            return Quaternion(
                self.a + other.a,
                self.b + other.b,
                self.c + other.c,
                self.d + other.d
            )

    def __radd__(self, other):
        """Soma à direita com escalar"""
        return self.__add__(other)
    
    def __sub__(self, other):
        """
        Subtração de quaterniões
        
        Args:
            other (Quaternion): Outro quaternião
            
        Returns:
            Quaternion: Resultado da subtração
        """
        if isinstance(other, (int, float)):
            # Subtração com escalar
            return Quaternion(self.a - other, self.b, self.c, self.d)
        else:
            # Subtração componente a componente
            return Quaternion(
                self.a - other.a,
                self.b - other.b,
                self.c - other.c,
                self.d - other.d
            )
        
    def __rsub__(self, other):
        """Subtração à direita com escalar"""
        return Quaternion(other - self.a, -self.b, -self.c, -self.d)
    
    def __mul__(self, other):
        """
        Multiplicação de quaterniões
        
        Args:
            other (Quaternion ou escalar): Outro quaternião ou número escalar
            
        Returns:
            Quaternion: Resultado da multiplicação
        """
        if isinstance(other, (int, float)):
            # Multiplicação por escalar
            return Quaternion(
                self.a * other,
                self.b * other,
                self.c * other,
                self.d * other
            )
        else:
            # Multiplicação de quaterniões usando a regra de Hamilton
            a = self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d
            b = self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c
            c = self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b
            d = self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a
            
            return Quaternion(a, b, c, d)
        
    def __rmul__(self, other):
        """Multiplicação à direita com escalar"""
        if isinstance(other, (int, float)):
            return Quaternion(
                self.a * other,
                self.b * other,
                self.c * other,
                self.d * other
            )
        return NotImplemented
    
    def __truediv__(self, other):
        """
        Divisão de quaterniões
        
        Args:
            other (Quaternion ou escalar): Outro quaternião ou número escalar
            
        Returns:
            Quaternion: Resultado da divisão
        """
        if isinstance(other, (int, float)):
            # Divisão por escalar
            if other == 0:
                raise ZeroDivisionError("Divisão por zero")
            
            return Quaternion(
                self.a / other,
                self.b / other,
                self.c / other,
                self.d / other
            )
        else:
            # Divisão por quaternião: q1 / q2 = q1 * (q2^-1)
            return self * other.inverse()
        
    def __rtruediv__(self, other):
        """Divisão à direita por escalar"""
        if isinstance(other, (int, float)):
            # other / self = other * (self^-1)
            return other * self.inverse()
        return NotImplemented
    
    def conjugate(self):
        """
        Conjugado do quaternião: q* = a - bi - cj - dk
        
        Returns:
            Quaternion: Conjugado do quaternião
        """
        return Quaternion(self.a, -self.b, -self.c, -self.d)
    
    def norm_squared(self):
        """
        Norma ao quadrado: |q|^2 = a^2 + b^2 + c^2 + d^2
        
        Returns:
            float: Norma ao quadrado
        """
        return self.a**2 + self.b**2 + self.c**2 + self.d**2
    
    def norm(self):
        """
        Norma (magnitude): |q| = sqrt(a^2 + b^2 + c^2 + d^2)
        
        Returns:
            float: Norma do quaternião
        """
        return math.sqrt(self.norm_squared())
    
    def vectorial(self):
        """
        Parte vetorial do quaternião: bi + cj + dk
        
        Returns:
            Quaternion: Parte vetorial do quaternião
        """
        return Quaternion(0, self.b, self.c, self.d)
    
    def real(self):
        """
        Parte real do quaternião: a
        
        Returns:
            Quaternion: Parte real como quaternião
        """
        return Quaternion(self.a, 0, 0, 0)
    
    def inverse(self):
        """
        Inverso do quaternião: q^-1 = conj(q) / |q|^2
        
        Returns:
            Quaternion: Inverso do quaternião
        
        Raises:
            ZeroDivisionError: Se o quaternião for nulo
        """
        norm_sq = self.norm_squared()
        if norm_sq == 0:
            raise ZeroDivisionError("Inverso de quaternião nulo")
            
        conj = self.conjugate()
        return Quaternion(
            conj.a / norm_sq,
            conj.b / norm_sq,
            conj.c / norm_sq,
            conj.d / norm_sq
        )
    
    def normalize(self):
        """
        Normaliza o quaternião (magnitude 1)
        
        Returns:
            Quaternion: Quaternião normalizado
            
        Raises:
            ZeroDivisionError: Se o quaternião for nulo
        """
        norm = self.norm()
        if norm == 0:
            raise ZeroDivisionError("Normalização de quaternião nulo")
            
        return Quaternion(
            self.a / norm,
            self.b / norm,
            self.c / norm,
            self.d / norm
        )
    
    def __str__(self):
        """
        Representação em string do quaternião
        
        Returns:
            str: Representação do quaternião no formato "a + bi + cj + dk"
        """
        result = []
        
        # Adiciona a parte real se não for zero ou se é o único componente
        if self.a != 0 or (self.b == 0 and self.c == 0 and self.d == 0):
            result.append(f"{self.a}")
        
        # Adiciona o termo i
        if self.b != 0:
            if self.b == 1:
                result.append("i")
            elif self.b == -1:
                result.append("-i")
            else:
                result.append(f"{self.b}i")
        
        # Adiciona o termo j
        if self.c != 0:
            if self.c == 1:
                result.append("j")
            elif self.c == -1:
                result.append("-j")
            else:
                result.append(f"{self.c}j")
        
        # Adiciona o termo k
        if self.d != 0:
            if self.d == 1:
                result.append("k")
            elif self.d == -1:
                result.append("-k")
            else:
                result.append(f"{self.d}k")
        
        # Junta os termos com sinal de adição
        if not result:
            return "0"
            
        first = result[0]
        rest = result[1:]
        
        # Substitui sinais negativos por subtração
        processed_rest = []
        for term in rest:
            if term.startswith('-'):
                processed_rest.append(f"- {term[1:]}")
            else:
                processed_rest.append(f"+ {term}")
                
        return first + ' ' + ' '.join(processed_rest)
        # Isso cria uma representação mais legível como "a - b + c" em vez de "a + -b + c"
    
    def __repr__(self):
        """Representação detalhada do objeto"""
        return f"Quaternion({self.a}, {self.b}, {self.c}, {self.d})"

def parse_quaternion_expr(expression):
    """
    Parse e avalia expressões com quaterniões, suportando expressões 
    complexas com múltiplos níveis de operações básicas (sem exponenciação)
    
    Args:
        expression (str): Expressão a ser avaliada
        
    Returns:
        Quaternion: Resultado da expressão
    """

    # Verifica se a expressão usa funções como real(), vectorial(), etc.
    func_pattern = r'(\w+)\((.*)\)'
    match_func = re.match(func_pattern, expression.strip())
    
    if match_func:
        func_name = match_func.group(1)
        inner_expr = match_func.group(2)
        
        # Funções especiais que precisam de processamento especial
        if func_name in ['real', 'vectorial', 'conjugate', 'norm']:
            # Avalia primeiro a expressão interna como um quaternião
            try:
                # Tenta avaliar a expressão interna diretamente
                inner_result = parse_quaternion_expr(inner_expr)
            except Exception:
                # Se falhar, tenta converter para um quaternião
                try:
                    inner_result = Quaternion.from_string(inner_expr)
                except Exception as e:
                    raise ValueError(f"Erro ao avaliar a expressão interna '{inner_expr}': {str(e)}")
            
            # Aplica a função apropriada ao resultado
            if func_name == 'real':
                return inner_result.real()
            elif func_name == 'vectorial':
                return inner_result.vectorial()
            elif func_name == 'conjugate':
                return inner_result.conjugate()
            elif func_name == 'norm':
                return Quaternion(inner_result.norm(), 0, 0, 0)
    
    # Substitui símbolos matemáticos por seus equivalentes em Python
    expression = expression.replace('×', '*')
    expression = expression.replace('÷', '/')
    
    # Pré-processamento: verifica se a expressão já contém uma construção de Quaternion explícita
    if re.search(r'Quaternion\s*\(', expression):
        # Se já contém, não aplicamos as substituições para evitar conflitos
        pass
    else:
        # Primeiro, preserva expressões com parênteses para não interferir com o próximo passo
        # Extrai todos os grupos de parênteses, incluindo aninhados, de forma recursiva
        def extract_parens(expr):
            # Encontra o parêntese de abertura mais à esquerda
            open_idx = expr.find('(')
            if open_idx == -1:
                return expr, []  # Sem parênteses, retorna a expressão original
            
            # Contador para acompanhar parênteses aninhados
            parens_count = 1
            close_idx = open_idx + 1
            
            # Encontra o parêntese de fechamento correspondente
            while close_idx < len(expr) and parens_count > 0:
                if expr[close_idx] == '(':
                    parens_count += 1
                elif expr[close_idx] == ')':
                    parens_count -= 1
                close_idx += 1
                
            if parens_count > 0:
                # Parênteses não balanceados, retorna a expressão original
                return expr, []
                
            # Extrai o grupo completo incluindo parênteses
            close_idx -= 1  # Ajusta para o índice correto do parêntese de fechamento
            paren_group = expr[open_idx:close_idx+1]
            
            # Substitui o grupo por um placeholder
            placeholder = f"__PAREN_{len(extracted_groups)}__"
            processed_expr = expr[:open_idx] + placeholder + expr[close_idx+1:]
            
            # Adiciona o grupo à lista
            extracted_groups.append(paren_group)
            
            # Continua processando recursivamente
            return extract_parens(processed_expr)
        
        # Lista para armazenar os grupos extraídos
        extracted_groups = []
        
        # Extrai todos os grupos de parênteses recursivamente
        processed_expr, _ = extract_parens(expression)
        while processed_expr != expression:
            expression = processed_expr
            processed_expr, _ = extract_parens(expression)
        
        # Processamento em duas fases:
        # Fase 1: Substitui unidades i, j, k fora dos parênteses
        # Esta parte lida com expressões como "2*i + j"
        expr_without_parens = expression
        for i, group in enumerate(extracted_groups):
            expr_without_parens = expr_without_parens.replace(f"__PAREN_{i}__", "")
            
        # Substitui i, j, k isolados na parte sem parênteses
        expr_without_parens = re.sub(r'(\d+)i', r'Quaternion(0, \1, 0, 0)', expr_without_parens)
        expr_without_parens = re.sub(r'(\d+)j', r'Quaternion(0, 0, \1, 0)', expr_without_parens)
        expr_without_parens = re.sub(r'(\d+)k', r'Quaternion(0, 0, 0, \1)', expr_without_parens)
        expr_without_parens = re.sub(r'(?<![a-zA-Z0-9_])i(?![a-zA-Z0-9_])', r'Quaternion(0, 1, 0, 0)', expr_without_parens)
        expr_without_parens = re.sub(r'(?<![a-zA-Z0-9_])j(?![a-zA-Z0-9_])', r'Quaternion(0, 0, 1, 0)', expr_without_parens)
        expr_without_parens = re.sub(r'(?<![a-zA-Z0-9_])k(?![a-zA-Z0-9_])', r'Quaternion(0, 0, 0, 1)', expr_without_parens)
        
        # Fase 2: Processa os grupos entre parênteses
        # Alguns grupos podem ter quaterniões, outros são apenas operações aritméticas
        processed_groups = []
        
        for group in extracted_groups:
            # Remove os parênteses para processar o conteúdo
            content = group[1:-1]
            
            # Verifica se o conteúdo contém i, j ou k (indicadores de quaterniões)
            if re.search(r'[ijk]', content):
                # Substitui padrões quaterniões
                content = re.sub(r'(\d+)i', r'Quaternion(0, \1, 0, 0)', content)
                content = re.sub(r'(\d+)j', r'Quaternion(0, 0, \1, 0)', content)
                content = re.sub(r'(\d+)k', r'Quaternion(0, 0, 0, \1)', content)
                content = re.sub(r'(?<![a-zA-Z0-9_])i(?![a-zA-Z0-9_])', r'Quaternion(0, 1, 0, 0)', content)
                content = re.sub(r'(?<![a-zA-Z0-9_])j(?![a-zA-Z0-9_])', r'Quaternion(0, 0, 1, 0)', content)
                content = re.sub(r'(?<![a-zA-Z0-9_])k(?![a-zA-Z0-9_])', r'Quaternion(0, 0, 0, 1)', content)
            
            # Adiciona o conteúdo processado com parênteses
            processed_groups.append('(' + content + ')')
        
        # Reconstrói a expressão substituindo os placeholders pelos grupos processados
        for i, group in enumerate(processed_groups):
            expression = expression.replace(f"__PAREN_{i}__", group)
    
    # Cria um ambiente seguro para avaliar a expressão
    # Adiciona as classes e funções necessárias
    safe_env = {
        'Quaternion': Quaternion,
        'math': math,
        'pi': math.pi,
        'e': math.e,
        're': re,
        'conjugate': lambda q: q.conjugate(),
        'norm': lambda q: q.norm(),
        'vectorial': lambda q: q.vectorial(),
        'real': lambda q: q.real()
    }
    
    try:
        # Tenta avaliar a expressão
        result = eval(expression, {"__builtins__": {}}, safe_env)
        # O parâmetro {"__builtins__": {}} bloqueia acesso às funções built-in do Python por segurança
        
        # Verifica se o resultado é um quaternião
        if not isinstance(result, Quaternion):
            # Converte para quaternião se for um número
            if isinstance(result, (int, float, complex)):
                if isinstance(result, complex):
                    return Quaternion(result.real, result.imag, 0, 0)
                else:
                    return Quaternion(result)
            else:
                raise ValueError(f"Resultado deve ser um quaternião")
        
        return result
    except Exception as e:
        # Se ocorrer um erro, tenta interpretar a expressão como um quaternião diretamente
        try:
            return Quaternion.from_string(expression)
        except:
            # Se isso também falhar, propaga o erro original
            raise ValueError(f"Erro ao avaliar expressão: {str(e)}")
