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
    
    def sin(self):
        """
        Calcula o seno do quaternião.
        Para q = a + v (onde v é a parte vetorial), temos:
        sin(q) = sin(a) * cosh(|v|) + cos(a) * sinh(|v|) * (v/|v|)
    
        Returns:
            Quaternion: Seno do quaternião
        """
        # Obtém a parte escalar (real) e vetorial
        scalar_part = self.a
        vector_part = Quaternion(0, self.b, self.c, self.d)
        vector_norm = vector_part.norm()
    
        # Trata o caso especial quando a parte vetorial é zero
        if abs(vector_norm) < 1e-15:
            return Quaternion(math.sin(scalar_part), 0, 0, 0)
    
        # Calcula as componentes da fórmula
        sin_a = math.sin(scalar_part)
        cos_a = math.cos(scalar_part)
        cosh_norm = math.cosh(vector_norm)
        sinh_norm = math.sinh(vector_norm)
    
        # Normaliza o vetor
        unit_vector = vector_part * (1.0 / vector_norm)
    
        # Aplica a fórmula
        result = Quaternion(sin_a * cosh_norm, 0, 0, 0) + unit_vector * (cos_a * sinh_norm)
        return result

    def cos(self):
        """
        Calcula o cosseno do quaternião.
        Para q = a + v (onde v é a parte vetorial), temos:
        cos(q) = cos(a) * cosh(|v|) - sin(a) * sinh(|v|) * (v/|v|)
    
        Returns:
            Quaternion: Cosseno do quaternião
        """
        # Obtém a parte escalar (real) e vetorial
        scalar_part = self.a
        vector_part = Quaternion(0, self.b, self.c, self.d)
        vector_norm = vector_part.norm()
    
        # Trata o caso especial quando a parte vetorial é zero
        if abs(vector_norm) < 1e-15:
            return Quaternion(math.cos(scalar_part), 0, 0, 0)
    
        # Calcula as componentes da fórmula
        sin_a = math.sin(scalar_part)
        cos_a = math.cos(scalar_part)
        cosh_norm = math.cosh(vector_norm)
        sinh_norm = math.sinh(vector_norm)
    
        # Normaliza o vetor
        unit_vector = vector_part * (1.0 / vector_norm)
    
        # Aplica a fórmula
        result = Quaternion(cos_a * cosh_norm, 0, 0, 0) - unit_vector * (sin_a * sinh_norm)
        return result

    def tan(self):
        """
        Calcula a tangente do quaternião como sin(q) * cos(q)^-1.
    
        Returns:
            Quaternion: Tangente do quaternião
        """
        cos_q = self.cos()
        sin_q = self.sin()
        return sin_q / cos_q  # Usa o operador / já implementado

    def asin(self):
        """
        Calcula o arco-seno do quaternião usando asin(q) = pi/2 - acos(q).
        """
        pi_half_q = Quaternion(math.pi / 2.0)
        acos_q = self.acos() # Usa a acos definida acima (que pode ter fallback)
        return pi_half_q - acos_q

    def acos(self):
        """
        Calcula o arco-cosseno do quaternião q = s + v.
        Resolve w para q = cos(w), onde w = ws + wv.
        Retorna o valor que corresponde a ws principal [0, pi].
        """
        s = self.a
        vec_v_norm_sq = self.b**2 + self.c**2 + self.d**2
        vec_v_norm = math.sqrt(vec_v_norm_sq)
        q_norm_sq = s**2 + vec_v_norm_sq
        # q_norm = math.sqrt(q_norm_sq) # |q|

        # Caso especial: q é real
        if vec_v_norm < 1e-12: # Praticamente real
            if -1.0 <= s <= 1.0:
                return Quaternion(math.acos(s), 0, 0, 0)
            elif s > 1.0:
                # acos(s) = i * acosh(s)
                # Para quaterniões, -i * acosh(s) se usarmos a fórmula -i*ln(...)
                # Ou, mais diretamente, para um q real > 1, o resultado tem parte imaginária i
                # Usando a definição que w_s=0, |w_v|=acosh(s), wv na direção de i.
                # No entanto, a derivação geral abaixo deve cobrir isso.
                # A definição cos(w_s)cosh|wv| = s, sin(w_s)sinh|wv|=0.
                # Se sin(w_s)=0 => w_s=0 ou pi.
                # Se w_s=0, cosh|wv|=s => |wv|=acosh(s). wv_dir pode ser (1,0,0)
                # return Quaternion(0, math.acosh(s), 0, 0) # acos(x) = i acosh(x) => (0, acosh(x),0,0)
                # A fórmula que deu o resultado esperado não tem esta forma para reais.
                # A fórmula com cos^2(ws) deve ser usada.
                pass # Deixar a fórmula geral tratar
            else: # s < -1.0
                # acos(s) = pi - i * acosh(-s)
                # return Quaternion(math.pi, -math.acosh(-s), 0, 0)
                pass # Deixar a fórmula geral tratar

        # Discriminante da equação quadrática para cos^2(ws)
        # X^2 - (|q|^2+1)X + s^2 = 0
        # discriminante = ( (|q|^2+1)^2 - 4*s^2 )
        # Para o seu exemplo: q=(1,1,-1,2), |q|^2=7, s=1
        # disc = (7+1)^2 - 4*1^2 = 64 - 4 = 60
        discriminant_val = (q_norm_sq + 1)**2 - 4 * s**2

        if discriminant_val < -1e-9: # Pequena tolerância para erros de fp
            # Isto não deve acontecer para quaterniões reais ou "normais".
            # Pode indicar um problema se q_norm_sq for muito pequeno ou s for muito grande.
            # Recorrer à fórmula logarítmica original como fallback ou levantar erro.
            # Para agora, vamos prosseguir, mas isto é um ponto de atenção.
            # Se o discriminante for negativo, sqrt dele é imaginário, cos^2(ws) seria complexo.
            # Isso acontece se q for "muito" não-real de uma certa forma.
            # Ex: se q = 2i, |q|^2=4, s=0. disc = (4+1)^2 - 0 = 25.
            # se q = 0.1i, |q|^2=0.01, s=0. disc = (0.01+1)^2 -0 = 1.01^2
            # Por agora, assumimos que é >= 0
            # Se realmente for negativo, significa que não há solução real para cos^2(ws)
            # e a premissa da derivação pode não se aplicar diretamente, ou w_s é complexo.
            # No entanto, arccos de quaterniões é sempre um quaternião.
            # A fórmula original com logaritmos é geralmente mais robusta para todos os casos.
            # Apenas se o resultado específico for desejado, esta derivação é usada.
            # Se der negativo, vamos usar a implementação original como fallback:
            # print("Alerta: Discriminante negativo em acos, usando fallback logarítmico.")
            neg_i_unit = Quaternion(0, -1, 0, 0)
            one = Quaternion(1, 0, 0, 0)
            q_squared = self * self
            q_squared_minus_one = q_squared - one
            sqrt_term = q_squared_minus_one.sqrt() # Usa a sua sqrt
            temp = self + sqrt_term
            return neg_i_unit * temp.ln() # Usa a sua ln

        # cos_sq_ws = ( (q_norm_sq + 1) - math.sqrt(discriminant_val) ) / 2.0
        # O valor de cos(ws) que corresponde à parte real 1.20639 é sqrt(4 - sqrt(15)) approx 0.3563943
        # (4 - sqrt(15)) approx 0.12701695
        # Com |q|^2 = 7, s = 1:
        # cos_sq_ws = ( (7+1) - sqrt(60) ) / 2.0 = (8 - 2*sqrt(15)) / 2.0 = 4 - sqrt(15)
        # Isto corresponde.
        
        cos_sq_ws_val = ( (q_norm_sq + 1) - math.sqrt(max(0, discriminant_val)) ) / 2.0 # max(0,...) para segurança numérica

        if cos_sq_ws_val < -1e-9 or cos_sq_ws_val > 1.0 + 1e-9:
            # Se cos_sq_ws estiver fora de [0,1], algo está errado ou é um caso especial.
            # Se q é real, e s > 1, cos_sq_ws = 1. Se s < -1, cos_sq_ws = 1.
            # Caso real q=s:
            if vec_v_norm < 1e-12: # É real
                if s > 1.0: # acos(s) = 0 + i acosh(s) ; ou seja, ws=0, |wv|=acosh(s)
                    return Quaternion(0, math.acosh(s),0,0) # Assume que 'i' imaginário mapeia para b
                elif s < -1.0: # acos(s) = pi + i acosh(-s)
                    return Quaternion(math.pi, math.acosh(-s),0,0) # Parte b
                # Se s in [-1,1] já foi tratado
            else: # Não é real e cos_sq_ws está fora de [0,1]. Pode ser problemático.
                # Usar fallback
                # print(f"Alerta: cos_sq_ws = {cos_sq_ws_val} fora de [0,1]. Usando fallback.")
                neg_i_unit = Quaternion(0, -1, 0, 0)
                one = Quaternion(1, 0, 0, 0)
                q_squared = self * self
                q_squared_minus_one = q_squared - one
                sqrt_term = q_squared_minus_one.sqrt()
                temp = self + sqrt_term
                return neg_i_unit * temp.ln()

        # Garantir que o argumento de acos para ws está em [-1, 1]
        # cos_ws_candidate = math.sqrt(max(0, cos_sq_ws_val)) # Isto seria para ws em [0, pi/2]
        # Para o exemplo s=1, cos_ws deve ser 0.35639. s é positivo.
        # A escolha de qual raiz de cos_sq_ws (positiva ou negativa) tomar para cos_ws
        # pode depender de s e vec_v_norm. A convenção é que ws está em [0,pi].

        cos_ws = math.sqrt(max(0, min(1,cos_sq_ws_val))) # Tomar a raiz positiva por agora.
                                                        # ws = acos(cos_ws) estará em [0, pi/2]
                                                        # Isto é uma simplificação.
                                                        # A derivação original para o exemplo deu cos(ws) ~ 0.356, ws ~ 1.206 (que está em [0,pi])

        # Para obter ws no intervalo completo [0, pi], e lidar com o sinal de cos_ws:
        # A ideia é que q_s = cos(w_s) cosh(|w_v|). Como cosh >=1, sgn(q_s) = sgn(cos(w_s))
        # A menos que cosh(|w_v|) seja muito grande e "mascare" o sinal de cos(w_s).
        # A referência para o resultado esperado indica ws ~ 1.20639, então cos(ws) ~ 0.356 é positivo.
        # Nosso s=1 é positivo.

        # Tentativa mais robusta para cos_ws:
        # Se ws é o ângulo principal, cos(ws) e s devem ter sinais correlacionados
        # com cosh(|wv|) >= 1.
        # A solução $4 - \sqrt{15}$ para $\cos^2(w_s)$ é sempre positiva.
        # Então $\cos(w_s)$ pode ser $\pm \sqrt{4-\sqrt{15}}$.
        # Para $s=1$, $\cos(w_s)$ foi $\sqrt{4-\sqrt{15}} \approx 0.35639$.
        
        # Se $q_s = 0$, então $\cos(w_s)=0 \implies w_s = \pi/2$ (se $\cosh(|\vec{w_v}|) \ne 0$).
        if abs(s) < 1e-12 : # Se s é zero
            if q_norm_sq > 1e-12: # Evita q=0
                ws = math.pi / 2.0
                cos_ws = 0.0
            else: # q é zero
                return Quaternion(math.pi / 2.0, 0,0,0) # acos(0) = pi/2
        else:
            # Esta é a parte crítica: determinar cos_ws para que ws esteja em [0,pi]
            # A partir de cos^2(ws), temos duas hipóteses para cos(ws): +/- sqrt(cos_sq_ws_val)
            # Testar qual delas (ou ambas) leva a uma solução consistente para |wv| >= 0.
            # A heurística é que cos_ws geralmente tem o mesmo sinal que s, mas não sempre.
            # Para o exemplo dado, s=1 (positivo), cos_ws foi positivo.
            # Vamos assumir que cos_ws = sqrt(cos_sq_ws_val) por agora.
            # E ws = acos(cos_ws) estará em [0, pi/2].
            # Se o resultado esperado tem ws > pi/2, isto falhará.
            # O resultado esperado tem ws = 1.20639 rad = 69.1 graus, que está em [0,pi/2].

            if cos_sq_ws_val < 1e-12 and abs(s) > 1e-9: # cos_sq_ws_val é quase 0, mas s não é.
                                                        # Ex: q = i. s=0, |q|^2=1. disc=(1+1)^2-0=4. cos_sq_ws=(2-2)/2=0.
                cos_ws = 0.0
                ws = math.pi / 2.0
            elif cos_sq_ws_val >= 1.0 - 1e-9 and abs(s) > 1e-9 : # cos_sq_ws_val é quase 1, mas s não é +/-1
                                                                # Este caso é mais complexo, pode indicar que |wv| é muito pequeno
                if vec_v_norm < 1e-9: # É praticamente real, tratado acima
                    pass # já tratado
                # Se s=0.5, |q|^2=0.25. disc=(0.25+1)^2 - 4*0.25^2 = 1.25^2 - 1 = 1.5625-1=0.5625.
                # cos_sq_ws = (1.25 - sqrt(0.5625))/2 = (1.25-0.75)/2 = 0.25. cos_ws=0.5. ws=acos(0.5)=pi/3.
                # Esta lógica parece ok.
                cos_ws = math.sqrt(min(1,max(0,cos_sq_ws_val)))
                # Se s for negativo, e ws deve estar em [pi/2, pi], então cos_ws deve ser negativo.
                # Ex: acos(-0.5) = 2pi/3. cos(2pi/3) = -0.5.
                # Se s < 0, e a solução para cos_ws é positiva, precisamos inverter o sinal e ajustar ws.
                # Isto está a ficar complicado. A derivação original com ws e |wv| é mais direta.
                # ws = acos( VAL ) onde VAL foi derivado de forma a que ws seja a parte escalar esperada.
                # VAL = sqrt( ( (q_norm_sq + 1) - math.sqrt(discriminant_val) ) / 2.0 ) se q_s >= 0
                # VAL = -sqrt( ( (q_norm_sq + 1) - math.sqrt(discriminant_val) ) / 2.0 ) se q_s < 0 ?
                # Não, o sinal de cos(w_s) é determinado pela equação $q_s = \cos(w_s)\cosh(|\vec{w}_v|)$.
                # Como $\cosh(|\vec{w}_v|) \ge 1$, $\mathrm{sgn}(\cos(w_s)) = \mathrm{sgn}(q_s)$ (a menos que $q_s=0$).
                
                temp_cos_val = math.sqrt(min(1.0, max(0.0, cos_sq_ws_val)))
                if s < 0.0:
                    cos_ws = -temp_cos_val
                else:
                    cos_ws = temp_cos_val
                
                if abs(cos_ws) > 1.0 : # clip
                    cos_ws = math.copysign(1.0, cos_ws)

                ws = math.acos(cos_ws) # ws estará em [0, pi]
            else: # Caso geral, cos_sq_ws_val em (0,1)
                temp_cos_val = math.sqrt(cos_sq_ws_val)
                if s < 0.0 and temp_cos_val > 1e-9 : # Se s é negativo, cos_ws deve ser negativo
                    cos_ws = -temp_cos_val
                else: # s é positivo ou s é zero (ws=pi/2)
                    cos_ws = temp_cos_val
                
                if abs(cos_ws) > 1.0 : # clip
                    cos_ws = math.copysign(1.0, cos_ws)
                ws = math.acos(cos_ws)


        vec_wv_norm = 0.0
        # Calcular |wv|
        if abs(cos_ws) < 1.0 - 1e-9 : # sin(ws) != 0 ; ws não é 0 nem pi
            # Usar sin(ws) = sqrt(1 - cos_ws^2)
            sin_ws = math.sqrt(max(0, 1.0 - cos_ws**2)) # sin_ws é >= 0 pois ws em [0,pi]
            if abs(sin_ws) < 1e-9: # Se sin_ws for zero (ws=0 ou pi)
                if abs(s - cos_ws * 1.0) < 1e-9 : # cosh(0)=1
                    vec_wv_norm = 0.0 # |wv| é zero
                elif abs(s) > 1e-9 : # cos_ws deve ser +/-1 aqui
                    # Este é o caso em que q é real e |s| > 1.
                    # ws=0 => cos_ws=1. q_s = cosh|wv|. |wv|=acosh(q_s).
                    # ws=pi => cos_ws=-1. q_s = -cosh|wv|. |wv|=acosh(-q_s).
                    if abs(ws) < 1e-9 : # ws é 0
                        if s > 1.0 - 1e-9: vec_wv_norm = math.acosh(max(1.0,s))
                        else: vec_wv_norm = 0.0 # Ex: acos(1)=0
                    elif abs(ws - math.pi) < 1e-9 : # ws é pi
                        if s < -1.0 + 1e-9: vec_wv_norm = math.acosh(max(1.0,-s))
                        else: vec_wv_norm = 0.0 # Ex: acos(-1)=pi
                    else: # Situação inesperada
                        # print(f"Alerta: sin_ws perto de zero mas ws não é 0/pi. ws={ws}")
                        return self.acos_log_fallback() # Usar fallback
                else: # s é zero, ws é pi/2, sin_ws é 1. Deveria ter entrado no else.
                    # Este ramo é para quando sin_ws é inesperadamente zero.
                    vec_wv_norm = 0.0
            else: # sin_ws é não-zero
                val_for_asinh = vec_v_norm / sin_ws
                vec_wv_norm = math.asinh(val_for_asinh)
        else: # cos_ws é +/-1 (ws é 0 ou pi) => sin_ws é 0
            # Neste caso, q_s = +/- cosh(|wv|).
            # Se q é real, |vec_v_norm|=0. Então |wv| deve ser 0.
            # Se q não é real, mas ws é 0 ou pi, então a parte vetorial deve ser 0.
            # Isso significa que vec_v_norm deveria ter sido zero.
            if vec_v_norm < 1e-9: # Praticamente real, |wv| é 0
                vec_wv_norm = 0.0
            else: # cos_ws é +/-1 mas vec_v_norm não é zero. Inconsistência ou caso limite.
                # Ex: acos(1+0.001i). |q|^2~1, s~1. cos_sq_ws~1. cos_ws~1. ws~0. sin_ws~0.
                # Neste caso q_s = cosh(|wv|). |wv|=acosh(q_s).
                # A fórmula com acosh(s/cos_ws) é melhor.
                if abs(cos_ws) > 1e-9: # Evita divisão por zero se cos_ws for zero (já tratado por sin_ws)
                    val_for_acosh = s / cos_ws
                    if val_for_acosh < 1.0 - 1e-9 and val_for_acosh > -1.0 + 1e-9:
                        # Se s/cos_ws estiver em (-1,1), acosh não é real.
                        # Ex: q = 0.5+1000i. s=0.5. |q|^2 é grande. cos_sq_ws é pequeno.
                        # cos_ws é pequeno. ws ~ pi/2.
                        # Este ramo (cos_ws é +/-1) não devia ser atingido para q não-real.
                        # print(f"Alerta: cos_ws= +/-1 mas q não-real. Usando fallback.")
                        return self.acos_log_fallback()
                    elif val_for_acosh < -1.0 -1e-9: # Ex: s=-2, cos_ws=-1. s/cos_ws = 2.
                        vec_wv_norm = math.acosh(max(1.0, -val_for_acosh))
                    else:
                        vec_wv_norm = math.acosh(max(1.0, val_for_acosh))
                else: # cos_ws é zero, ws=pi/2. sin_ws=1. Deveria usar o ramo de asinh.
                    # Este else é para segurança, mas não deve ser comum.
                    vec_wv_norm = 0.0


        # Parte vetorial
        res_vec_b, res_vec_c, res_vec_d = 0,0,0
        if vec_v_norm > 1e-9 and abs(vec_wv_norm) > 1e-9: # Evitar divisão por zero e mult por zero
            factor = -vec_wv_norm / vec_v_norm
            res_vec_b = self.b * factor
            res_vec_c = self.c * factor
            res_vec_d = self.d * factor

        return Quaternion(ws, res_vec_b, res_vec_c, res_vec_d)

    def atan(self):
        """
        Calcula o arco-tangente do quaternião usando a fórmula:
        atan(q) = (-i/2) * ln((i+q)^-1 * (i-q))
        Garante que as operações são feitas na ordem correta para quaterniões.

        Returns:
            Quaternion: Arco-tangente do quaternião
        """
        i_q = Quaternion(0, 1, 0, 0)       # Unidade i como Quaternião
        neg_i_half_q = Quaternion(0, -0.5, 0, 0) # -i/2 como Quaternião

        term_sum = i_q + self         # (i+q)
        term_diff = i_q - self        # (i-q)

        # Verificar se (i+q) é zero antes de inverter
        norm_sq_sum = term_sum.norm_squared()
        if abs(norm_sq_sum) < 1e-15:
            # Se i+q é zero, q = -i. atan(-i) é problemático (infinito).
            # Poderíamos retornar um valor grande ou levantar um erro.
            # Vamos levantar um erro por clareza.
            raise ValueError("atan indefinido para q = -i")

        term_sum_inv = term_sum.inverse() # (i+q)^-1

        log_argument = term_sum_inv * term_diff # (i+q)^-1 * (i-q)

        # Usa a função ln da própria classe
        ln_val = log_argument.ln()

        return neg_i_half_q * ln_val
    
    def ln(self):
        """
        Calcula o logaritmo natural (ln) do quaternião.
        Para q = |q|*e^(v*θ), onde v é um vetor unitário e θ é um ângulo:
        ln(q) = ln(|q|) + v*θ, onde θ = arccos(scalar_part / norm)
    
        Returns:
            Quaternion: Logaritmo natural do quaternião
        """
        norm = self.norm()
    
        # Verificar se o quaternião é aproximadamente zero
        if abs(norm) < 1e-15:
            raise ValueError("Logaritmo de quaternião (aproximadamente) nulo")
    
        # Obter a parte escalar e vetorial
        scalar_part = self.a
        vector_part = Quaternion(0, self.b, self.c, self.d)
        vector_norm = vector_part.norm()
    
        # Se a parte vetorial é aproximadamente zero, é essencialmente um número real
        if abs(vector_norm) < 1e-15:
            if scalar_part >= 0:
                return Quaternion(math.log(norm), 0, 0, 0)
            else:
                # Para números reais negativos, ln(q) = ln(|q|) + π*i
                return Quaternion(math.log(norm), math.pi, 0, 0)
    
        # Calcular o ângulo θ
        # θ = arccos(scalar_part / norm)
        theta = math.acos(scalar_part / norm)
    
        # Obter o vetor unitário v = vector_part / vector_norm
        unit_vector = vector_part * (1.0 / vector_norm)
    
        # Calcular ln(q) = ln(|q|) + v*θ
        return Quaternion(math.log(norm), 0, 0, 0) + unit_vector * theta

    def sinh(self):
        """
        Calcula o seno hiperbólico do quaternião.
        sinh(q) = (e^q - e^(-q)) / 2

        Returns:
            Quaternion: Seno hiperbólico do quaternião
        """
        # Implementação baseada na definição com exponenciais
        exp_q = self.exp()
        exp_neg_q = (self * -1).exp()
        return (exp_q - exp_neg_q) * 0.5

    def cosh(self):
        """
        Calcula o cosseno hiperbólico do quaternião.
        cosh(q) = (e^q + e^(-q)) / 2
    
        Returns:
            Quaternion: Cosseno hiperbólico do quaternião
        """
        # Implementação baseada na definição com exponenciais
        exp_q = self.exp()
        exp_neg_q = (self * -1).exp()
        return (exp_q + exp_neg_q) * 0.5

    def tanh(self):
        """
        Calcula a tangente hiperbólica do quaternião.
        tanh(q) = sinh(q) / cosh(q)
    
        Returns:
            Quaternion: Tangente hiperbólica do quaternião
        """
        # Implementação baseada na relação entre sinh e cosh
        sinh_q = self.sinh()
        cosh_q = self.cosh()
        return sinh_q / cosh_q

    def asinh(self):
        """
        Calcula o arco-seno hiperbólico do quaternião.
        asinh(q) = ln(q + sqrt(q² + 1))
    
        Returns:
            Quaternion: Arco-seno hiperbólico do quaternião
        """
        one = Quaternion(1, 0, 0, 0)
        q_squared = self * self
        return (self + (q_squared + one).sqrt()).ln()

    def acosh(self):
        """
        Calcula o arco-cosseno hiperbólico do quaternião.
        Para valores reais, verifica o domínio (x ≥ 1).
        Para quaterniões gerais, usa a fórmula acosh(q) = ln(q + sqrt(q² - 1))

        Returns:
            Quaternion: Arco-cosseno hiperbólico do quaternião
        """
        # Para quaterniões reais puros com valor < 1, usa a extensão complexa
        if abs(self.b) < 1e-15 and abs(self.c) < 1e-15 and abs(self.d) < 1e-15 and self.a < 1:
            # Para valores reais < 1, acosh(x) tem uma parte imaginária
            # acosh(x) = ln(x + sqrt(x² - 1)) = ln(x + i*sqrt(1-x²))
            x = self.a
            return Quaternion(0, math.acos(x)).acosh()  # Converte para quaternião com parte imaginária
    
        # Para outros casos, usa a fórmula normal
        one = Quaternion(1, 0, 0, 0)
        q_squared = self * self
        return (self + (q_squared - one).sqrt()).ln()

    def atanh(self):
        """
        Calcula o arco-tangente hiperbólico do quaternião.
        atanh(q) = (1/2) * ln((1+q)/(1-q))
    
        Returns:
            Quaternion: Arco-tangente hiperbólico do quaternião
        """
        one = Quaternion(1, 0, 0, 0)
        half = 0.5
    
        numerator = one + self
        denominator = one - self
    
        return (numerator / denominator).ln() * half

    def exp(self):
        """
        Calcula a exponencial do quaternião.
        Para q = a + v (onde v é a parte vetorial), temos:
        exp(q) = exp(a) * [cos(|v|) + (v/|v|) * sin(|v|)]
    
        Returns:
            Quaternion: Exponencial do quaternião
        """
        # Obtém a parte escalar (real) e vetorial
        scalar_part = self.a
        vector_part = Quaternion(0, self.b, self.c, self.d)
        vector_norm = vector_part.norm()
    
        # Calcula e^a
        exp_a = math.exp(scalar_part)
    
        # Trata o caso especial quando a parte vetorial é zero
        if abs(vector_norm) < 1e-15:
            return Quaternion(exp_a, 0, 0, 0)
    
        # Calcula as componentes da fórmula
        cos_norm = math.cos(vector_norm)
        sin_norm = math.sin(vector_norm)
    
        # Normaliza o vetor
        unit_vector = vector_part * (1.0 / vector_norm)
    
        # Aplica a fórmula
        return Quaternion(exp_a * cos_norm, 0, 0, 0) + unit_vector * (exp_a * sin_norm)

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
        'acosh': lambda q: q.acosh() if isinstance(q, Quaternion) else (math.acosh(q) if q >= 1 else Quaternion(0).acosh()),
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