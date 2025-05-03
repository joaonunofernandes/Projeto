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
            # Verifica se contém apenas dígitos, ponto decimal opcional, e sinal opcional no início
            if re.fullmatch(r'-?\d+(\.\d+)?', s.strip()):
                return cls(float(s.strip()), 0, 0, 0)
        except (ValueError, TypeError):
            pass # Continua se não for um número simples

        # Remove espaços e substitui - por +- para facilitar split
        s = s.replace(' ', '').replace('-', '+-')
        if s.startswith('+'):
            s = s[1:]
        elif s.startswith('-'): # Garante que o sinal negativo inicial é tratado corretamente
            pass # Não faz nada, o split tratará disso
        elif not s.startswith('+') and s[0] not in 'ijk' and s[0].isdigit():
            # Adiciona um '+' no início se começar com um número sem sinal
            # (exceto se for só 'i', 'j', 'k')
            # Isto ajuda a separar corretamente o primeiro termo real
            pass # A lógica de split atual deve lidar com isto

        # Separa os termos por '+'
        # Usar lookbehind para não separar em expoentes como 'e+10' se necessário
        parts = re.split(r'(?<!e)\+', s) # Divide por '+' a menos que precedido por 'e'

        for part in parts:
            if not part:  # Ignora termos vazios (resultantes de múltiplos sinais, ex: ++ ou +-)
                continue

            # Trata o sinal negativo remanescente do replace '-' -> '+-'
            is_negative = part.startswith('-')
            if is_negative:
                part = part[1:] # Remove o sinal '-' para processar o resto

            val = 1.0 # Valor padrão do coeficiente se for apenas 'i', 'j', 'k'

            # Verifica se tem unidade imaginária
            if 'i' in part:
                if part == 'i':
                    pass # val já é 1
                else:
                    try:
                        val = float(part.replace('i', ''))
                    except ValueError:
                        raise ValueError(f"Componente inválido para i: '{part}'")
                b += -val if is_negative else val
            elif 'j' in part:
                if part == 'j':
                    pass # val já é 1
                else:
                    try:
                        val = float(part.replace('j', ''))
                    except ValueError:
                        raise ValueError(f"Componente inválido para j: '{part}'")
                c += -val if is_negative else val
            elif 'k' in part:
                if part == 'k':
                    pass # val já é 1
                else:
                    try:
                        val = float(part.replace('k', ''))
                    except ValueError:
                        raise ValueError(f"Componente inválido para k: '{part}'")
                d += -val if is_negative else val
            else:
                # É a parte real
                try:
                    val = float(part)
                    a += -val if is_negative else val
                except ValueError:
                    # Ignora partes que não podem ser convertidas (pode acontecer com erros de input)
                    # Ou levanta um erro mais específico
                    raise ValueError(f"Componente real inválido: '{part}'")

        return cls(a, b, c, d)

    def __add__(self, other):
        """
        Soma dois quaterniões

        Args:
            other (Quaternion ou escalar): Outro quaternião ou número real/complexo

        Returns:
            Quaternion: Resultado da soma
        """
        if isinstance(other, (int, float)):
            # Soma com escalar real
            return Quaternion(self.a + other, self.b, self.c, self.d)
        elif isinstance(other, complex):
            # Soma com escalar complexo (afeta a e b)
            return Quaternion(self.a + other.real, self.b + other.imag, self.c, self.d)
        elif isinstance(other, Quaternion):
            # Soma componente a componente
            return Quaternion(
                self.a + other.a,
                self.b + other.b,
                self.c + other.c,
                self.d + other.d
            )
        else:
            return NotImplemented # Indica que a operação não é suportada para este tipo

    def __radd__(self, other):
        """Soma à direita (other + self)"""
        # A adição é comutativa, mas chamamos __add__ para reutilizar a lógica
        return self.__add__(other)

    def __sub__(self, other):
        """
        Subtração de quaterniões (self - other)

        Args:
            other (Quaternion ou escalar): Outro quaternião ou número real/complexo

        Returns:
            Quaternion: Resultado da subtração
        """
        if isinstance(other, (int, float)):
            # Subtração com escalar real
            return Quaternion(self.a - other, self.b, self.c, self.d)
        elif isinstance(other, complex):
            # Subtração com escalar complexo
            return Quaternion(self.a - other.real, self.b - other.imag, self.c, self.d)
        elif isinstance(other, Quaternion):
            # Subtração componente a componente
            return Quaternion(
                self.a - other.a,
                self.b - other.b,
                self.c - other.c,
                self.d - other.d
            )
        else:
            return NotImplemented

    def __rsub__(self, other):
        """Subtração à direita (other - self)"""
        # q_result = other - self = -(self - other)
        if isinstance(other, (int, float, complex, Quaternion)):
            result = self.__sub__(other) # Calcula self - other
            return result * -1 # Multiplica por -1 para obter other - self
        else:
            return NotImplemented

    def __mul__(self, other):
        """
        Multiplicação de quaterniões (self * other)

        Args:
            other (Quaternion ou escalar): Outro quaternião ou número escalar (real/complexo)

        Returns:
            Quaternion: Resultado da multiplicação
        """
        if isinstance(other, (int, float)):
            # Multiplicação por escalar real
            return Quaternion(
                self.a * other,
                self.b * other,
                self.c * other,
                self.d * other
            )
        elif isinstance(other, complex):
             # Multiplicação por complexo c = x + yi é tratada como q * (x + yi)
             # q * (x + yi + 0j + 0k)
            other_q = Quaternion(other.real, other.imag, 0, 0)
            return self.__mul__(other_q) # Reutiliza a multiplicação de quaterniões
        elif isinstance(other, Quaternion):
            # Multiplicação de quaterniões usando a regra de Hamilton
            a1, b1, c1, d1 = self.a, self.b, self.c, self.d
            a2, b2, c2, d2 = other.a, other.b, other.c, other.d

            a = a1*a2 - b1*b2 - c1*c2 - d1*d2
            b = a1*b2 + b1*a2 + c1*d2 - d1*c2
            c = a1*c2 - b1*d2 + c1*a2 + d1*b2
            d = a1*d2 + b1*c2 - c1*b2 + d1*a2

            return Quaternion(a, b, c, d)
        else:
            return NotImplemented

    def __rmul__(self, other):
        """Multiplicação à direita (other * self)"""
        if isinstance(other, (int, float)):
            # Escalar * self é o mesmo que self * escalar
            return self.__mul__(other)
        elif isinstance(other, complex):
            # Complexo * self: (x + yi) * q
            other_q = Quaternion(other.real, other.imag, 0, 0)
            # A multiplicação não é comutativa, calculamos other_q * self
            return other_q.__mul__(self)
        # Se other for Quaternion, __mul__ já foi tentado.
        # Se chegou aqui e other não é escalar/complexo, não é suportado.
        return NotImplemented

    def __truediv__(self, other):
        """
        Divisão à esquerda (self / other), ou seja, self * other^-1.

        Args:
            other (Quaternion ou escalar): O divisor.

        Returns:
            Quaternion: Resultado da divisão self * other.inverse().
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Divisão de quaternião por escalar zero")
            return self * (1.0 / other)
        elif isinstance(other, complex):
            if other == 0:
                raise ZeroDivisionError("Divisão de quaternião por complexo zero")
            other_q = Quaternion(other.real, other.imag, 0, 0)
            return self * other_q.inverse() # self * other^-1
        elif isinstance(other, Quaternion):
            # inverse() já trata other == 0
            return self * other.inverse() # self * other^-1
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        """
        Divisão à direita por self (other / self), ou seja, other * self^-1.

        Args:
            other (Quaternion ou escalar): O dividendo.

        Returns:
            Quaternion: Resultado da divisão other * self.inverse().
        """
        if isinstance(other, (int, float)):
            # other * self.inverse()
            return other * self.inverse()
        elif isinstance(other, complex):
            # other * self.inverse()
            other_q = Quaternion(other.real, other.imag, 0, 0)
            return other_q * self.inverse()
        # Se 'other' for um Quaternion, __truediv__ já foi tentado no outro objeto.
        return NotImplemented

    def right_divide_by(self, other):
        """
        Calcula a divisão à direita de self por other: other^-1 * self.
        Isto corresponde à solução x para a equação: other * x = self.

        Args:
            other (Quaternion ou escalar): O quaternião pelo qual dividir (fica à esquerda na multiplicação).

        Returns:
            Quaternion: O resultado de other.inverse() * self.
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Divisão à direita por escalar zero")
            # other^-1 * self = (1/other) * self
            inv_other = 1.0 / other
            # Usamos __rmul__ de self implicitamente: inv_other * self
            return inv_other * self
        elif isinstance(other, complex):
            if other == 0:
                raise ZeroDivisionError("Divisão à direita por complexo zero")
            # other^-1 * self
            other_q = Quaternion(other.real, other.imag, 0, 0)
            # inverse() trata other_q == 0
            return other_q.inverse() * self
        elif isinstance(other, Quaternion):
            # other^-1 * self
            # inverse() trata other == 0
            return other.inverse() * self
        else:
            return NotImplemented


    def __pow__(self, exponent):
        """
        Potenciação do quaternião (self ** exponent)

        Args:
            exponent (int): O expoente (atualmente suporta apenas 2)

        Returns:
            Quaternion: Resultado da potenciação

        Raises:
            TypeError: Se o expoente não for um inteiro.
            ValueError: Se o expoente inteiro não for 2 (por agora).
        """
        if not isinstance(exponent, int):
            raise TypeError("Expoente para potenciação de quaternião deve ser inteiro.")

        if exponent == 2:
            return self * self # q^2 = q * q
        elif exponent == 0:
            return Quaternion(1, 0, 0, 0)
        elif exponent == 1:
            return self
        elif exponent < 0:
            # q^-n = (q^-1)^n
            if exponent == -1:
                return self.inverse()
            else:
                # Implementação mais geral (poderia ser otimizada com exp. por quadratura)
                inv = self.inverse()
                res = Quaternion(1, 0, 0, 0)
                for _ in range(abs(exponent)):
                       res = res * inv
                return res
        else: # exponent > 2
            # Implementação mais geral (poderia ser otimizada com exp. por quadratura)
            res = Quaternion(1, 0, 0, 0)
            temp = self
            n = exponent
            # Exponenciação por quadratura (binária)
            while n > 0:
                if n % 2 == 1: # Se o bit atual é 1
                     res = res * temp
                temp = temp * temp # Quadrado para o próximo bit
                n //= 2 # Move para o próximo bit
            return res
            # raise ValueError("Potenciação de quaternião atualmente só suporta expoente 2.")


    def sqrt(self):
        """
        Calcula a raiz quadrada principal do quaternião.

        Retorna a raiz quadrada com a parte real não-negativa.
        Trata casos especiais para q=0 e q sendo um número real negativo.

        Returns:
            Quaternion: A raiz quadrada principal de self.
        """
        norm_q = self.norm()
        epsilon = 1e-15 # Uma pequena tolerância para comparações de ponto flutuante

        # Caso 1: q = 0
        if norm_q < epsilon:
            return Quaternion(0, 0, 0, 0)

        # Caso 2: q é um número real negativo (b=c=d=0, a < 0)
        if abs(self.b) < epsilon and abs(self.c) < epsilon and abs(self.d) < epsilon and self.a < -epsilon:
            # Infinitas raízes da forma sqrt(|a|) * (unit vector)
            # Retornamos uma específica, por exemplo, usando i
            return Quaternion(0, math.sqrt(-self.a), 0, 0)

        # Caso 3: Geral
        # Denominador da fórmula: sqrt(2 * (|q| + a))
        denom = math.sqrt(2 * (norm_q + self.a))

        # Evitar divisão por zero (embora teoricamente coberto pelo Caso 2)
        if abs(denom) < epsilon:
            # Isto pode acontecer se a = -|q|, que é o caso real negativo
            # A lógica acima já deve ter tratado isso, mas por segurança:
            if abs(self.b) < epsilon and abs(self.c) < epsilon and abs(self.d) < epsilon:
                # É um real negativo ou zero
                if self.a < -epsilon:
                    return Quaternion(0, math.sqrt(-self.a), 0, 0) # Real negativo
                else:
                    return Quaternion(0,0,0,0) # Zero
            else:
                # Situação inesperada, talvez erro numérico?
                # Poderia levantar um erro ou tentar uma abordagem numérica diferente.
                # Por agora, retorna o caso real negativo como fallback mais próximo
                # ou levanta um erro. Vamos levantar um erro.
                raise ValueError("Divisão por zero inesperada no cálculo da raiz quadrada do quaternião.")


        # Calcula os componentes da raiz com parte real positiva
        sqrt_a = math.sqrt((norm_q + self.a) / 2)
        mult = 1 / denom # Multiplicador para a parte vetorial = 1 / sqrt(2*(|q|+a))

        sqrt_b = self.b * mult
        sqrt_c = self.c * mult
        sqrt_d = self.d * mult

        return Quaternion(sqrt_a, sqrt_b, sqrt_c, sqrt_d)


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
        norm_sq = self.norm_squared()
        # Adicionar uma pequena verificação para evitar erro em math.sqrt para valores negativos muito pequenos devido a precisão
        if norm_sq < 0 and abs(norm_sq) < 1e-15:
            return 0.0
        return math.sqrt(norm_sq)


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
            Quaternion: Parte real como quaternião (a + 0i + 0j + 0k)
        """
        # Retorna um Quaternião para consistência, embora pudesse retornar só float
        return Quaternion(self.a, 0, 0, 0)

    def inverse(self):
        """
        Inverso do quaternião: q^-1 = conj(q) / |q|^2

        Returns:
            Quaternion: Inverso do quaternião

        Raises:
            ZeroDivisionError: Se o quaternião for nulo (|q|^2 == 0)
        """
        norm_sq = self.norm_squared()
        epsilon = 1e-15 # Tolerância para zero
        if abs(norm_sq) < epsilon:
            raise ZeroDivisionError("Inverso de quaternião (aproximadamente) nulo")

        conj = self.conjugate()
        return Quaternion(
            conj.a / norm_sq,
            conj.b / norm_sq,
            conj.c / norm_sq,
            conj.d / norm_sq
        )

    def normalize(self):
        """
        Normaliza o quaternião (torna-o unitário, com magnitude 1)

        Returns:
            Quaternion: Quaternião normalizado

        Raises:
            ZeroDivisionError: Se o quaternião for (aproximadamente) nulo
        """
        norm = self.norm()
        epsilon = 1e-15 # Tolerância para zero
        if abs(norm) < epsilon:
            raise ZeroDivisionError("Normalização de quaternião (aproximadamente) nulo")

        return Quaternion(
            self.a / norm,
            self.b / norm,
            self.c / norm,
            self.d / norm
        )

    def __str__(self):
        """
        Representação em string do quaternião de forma mais legível.
        Formato: a + bi + cj + dk, omitindo termos nulos e simplificando coeficientes 1.
        """
        parts = []
        epsilon = 1e-12 # Tolerância para considerar um float como zero

        # Formatar com precisão limitada para evitar ".0" desnecessário e lidar com floats
        def format_num(n):
            # Se for muito próximo de um inteiro, mostra como inteiro
            if abs(n - round(n)) < epsilon:
                num_str = str(round(n))
            else:
                # Formata com casas decimais, removendo zeros e ponto final desnecessários
                num_str = f"{n:.4f}".rstrip('0').rstrip('.')
                # Caso especial: evitar resultado "-0"
                if num_str == "-0":
                    return "0"
            return num_str

        # Parte real
        if abs(self.a) > epsilon or (abs(self.b) < epsilon and abs(self.c) < epsilon and abs(self.d) < epsilon):
            parts.append(format_num(self.a))

        # Parte i
        if abs(self.b) > epsilon:
            sign = "+" if self.b > 0 else "-"
            val = abs(self.b)
            term = ""
            if abs(val - 1) < epsilon: # Coeficiente é 1 ou -1
                term = "i"
            else:
                term = f"{format_num(val)}i"

            if not parts: # Se for o primeiro termo
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                # Adiciona sinal e espaço apenas se não for o primeiro termo
                # ou se o sinal for negativo
                parts.append(f"{sign} {term}")

        # Parte j
        if abs(self.c) > epsilon:
            sign = "+" if self.c > 0 else "-"
            val = abs(self.c)
            term = ""
            if abs(val - 1) < epsilon:
                term = "j"
            else:
                term = f"{format_num(val)}j"

            if not parts:
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                parts.append(f"{sign} {term}")

        # Parte k
        if abs(self.d) > epsilon:
            sign = "+" if self.d > 0 else "-"
            val = abs(self.d)
            term = ""
            if abs(val - 1) < epsilon:
                term = "k"
            else:
                term = f"{format_num(val)}k"

            if not parts:
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                parts.append(f"{sign} {term}")

        if not parts:
            return "0"
        else:
            # Junta as partes, tratando o primeiro sinal '+' se existir
            result = " ".join(parts)
            if result.startswith('+ '):
                return result[2:]
            return result


    def __repr__(self):
        """Representação detalhada do objeto para debugging"""
        return f"Quaternion({self.a}, {self.b}, {self.c}, {self.d})"

# Função de Parse (Atualizar safe_env)
def parse_quaternion_expr(expression):
    """
    Parse e avalia expressões com quaterniões, suportando operações básicas,
    potenciação (**), raiz quadrada (sqrt), divisões (divL, divR) e funções específicas.

    Args:
        expression (str): Expressão a ser avaliada

    Returns:
        Quaternion: Resultado da expressão
    """

    # Remover a substituição de '÷' por '/' aqui, pois usaremos divL e divR
    expression = expression.replace('×', '*')
    # expression = expression.replace('÷', '/') # REMOVIDO
    expression = expression.replace('^', '**') # Suporte para ^ como potência

    # Tratamento de funções como sqrt(arg), divL(arg1, arg2), divR(arg1, arg2), etc.
    # Não precisamos mais da lógica específica de match_func aqui,
    # pois o eval com safe_env tratará as funções diretamente.

    # Substitui i, j, k isolados (não como parte de nomes tipo 'sin')
    # Usando limites de palavra (\b) para evitar substituições indesejadas
    expression = re.sub(r'\bi\b', 'Quaternion(0,1,0,0)', expression)
    expression = re.sub(r'\bj\b', 'Quaternion(0,0,1,0)', expression)
    expression = re.sub(r'\bk\b', 'Quaternion(0,0,0,1)', expression)

    # Cria um ambiente seguro para avaliar a expressão
    # Adiciona as classes e funções necessárias
    safe_env = {
        'Quaternion': Quaternion,
        'math': math,
        'pi': math.pi,
        'e': math.e,
        # Funções específicas de Quaterniões (lambda para garantir que chamam o método do objeto)
        'conjugate': lambda q: q.conjugate() if isinstance(q, Quaternion) else Quaternion(q).conjugate(),
        'norm': lambda q: q.norm() if isinstance(q, Quaternion) else abs(q), # Norm de número é abs
        'vectorial': lambda q: q.vectorial() if isinstance(q, Quaternion) else Quaternion(0,0,0,0),
        'real': lambda q: q.real() if isinstance(q, Quaternion) else Quaternion(q),
        'sqrt': lambda q: q.sqrt() if isinstance(q, Quaternion) else math.sqrt(q), # Sqrt de número usa math.sqrt
        'inverse': lambda q: q.inverse() if isinstance(q, Quaternion) else 1.0/q, # Inverso
        'normalize': lambda q: q.normalize() if isinstance(q, Quaternion) else (q/abs(q) if q != 0 else 0), # Normalização
        # divL(q, p) -> q / p -> q * p^-1
        'divL': lambda q, p: q / p, # Usa o __truediv__ da classe Quaternion
        # divR(q, p) -> p^-1 * q
        # O método right_divide_by(self, other) calcula other.inverse() * self
        # Portanto, para calcular p^-1 * q, precisamos chamar q.right_divide_by(p)
        'divR': lambda q, p: q.right_divide_by(p),
    }

    try:
        # Avaliar a expressão no ambiente seguro
        # Usar eval é um risco de segurança se a expressão vier de fontes não confiáveis.
        # Aqui, assumimos que vem da interface da calculadora.
        result = eval(expression, {"__builtins__": {}}, safe_env)
        # O parâmetro {"__builtins__": {}} bloqueia acesso às funções built-in do Python por segurança

        # Verifica se o resultado é um quaternião ou um número (resultante de norm, etc.)
        if isinstance(result, Quaternion):
            return result
        elif isinstance(result, (int, float)):
            # Se for um número real, retorna como um quaternião real
            return Quaternion(result)
        elif isinstance(result, complex):
            # Se for complexo, retorna como quaternião com c=d=0
            return Quaternion(result.real, result.imag)
        else:
            # Tenta converter outros tipos numéricos (como numpy floats)
            try:
                return Quaternion(float(result))
            except (TypeError, ValueError):
                raise ValueError(f"Resultado da expressão é de tipo não suportado: {type(result)}")

    except Exception as e:
        # Se ocorrer um erro na avaliação, pode ser que a expressão original
        # fosse apenas a representação de um quaternião (ex: "1+2i").
        # Tentamos fazer o parse direto.
        original_expression = expression # Guardar a original antes das substituições de i,j,k
        original_expression = original_expression.replace('Quaternion(0,1,0,0)','i') # Reverter para parse
        original_expression = original_expression.replace('Quaternion(0,0,1,0)','j')
        original_expression = original_expression.replace('Quaternion(0,0,0,1)','k')
        try:
            # Tenta parsear a string original (antes das substituições i->Quaternion)
            return Quaternion.from_string(original_expression)
        except Exception as e_parse:
            # Se o parse direto também falhar, propaga o erro original da avaliação
            # ou uma combinação de ambos.
            # Melhora a mensagem de erro para incluir a causa original
            import traceback
            tb_str = traceback.format_exc()
            raise ValueError(f"Erro ao avaliar expressão '{original_expression}'.\nDetalhe: {str(e)}\nParser alternativo falhou: {str(e_parse)}\nTraceback: {tb_str}")