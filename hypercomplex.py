"""
Implementação de operações com números hipercomplexos:
- Quaterniões: Extensão dos números complexos com 4 dimensões (1, i, j, k)

Este módulo será importado pelo app.py principal.
"""
import re
import math
import cmath # Adicionar esta importação
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
        elif s.startswith('+-'): # Garante que o sinal negativo inicial é tratado corretamente
            s = '-' + s[2:] # Mantém o sinal negativo inicial
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
                        # Tratamento para frações como "3/5i"
                        if '/' in part:
                            num_part = part.replace('i', '')
                            num, denom = num_part.split('/')
                            val = float(num) / float(denom)
                        else:
                            val = float(part.replace('i', ''))
                    except ValueError:
                        raise ValueError(f"Componente inválido para i: '{part}'")
                b += -val if is_negative else val
            elif 'j' in part:
                if part == 'j':
                    pass # val já é 1
                else:
                    try:
                        # Tratamento para frações como "3/5j"
                        if '/' in part:
                            num_part = part.replace('j', '')
                            num, denom = num_part.split('/')
                            val = float(num) / float(denom)
                        else:
                            val = float(part.replace('j', ''))
                    except ValueError:
                        raise ValueError(f"Componente inválido para j: '{part}'")
                c += -val if is_negative else val
            elif 'k' in part:
                if part == 'k':
                    pass # val já é 1
                else:
                    try:
                        # Tratamento para frações como "3/5k"
                        if '/' in part:
                            num_part = part.replace('k', '')
                            num, denom = num_part.split('/')
                            val = float(num) / float(denom)
                        else:
                            val = float(part.replace('k', ''))
                    except ValueError:
                        raise ValueError(f"Componente inválido para k: '{part}'")
                d += -val if is_negative else val
            else:
                # É a parte real
                try:
                    # Tratamento para frações como "3/5"
                    if '/' in part:
                        num, denom = part.split('/')
                        val = float(num) / float(denom)
                    else:
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
        Divisão à Direita (DivR): self / other. Calcula self * other^-1.
        Este é o comportamento padrão para o operador '/'.

        Args:
            other (Quaternião ou escalar): O divisor (q1).

        Retorna:
            Quaternião: Resultado da divisão à direita self * other.inverse() (q2 * q1^-1).
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
        Divisão à Direita (DivR) por self: other / self. Calcula other * self^-1.
        Chamado quando o operando esquerdo não suporta __truediv__ com Quaternião.

        Args:
            other (escalar ou complexo): O dividendo (q2).

        Retorna:
            Quaternião: Resultado da divisão à direita other * self.inverse() (q2 * q1^-1).
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

    def left_division(self, other):
        """
        Divisão à Esquerda (DivL) de self por other: other^-1 * self.
        Calcula o resultado 'x' para a equação: other * x = self.

        Args:
            other (Quaternião ou escalar): O divisor (q1), que multiplica pela esquerda na equação other * x = self.

        Retorna:
            Quaternião: O resultado da divisão à esquerda other.inverse() * self (q1^-1 * q2).
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
    
    def arg(self):
        """
        Calcula o argumento do quaternião, que é o ângulo em radianos entre a parte real
        e a parte vetorial. Para um quaternião q = a + bi + cj + dk, o argumento é
        definido como arccos(a/|q|), onde |q| é a norma do quaternião.
        
        Para quaterniões puramente reais positivos, o argumento é 0.
        Para quaterniões puramente reais negativos, o argumento é π.
        Para quaterniões nulos, o argumento é indefinido (retorna 0).
        
        Returns:
            float: O argumento do quaternião em radianos.
        """
        norm = self.norm()
    
        # Se o quaternião for aproximadamente nulo, o argumento é indefinido
        # Por convenção, retornamos 0
        epsilon = 1e-15
        if abs(norm) < epsilon:
            return 0.0
    
        # Calcula o ângulo entre a parte real e o quaternião completo
        # arccos(a/|q|) onde a é a parte real e |q| é a norma
        cos_theta = self.a / norm
    
        # Garante que o valor está no domínio válido de arccos [-1, 1]
        cos_theta = max(-1.0, min(1.0, cos_theta))
    
        return math.acos(cos_theta)
    
    def _apply_complex_func_to_quaternion(self, cmath_function):
        """
        Método auxiliar para aplicar uma função complexa (de cmath) a um quaternião.
        Se q = s + v, calcula f(s + i*||v||) = Ac + i*Bc.
        O resultado do quaternião é Ac + (Bc/||v||)*v.
        Se ||v|| é zero, trata q como um escalar s. Se f(s) é complexo (ex: log(-1)),
        o resultado é um quaternião com parte b não nula (Ac + Bc*i + 0j + 0k).
        """
        s = self.a
        vb, vc, vd = self.b, self.c, self.d
        norm_v_sq = vb**2 + vc**2 + vd**2
        epsilon = 1e-15  # Tolerância para zero

        if norm_v_sq < epsilon**2:  # Parte vetorial é praticamente zero, q é um escalar s
            # Usar cmath para o caso escalar para lidar consistentemente com resultados complexos
            # (ex: cmath.log(-1) = pi*j, cmath.acos(2) tem parte imaginária)
            complex_res_scalar = cmath_function(complex(s, 0.0))
            # O resultado mapeia para Quaternion(Ac, Bc, 0.0, 0.0)
            return Quaternion(complex_res_scalar.real, complex_res_scalar.imag, 0.0, 0.0)
        else:  # Parte vetorial não é zero
            norm_v = math.sqrt(norm_v_sq)
            z_complex = complex(s, norm_v)
            complex_result = cmath_function(z_complex)
            
            Ac = complex_result.real
            Bc = complex_result.imag
            
            res_a = Ac
            res_b, res_c, res_d = 0.0, 0.0, 0.0 # Inicializa componentes vetoriais
            
            if math.isinf(Bc):
                # Se Bc é infinito, a parte vetorial do resultado é 
                # (sinal de Bc * infinito) * (vetor unitário v/||v||)
                u_b = vb / norm_v
                u_c = vc / norm_v
                u_d = vd / norm_v
                
                # Se o componente do vetor unitário (u_comp) for zero, 
                # o resultado desse componente vetorial é 0.0.
                # Senão, é +/- infinito, dependendo do produto de sinais de Bc e u_comp.
                res_b = math.copysign(float('inf'), Bc * u_b) if abs(u_b) > epsilon else 0.0
                res_c = math.copysign(float('inf'), Bc * u_c) if abs(u_c) > epsilon else 0.0
                res_d = math.copysign(float('inf'), Bc * u_d) if abs(u_d) > epsilon else 0.0
            else:
                # Bc é finito e norm_v é garantidamente não-zero aqui
                factor = Bc / norm_v
                res_b = factor * vb
                res_c = factor * vc
                res_d = factor * vd
                
            return Quaternion(res_a, res_b, res_c, res_d)

    # --- Funções Trigonométricas ---
    def sin(self):
        """Calcula o seno do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.sin)

    def cos(self):
        """Calcula o cosseno do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.cos)

    def tan(self):
        """Calcula a tangente do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.tan)

    def asin(self):
        """Calcula o arco-seno do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.asin)

    def acos(self):
        """Calcula o arco-cosseno do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.acos)

    def atan(self):
        """Calcula o arco-tangente do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.atan)

    # --- Funções Hiperbólicas ---
    def sinh(self):
        """Calcula o seno hiperbólico do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.sinh)

    def cosh(self):
        """Calcula o cosseno hiperbólico do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.cosh)

    def tanh(self):
        """Calcula a tangente hiperbólica do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.tanh)

    def asinh(self):
        """Calcula o arco-seno hiperbólico do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.asinh)

    def acosh(self):
        """Calcula o arco-cosseno hiperbólico do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.acosh)

    def atanh(self):
        """Calcula o arco-tangente hiperbólico do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.atanh)

    # --- Outras Funções ---
    def exp(self):
        """Calcula a exponencial do quaternião."""
        # A implementação original era e^s * (cos(||v||) + (v/||v||) * sin(||v||))
        # Usar o helper produz o mesmo resultado e mantém a consistência.
        return self._apply_complex_func_to_quaternion(cmath.exp)

    def ln(self):
        """Calcula o logaritmo natural (base e) do quaternião."""
        # cmath.log é o logaritmo natural.
        return self._apply_complex_func_to_quaternion(cmath.log)

    def sqrt(self):
        """Calcula a raiz quadrada principal do quaternião."""
        # A raiz quadrada principal (parte real do resultado >= 0).
        # cmath.sqrt fornece este comportamento.
        return self._apply_complex_func_to_quaternion(cmath.sqrt)

    

    def __str__(self):
        """
        Representação em string do quaternião de forma mais legível.
        Formato: a+bi+cj+dk, omitindo termos nulos e simplificando coeficientes 1.
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
                num_str = f"{n:.6f}".rstrip('0').rstrip('.')
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
                # Adiciona sinal sem espaço
                parts.append(f"{sign}{term}")

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
                parts.append(f"{sign}{term}")

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
                parts.append(f"{sign}{term}")

        if not parts:
            return "0"
        else:
            # Junta as partes sem espaços
            result = "".join(parts)
            if result.startswith('+'):
                return result[1:]
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
    
    # Substitui símbolos de raiz quadrada pelo equivalente sqrt
    expression = re.sub(r'√(\d+)', r'sqrt(\1)', expression)
    expression = re.sub(r'√\(([^)]+)\)', r'sqrt(\1)', expression)
    
    # Conversão do formato 2i para 2*i (ou similares)
    expression = re.sub(r'(\d+)([ijk])(?!\w)', r'\1*\2', expression)
    
    # Conversão do formato i2 para i*2 (ou similares)
    expression = re.sub(r'([ijk])(\d+)(?!\w)', r'\1*\2', expression)
    
    # Conversão do formato func(...)i para func(...)*i (ou qualquer letra seguida de i,j,k)
    # Primeiro captura a expressão até um parêntese fechado, seguido de i,j,k
    expression = re.sub(r'(\w+\([^()]*(?:\([^()]*\)[^()]*)*\))([ijk])(?!\w)', r'\1*\2', expression)
    
    # Captura casos onde temos letras como variáveis e constantes (ex: pi, e) seguidas de i,j,k
    expression = re.sub(r'([a-oq-zA-OQ-Z_][a-oq-zA-OQ-Z0-9_]*)([ijk])(?!\w)', r'\1*\2', expression)

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
        'arg': lambda q: q.arg() if isinstance(q, Quaternion) else math.atan2(0, q) if q >= 0 else math.pi,

        # Funções trigonométricas e hiperbólicas
        'sin': lambda q: q.sin() if isinstance(q, Quaternion) else math.sin(q),
        'cos': lambda q: q.cos() if isinstance(q, Quaternion) else math.cos(q),
        'tan': lambda q: q.tan() if isinstance(q, Quaternion) else math.tan(q),
        'asin': lambda q: q.asin() if isinstance(q, Quaternion) else math.asin(q),
        'acos': lambda q: q.acos() if isinstance(q, Quaternion) else math.acos(q),
        'atan': lambda q: q.atan() if isinstance(q, Quaternion) else math.atan(q),
        'sinh': lambda q: q.sinh() if isinstance(q, Quaternion) else math.sinh(q),
        'cosh': lambda q: q.cosh() if isinstance(q, Quaternion) else math.cosh(q),
        'tanh': lambda q: q.tanh() if isinstance(q, Quaternion) else math.tanh(q),
        'asinh': lambda q: q.asinh() if isinstance(q, Quaternion) else math.asinh(q),
        'acosh': lambda q: q.acosh() if isinstance(q, Quaternion) else Quaternion(float(q)).acosh(),
        'atanh': lambda q: q.atanh() if isinstance(q, Quaternion) else math.atanh(q),
        'exp': lambda q: q.exp() if isinstance(q, Quaternion) else math.exp(q),
        'ln': lambda q: q.ln() if isinstance(q, Quaternion) else math.log(q),
        
        # divL(q, p) representa a Divisão à Esquerda: p^-1 * q
        'divL': lambda q, p: (Quaternion(q) if not isinstance(q, Quaternion) else q).left_division(
                            Quaternion(p) if not isinstance(p, Quaternion) else p),
        # divR(q, p) representa a Divisão à Direita: q * p^-1
        'divR': lambda q, p: (Quaternion(q) if not isinstance(q, Quaternion) else q) / 
                            (Quaternion(p) if not isinstance(p, Quaternion) else p),
        # Adicionando suporte ao operador negativo unário para Quaternion
        'neg': lambda q: Quaternion(-q.a, -q.b, -q.c, -q.d) if isinstance(q, Quaternion) else -q,
    }

    try:
        # Avaliar a expressão no ambiente seguro
        # Usar eval é um risco de segurança se a expressão vier de fontes não confiáveis.
        # Aqui, assumimos que vem da interface da calculadora.
        
        # Tratamento especial para operador de negação unária (-) aplicado a funções ou quaterniões
        # Substitui padrões como "-sqrt(...)" por "neg(sqrt(...))"
        
        # Primeiro, protege operações normais como "a-b" substituindo temporariamente
        # Substitui operadores binários por marcadores especiais
        expression = re.sub(r'(\w|\)|\d)\s*-\s*', r'\1 __MINUS__ ', expression)
        
        # Agora substitui as negações unárias
        neg_pattern = r'-(\w+\(.*?\))'
        while re.search(neg_pattern, expression):
            expression = re.sub(neg_pattern, r'neg(\1)', expression)
        
        # Também trata casos como "-i", "-j", "-k" e "-2" diretamente
        expression = re.sub(r'-([ijk])\b', r'neg(\1)', expression)
        expression = re.sub(r'(?<![a-zA-Z0-9_])-(\d+(\.\d+)?)', r'neg(\1)', expression)
        
        # Restaura os operadores binários
        expression = expression.replace('__MINUS__', '-')

        # Tratamento especial para negação de funções divL/divR
        neg_func_pattern = r'-\s*(divL|divR)\s*\('
        if re.search(neg_func_pattern, expression):
            # Precisamos garantir que há um operador antes e depois da substituição
            # Substitui "-divL(" por " - neg(divL(" para garantir espaço para operador
            expression = re.sub(neg_func_pattern, r' - neg(\1(', expression)
            
            # Encontrar todas as ocorrências do padrão e processar cada uma
            for match in re.finditer(r'neg\((divL|divR)\(', expression):
                start_pos = match.end() - 1  # Posição do último parêntese aberto
                count = 1  # Contagem de parênteses (começamos com 1 aberto)
                close_pos = start_pos
                
                # Procurar o parêntese de fechamento correspondente
                for i in range(start_pos + 1, len(expression)):
                    if expression[i] == '(':
                        count += 1
                    elif expression[i] == ')':
                        count -= 1
                        if count == 0:
                            close_pos = i
                            break
                        
                # Inserir o parêntese extra de fechamento após o parêntese correspondente
                if close_pos < len(expression) and count == 0:
                    expression = expression[:close_pos+1] + ')' + expression[close_pos+1:]
        
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