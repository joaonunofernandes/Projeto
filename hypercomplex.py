"""
Implementação de operações com números hipercomplexos:
- Quaterniões: Extensão dos números complexos com 4 dimensões (1, i, j, k)
- Coquaterniões: Quaterniões com métrica de Minkowski

Regras de multiplicação para Quaterniões:
i² = j² = k² = ijk = -1
ij = k, ji = -k
jk = i, kj = -i
ki = j, ik = -j
"""
import re
import math
import cmath 
import numpy as np

class Quaternion:
    """
    Classe que representa um quaternião q = a + bi + cj + dk
    onde a, b, c, d são números reais e i, j, k são unidades imaginárias.
    
    Implementa todas as operações matemáticas básicas e funções especiais
    para quaterniões usando a álgebra de Hamilton.
    """

    def __init__(self, a=0, b=0, c=0, d=0):
        """
        Inicializa um quaternião com componentes a, b, c, d.

        Args:
            a (float): Parte real (escalar)
            b (float): Coeficiente de i
            c (float): Coeficiente de j
            d (float): Coeficiente de k
        """
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)

    @classmethod
    def from_string(cls, s):
        """
        Cria um quaternião a partir de uma string.
        Suporta formatos como "1 + 2i + 3j + 4k", "2i", "3+4j", etc.

        Args:
            s (str): String representando o quaternião

        Returns:
            Quaternion: Objecto quaternião

        Raises:
            ValueError: Se a string não puder ser interpretada
        """
        a, b, c, d = 0, 0, 0, 0

        if not s or s.isspace():
            return cls(0, 0, 0, 0)

        # Verificar se é apenas um número simples
        try:
            if re.fullmatch(r'-?\d+(\.\d+)?', s.strip()):
                return cls(float(s.strip()), 0, 0, 0)
        except (ValueError, TypeError):
            pass

        # Processar a string substituindo - por +- para facilitar divisão
        s = s.replace(' ', '').replace('-', '+-')
        if s.startswith('+'):
            s = s[1:]
        elif s.startswith('+-'):
            s = '-' + s[2:]

        # Dividir os termos por '+'
        parts = re.split(r'(?<!e)\+', s)

        for part in parts:
            if not part:
                continue

            is_negative = part.startswith('-')
            if is_negative:
                part = part[1:]

            val = 1.0

            # Processar cada unidade imaginária
            if 'i' in part:
                if part == 'i':
                    pass
                else:
                    try:
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
                    pass
                else:
                    try:
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
                    pass
                else:
                    try:
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
                    if '/' in part:
                        num, denom = part.split('/')
                        val = float(num) / float(denom)
                    else:
                        val = float(part)
                    a += -val if is_negative else val
                except ValueError:
                    raise ValueError(f"Componente real inválido: '{part}'")

        return cls(a, b, c, d)

    def __add__(self, other):
        """Soma de quaterniões ou escalares."""
        if isinstance(other, (int, float)):
            return Quaternion(self.a + other, self.b, self.c, self.d)
        elif isinstance(other, complex):
            return Quaternion(self.a + other.real, self.b + other.imag, self.c, self.d)
        elif isinstance(other, Quaternion):
            return Quaternion(
                self.a + other.a,
                self.b + other.b,
                self.c + other.c,
                self.d + other.d
            )
        return NotImplemented

    def __radd__(self, other):
        """Soma à direita (comutativa)."""
        return self.__add__(other)

    def __sub__(self, other):
        """Subtracção de quaterniões ou escalares."""
        if isinstance(other, (int, float)):
            return Quaternion(self.a - other, self.b, self.c, self.d)
        elif isinstance(other, complex):
            return Quaternion(self.a - other.real, self.b - other.imag, self.c, self.d)
        elif isinstance(other, Quaternion):
            return Quaternion(
                self.a - other.a,
                self.b - other.b,
                self.c - other.c,
                self.d - other.d
            )
        return NotImplemented

    def __rsub__(self, other):
        """Subtracção à direita (other - self)."""
        if isinstance(other, (int, float, complex, Quaternion)):
            result = self.__sub__(other)
            return result * -1
        return NotImplemented
    
    def __mul__(self, other):
        """
        Multiplicação de quaterniões usando as regras de Hamilton.
        A multiplicação de quaterniões NÃO é comutativa.

        Args:
            other: Quaternião, escalar real/complexo

        Returns:
            Quaternion: Resultado da multiplicação
        """
        if isinstance(other, (int, float)):
            return Quaternion(
                self.a * other,
                self.b * other,
                self.c * other,
                self.d * other
            )
        elif isinstance(other, complex):
            other_q = Quaternion(other.real, other.imag, 0, 0)
            return self.__mul__(other_q)
        elif isinstance(other, Quaternion):
            # Multiplicação de quaterniões usando a regra de Hamilton
            a1, b1, c1, d1 = self.a, self.b, self.c, self.d
            a2, b2, c2, d2 = other.a, other.b, other.c, other.d

            a = a1*a2 - b1*b2 - c1*c2 - d1*d2
            b = a1*b2 + b1*a2 + c1*d2 - d1*c2
            c = a1*c2 - b1*d2 + c1*a2 + d1*b2
            d = a1*d2 + b1*c2 - c1*b2 + d1*a2

            return Quaternion(a, b, c, d)
        return NotImplemented

    def __rmul__(self, other):
        """Multiplicação à direita."""
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        elif isinstance(other, complex):
            other_q = Quaternion(other.real, other.imag, 0, 0)
            return other_q.__mul__(self)
        return NotImplemented

    def __truediv__(self, other):
        """
        Divisão à direita (DivR): self / other = self * other^-1.
        Este é o comportamento padrão para o operador '/'.

        Args:
            other: Quaternião ou escalar

        Returns:
            Quaternion: Resultado da divisão à direita

        Raises:
            ZeroDivisionError: Se o divisor for zero
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Divisão de quaternião por escalar zero")
            return self * (1.0 / other)
        elif isinstance(other, complex):
            if other == 0:
                raise ZeroDivisionError("Divisão de quaternião por complexo zero")
            other_q = Quaternion(other.real, other.imag, 0, 0)
            return self * other_q.inverse()
        elif isinstance(other, Quaternion):
            return self * other.inverse()
        return NotImplemented

    def __rtruediv__(self, other):
        """
        Divisão à direita por self: other / self = other * self^-1.

        Args:
            other: Escalar ou complexo

        Returns:
            Quaternion: Resultado da divisão à direita
        """
        if isinstance(other, (int, float)):
            return other * self.inverse()
        elif isinstance(other, complex):
            other_q = Quaternion(other.real, other.imag, 0, 0)
            return other_q * self.inverse()
        return NotImplemented

    def left_division(self, other):
        """
        Divisão à esquerda (DivL): other^-1 * self.
        Calcula o resultado 'x' para a equação: other * x = self.

        Args:
            other: Quaternião ou escalar

        Returns:
            Quaternion: Resultado da divisão à esquerda

        Raises:
            ZeroDivisionError: Se o divisor for zero
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Divisão à esquerda por escalar zero")
            inv_other = 1.0 / other
            return inv_other * self
        elif isinstance(other, complex):
            if other == 0:
                raise ZeroDivisionError("Divisão à esquerda por complexo zero")
            other_q = Quaternion(other.real, other.imag, 0, 0)
            return other_q.inverse() * self
        elif isinstance(other, Quaternion):
            return other.inverse() * self
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
        norm_sq = self.norm_squared()
        if norm_sq < 0 and abs(norm_sq) < 1e-15:
            return 0.0
        return math.sqrt(norm_sq)

    def vectorial(self):
        """
        Parte vectorial do quaternião: bi + cj + dk

        Returns:
            Quaternion: Parte vectorial do quaternião
        """
        return Quaternion(0, self.b, self.c, self.d)

    def real(self):
        """
        Parte real do quaternião: a

        Returns:
            Quaternion: Parte real como quaternião (a + 0i + 0j + 0k)
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
        epsilon = 1e-15
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
        Normaliza o quaternião (torna-o unitário, com magnitude 1).

        Returns:
            Quaternion: Quaternião normalizado

        Raises:
            ZeroDivisionError: Se o quaternião for nulo
        """
        norm = self.norm()
        epsilon = 1e-15
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
        Calcula o argumento do quaternião, que é o ângulo em radianos entre 
        a parte real e a parte vectorial.
        
        Para quaterniões q = a + bi + cj + dk, o argumento é arccos(a/|q|).
        
        Returns:
            float: O argumento do quaternião em radianos
        """
        norm = self.norm()
        epsilon = 1e-15
        if abs(norm) < epsilon:
            return 0.0
    
        cos_theta = self.a / norm
        cos_theta = max(-1.0, min(1.0, cos_theta))
    
        return math.acos(cos_theta)

    def vec_norm(self):
        """
        Calcula a norma (magnitude) da parte vectorial: ||vec(q)|| = sqrt(b^2 + c^2 + d^2)

        Returns:
            float: Norma da parte vectorial do quaternião
        """
        norm_sq_vec = self.b**2 + self.c**2 + self.d**2

        if norm_sq_vec < 0 and abs(norm_sq_vec) < 1e-15:
            return 0.0
    
        return math.sqrt(norm_sq_vec)

    def vec_normalize(self):
        """
        Normaliza a parte vectorial do quaternião, retornando um quaternião 
        com a mesma direcção vectorial mas com norma vectorial unitária.

        Returns:
            Quaternion: Quaternião com a parte vectorial normalizada e parte real zero

        Raises:
            ZeroDivisionError: Se a parte vectorial for nula
        """
        norm_vec = self.vec_norm()
        epsilon = 1e-15
        if abs(norm_vec) < epsilon:
            raise ZeroDivisionError("Normalização de parte vectorial (aproximadamente) nula")
    
        return Quaternion(
            0,
            self.b / norm_vec,
            self.c / norm_vec,
            self.d / norm_vec
        )
    
    def __pow__(self, exponent):
        """
        Potenciação do quaternião (self ** exponent).
        Suporta expoentes inteiros, reais e quaterniões.

        Args:
            exponent: O expoente (inteiro, real ou quaternião)

        Returns:
            Quaternion: Resultado da potenciação

        Raises:
            TypeError: Se o expoente não for um tipo suportado
        """
        if isinstance(exponent, int):
            if exponent == 2:
                return self * self
            elif exponent == 0:
                return Quaternion(1, 0, 0, 0)
            elif exponent == 1:
                return self
            elif exponent < 0:
                if exponent == -1:
                    return self.inverse()
                else:
                    inv = self.inverse()
                    res = Quaternion(1, 0, 0, 0)
                    for _ in range(abs(exponent)):
                        res = res * inv
                    return res
            else:  # exponent > 2
                # Exponenciação binária para eficiência
                res = Quaternion(1, 0, 0, 0)
                temp = self
                n = exponent
                while n > 0:
                    if n % 2 == 1:
                        res = res * temp
                    temp = temp * temp
                    n //= 2
                return res
    
        elif isinstance(exponent, float):
            # Para expoentes reais: q^r = exp(r * log(q))
            log_q = self.ln()
            r_log_q = log_q * exponent
            return r_log_q.exp()
    
        elif isinstance(exponent, Quaternion):
            # Para expoentes quaterniões: q^p = exp(p * log(q))
            log_q = self.ln()
            p_log_q = exponent * log_q
            return p_log_q.exp()
    
        else:
            raise TypeError("Expoente para potenciação de quaternião deve ser inteiro, float ou quaternião.")

    def ten_power(self):
        """
        Calcula 10 elevado à potência do quaternião: 10^q.
        Usa a fórmula: 10^q = exp(q * ln(10))

        Returns:
            Quaternion: Resultado da operação 10^q
        """
        log_10 = math.log(10)
        q_scaled = self * log_10
        return q_scaled.exp()

    def _apply_complex_func_to_quaternion(self, cmath_function):
        """
        Método auxiliar para aplicar uma função complexa (cmath) a um quaternião.
        
        Se q = s + v, calcula f(s + i*||v||) = Ac + i*Bc.
        O resultado do quaternião é Ac + (Bc/||v||)*v.
        
        Args:
            cmath_function: Função do módulo cmath a aplicar

        Returns:
            Quaternion: Resultado da aplicação da função
        """
        s = self.a
        vb, vc, vd = self.b, self.c, self.d
        norm_v_sq = vb**2 + vc**2 + vd**2
        epsilon = 1e-15

        if norm_v_sq < epsilon**2:  # Parte vectorial é praticamente zero
            complex_res_scalar = cmath_function(complex(s, 0.0))
            return Quaternion(complex_res_scalar.real, complex_res_scalar.imag, 0.0, 0.0)
        else:  # Parte vectorial não é zero
            norm_v = math.sqrt(norm_v_sq)
            z_complex = complex(s, norm_v)
            complex_result = cmath_function(z_complex)
            
            Ac = complex_result.real
            Bc = complex_result.imag
            
            res_a = Ac
            res_b, res_c, res_d = 0.0, 0.0, 0.0
            
            if math.isinf(Bc):
                u_b = vb / norm_v
                u_c = vc / norm_v
                u_d = vd / norm_v
                
                res_b = math.copysign(float('inf'), Bc * u_b) if abs(u_b) > epsilon else 0.0
                res_c = math.copysign(float('inf'), Bc * u_c) if abs(u_c) > epsilon else 0.0
                res_d = math.copysign(float('inf'), Bc * u_d) if abs(u_d) > epsilon else 0.0
            else:
                factor = Bc / norm_v
                res_b = factor * vb
                res_c = factor * vc
                res_d = factor * vd
                
            return Quaternion(res_a, res_b, res_c, res_d)
        
    # Funções trigonométricas
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

    # Funções hiperbólicas
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

    # Outras funções
    def exp(self):
        """Calcula a exponencial do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.exp)

    def ln(self):
        """Calcula o logaritmo natural (base e) do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.log)

    def sqrt(self):
        """Calcula a raiz quadrada principal do quaternião."""
        return self._apply_complex_func_to_quaternion(cmath.sqrt)

    def __str__(self):
        """
        Representação em string do quaternião de forma legível.
        Formato: a+bi+cj+dk, omitindo termos nulos e simplificando coeficientes 1.
        """
        parts = []
        epsilon = 1e-12

        def format_num(n):
            if abs(n - round(n)) < epsilon:
                num_str = str(round(n))
            else:
                num_str = f"{n:.6g}".rstrip('0').rstrip('.')
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
            term = "i" if abs(val - 1) < epsilon else f"{format_num(val)}i"

            if not parts:
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                parts.append(f"{sign}{term}")

        # Parte j
        if abs(self.c) > epsilon:
            sign = "+" if self.c > 0 else "-"
            val = abs(self.c)
            term = "j" if abs(val - 1) < epsilon else f"{format_num(val)}j"

            if not parts:
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                parts.append(f"{sign}{term}")

        # Parte k
        if abs(self.d) > epsilon:
            sign = "+" if self.d > 0 else "-"
            val = abs(self.d)
            term = "k" if abs(val - 1) < epsilon else f"{format_num(val)}k"

            if not parts:
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                parts.append(f"{sign}{term}")

        if not parts:
            return "0"
        else:
            result = "".join(parts)
            if result.startswith('+'):
                return result[1:]
            return result
        
    def __repr__(self):
        """Representação detalhada do objecto para depuração."""
        return f"Quaternion({self.a}, {self.b}, {self.c}, {self.d})"
    
class Coquaternion:
    """
    Classe que representa um coquaternião q = a + bi + cj + dk
    onde a, b, c, d são números reais e i, j, k são unidades imaginárias.

    Regras de multiplicação para Coquaterniões (diferentes dos quaterniões):
    i² = -1, j² = +1, k² = +1
    ij = k,  ji = -k
    jk = -i, kj = i
    ki = j,  ik = -j
    ijk = 1 (decorrente das outras)
    
    Usa métrica de Minkowski em vez da métrica euclidiana.
    """
    
    def __init__(self, a=0, b=0, c=0, d=0):
        """
        Inicializa um coquaternião com componentes a, b, c, d.

        Args:
            a (float): Parte real (escalar)
            b (float): Coeficiente de i
            c (float): Coeficiente de j  
            d (float): Coeficiente de k
        """
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)

    @classmethod
    def from_string(cls, s):
        """
        Cria um coquaternião a partir de uma string.
        Reutiliza a lógica de parsing de Quaternion, pois o formato é idêntico.

        Args:
            s (str): String representando o coquaternião

        Returns:
            Coquaternion: Objecto coquaternião
        """
        q_temp = Quaternion.from_string(s)
        return cls(q_temp.a, q_temp.b, q_temp.c, q_temp.d)

    def __add__(self, other):
        """Soma de coquaterniões ou escalares."""
        if isinstance(other, (int, float)):
            return Coquaternion(self.a + other, self.b, self.c, self.d)
        elif isinstance(other, complex):
            return Coquaternion(self.a + other.real, self.b + other.imag, self.c, self.d)
        elif isinstance(other, Coquaternion):
            return Coquaternion(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d)
        return NotImplemented

    def __radd__(self, other):
        """Soma à direita (comutativa)."""
        return self.__add__(other)
    
    def __sub__(self, other):
        """Subtracção de coquaterniões ou escalares."""
        if isinstance(other, (int, float)):
            return Coquaternion(self.a - other, self.b, self.c, self.d)
        elif isinstance(other, complex):
            return Coquaternion(self.a - other.real, self.b - other.imag, self.c, self.d)
        elif isinstance(other, Coquaternion):
            return Coquaternion(self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d)
        return NotImplemented

    def __rsub__(self, other):
        """Subtracção à direita (other - self)."""
        if isinstance(other, (int, float, complex, Coquaternion)):
            result = self.__sub__(other)
            return result * -1
        return NotImplemented
    
    def __mul__(self, other):
        """
        Multiplicação de coquaterniões usando regras específicas.
        Diferente dos quaterniões normais devido às propriedades j² = k² = +1.

        Args:
            other: Coquaternião, escalar real/complexo

        Returns:
            Coquaternion: Resultado da multiplicação
        """
        if isinstance(other, (int, float)):
            return Coquaternion(self.a * other, self.b * other, self.c * other, self.d * other)
        elif isinstance(other, complex):
            other_cq = Coquaternion(other.real, other.imag, 0, 0)
            return self.__mul__(other_cq)
        elif isinstance(other, Coquaternion):
            a1, b1, c1, d1 = self.a, self.b, self.c, self.d
            a2, b2, c2, d2 = other.a, other.b, other.c, other.d

            # Regras de Coquaternião: i*i=-1, j*j=1, k*k=1
            res_a = a1*a2 - b1*b2 + c1*c2 + d1*d2
            res_b = a2*b1 + a1*b2 + c2*d1 - c1*d2
            res_c = a2*c1 + a1*c2 + b2*d1 - b1*d2
            res_d = -(b2*c1) + b1*c2 + a2*d1 + a1*d2
            return Coquaternion(res_a, res_b, res_c, res_d)
        return NotImplemented

    def __rmul__(self, other):
        """Multiplicação à direita."""
        if isinstance(other, (int, float)):
            return self.__mul__(other)
        elif isinstance(other, complex):
            other_cq = Coquaternion(other.real, other.imag, 0, 0)
            return other_cq.__mul__(self)
        return NotImplemented
    
    def __truediv__(self, other):
        """
        Divisão à direita (DivR): self / other = self * other^-1.

        Args:
            other: Coquaternião ou escalar

        Returns:
            Coquaternion: Resultado da divisão à direita

        Raises:
            ZeroDivisionError: Se o divisor for zero
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Divisão de coquaternião por escalar zero")
            return self * (1.0 / other)
        elif isinstance(other, complex):
            if other == 0:
                raise ZeroDivisionError("Divisão de coquaternião por complexo zero")
            other_cq = Coquaternion(other.real, other.imag, 0, 0)
            return self * other_cq.inverse()
        elif isinstance(other, Coquaternion):
            return self * other.inverse()
        return NotImplemented

    def __rtruediv__(self, other):
        """
        Divisão à direita por self: other / self = other * self^-1.

        Args:
            other: Escalar ou complexo

        Returns:
            Coquaternion: Resultado da divisão à direita
        """
        if isinstance(other, (int, float)):
            return other * self.inverse()
        elif isinstance(other, complex):
            other_cq = Coquaternion(other.real, other.imag, 0, 0)
            return other_cq * self.inverse()
        return NotImplemented

    def left_division(self, other):
        """
        Divisão à esquerda (DivL): other^-1 * self.
        Calcula o resultado 'x' para a equação: other * x = self.

        Args:
            other: Coquaternião ou escalar

        Returns:
            Coquaternion: Resultado da divisão à esquerda

        Raises:
            ZeroDivisionError: Se o divisor for zero
        """
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Divisão à esquerda por escalar zero")
            inv_other = 1.0 / other
            return inv_other * self
        elif isinstance(other, complex):
            if other == 0:
                raise ZeroDivisionError("Divisão à esquerda por complexo zero")
            other_cq = Coquaternion(other.real, other.imag, 0, 0)
            return other_cq.inverse() * self
        elif isinstance(other, Coquaternion):
            return other.inverse() * self
        return NotImplemented
    
    def inverse(self):
        """
        Inverso do coquaternião: q^-1 = conj(q) / |q|^2_Minkowski.
        Para coquaterniões, usa-se a norma de Minkowski: |q|^2 = a^2 + b^2 - c^2 - d^2

        Returns:
            Coquaternion: Inverso do coquaternião

        Raises:
            ZeroDivisionError: Se o coquaternião for nulo segundo a métrica de Minkowski
        """
        norm_sq_mink = self.a**2 + self.b**2 - self.c**2 - self.d**2
        epsilon = 1e-15
    
        if abs(norm_sq_mink) < epsilon:
            raise ZeroDivisionError("Inverso de coquaternião (aproximadamente) nulo segundo métrica de Minkowski")

        conj = self.conjugate()
        return Coquaternion(
            conj.a / norm_sq_mink,
            conj.b / norm_sq_mink,
            conj.c / norm_sq_mink,
            conj.d / norm_sq_mink
        )

    def vec_norm(self):
        """
        Calcula a norma de Minkowski da parte vectorial: √|b² - c² - d²|.
        Esta é a função AbsIJK do Mathematica para coquaterniões.

        Returns:
            float: Norma de Minkowski da parte vectorial
        """
        norm_sq_vec_mink = self.b**2 - self.c**2 - self.d**2
        return math.sqrt(abs(norm_sq_vec_mink))

    def vec_normalize(self):
        """
        Normaliza a parte vectorial do coquaternião usando a métrica de Minkowski.

        Returns:
            Coquaternion: Coquaternião com a parte vectorial normalizada e parte real zero

        Raises:
            ZeroDivisionError: Se a parte vectorial for nula
        """
        norm_vec = self.vec_norm()
        epsilon = 1e-15
        if abs(norm_vec) < epsilon:
            raise ZeroDivisionError("Normalização de parte vectorial (aproximadamente) nula")

        return Coquaternion(
            0,
            self.b / norm_vec,
            self.c / norm_vec,
            self.d / norm_vec
        )

    def real(self):
        """
        Parte real do coquaternião: a

        Returns:
            Coquaternion: Parte real como coquaternião (a + 0i + 0j + 0k)
        """
        return Coquaternion(self.a, 0, 0, 0)

    def vectorial(self):
        """
        Parte vectorial do coquaternião: bi + cj + dk

        Returns:
            Coquaternion: Parte vectorial do coquaternião
        """
        return Coquaternion(0, self.b, self.c, self.d)

    def norm(self):
        """
        Norma de Minkowski do coquaternião: |√(a² + b² - c² - d²)|.
        Esta é a norma padrão para coquaterniões no Mathematica.

        Returns:
            float: Norma de Minkowski do coquaternião
        """
        norm_sq_mink = self.a**2 + self.b**2 - self.c**2 - self.d**2
        return math.sqrt(abs(norm_sq_mink))

    def conjugate(self):
        """
        Conjugado do coquaternião: q* = a - bi - cj - dk

        Returns:
            Coquaternion: Conjugado do coquaternião
        """
        return Coquaternion(self.a, -self.b, -self.c, -self.d)
    
    def _classify_coquaternion(self):
        """
        Classifica o coquaternião de acordo com o sinal de (b² - c² - d²):
        - T (timelike): b² - c² - d² > 0
        - L (lightlike): b² - c² - d² = 0  
        - S (spacelike): b² - c² - d² < 0

        Returns:
            str: 'T', 'L', ou 'S' dependendo da classificação
        """
        discriminant = self.b**2 - self.c**2 - self.d**2
        epsilon = 1e-15
    
        if abs(discriminant) < epsilon:
            return 'L'  # Lightlike
        elif discriminant > 0:
            return 'T'  # Timelike
        else:
            return 'S'  # Spacelike
        
    def _get_omega_q(self):
        """
        Calcula SIGN[q] para um coquaternião q.
        SIGN[q] = Vec[q] / AbsIJK[q] se AbsIJK[q] != 0.
        SIGN[q] = Vec[q] se AbsIJK[q] == 0.

        Returns:
            Coquaternion: O resultado da operação SIGN
        """
        vec_norm = self.vec_norm()
        epsilon = 1e-15

        if abs(vec_norm) < epsilon:
            return self.vectorial()  
    
        return Coquaternion(0, self.b / vec_norm, self.c / vec_norm, self.d / vec_norm)
    
    def exp(self):
        """
        Calcula a função exponencial do coquaternião seguindo as fórmulas específicas
        baseadas na classificação T/L/S do coquaternião.

        Returns:
            Coquaternion: Resultado da exponencial do coquaternião
        """
        classification = self._classify_coquaternion()
        q0 = self.a
        vec_norm = self.vec_norm()
        omega_q = self._get_omega_q()
    
        exp_q0 = math.exp(q0)
    
        if classification == 'T':  # Timelike
            # Exp(q) = e^q0 * (cos(||q||) + ωq * sin(||q||))
            cos_norm = math.cos(vec_norm)
            sin_norm = math.sin(vec_norm)
        
            result_a = exp_q0 * cos_norm
            result_vec = omega_q * (exp_q0 * sin_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        elif classification == 'S':  # Spacelike
            # Exp(q) = e^q0 * (cosh(||q||) + ωq * sinh(||q||))
            cosh_norm = math.cosh(vec_norm)
            sinh_norm = math.sinh(vec_norm)
        
            result_a = exp_q0 * cosh_norm
            result_vec = omega_q * (exp_q0 * sinh_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        else:  # Lightlike (L)
            # Exp(q) = e^q0 * (1 + ωq)
            result_a = exp_q0
            result_vec = omega_q * exp_q0
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
        
    def sin(self):
        """
        Calcula o seno do coquaternião seguindo as fórmulas específicas
        baseadas na classificação T/L/S do coquaternião.

        Returns:
            Coquaternion: Resultado do seno do coquaternião
        """
        classification = self._classify_coquaternion()
        q0 = self.a
        vec_norm = self.vec_norm()
        omega_q = self._get_omega_q()
    
        if classification == 'T':  # Timelike
            # Sin(q) = sin(q0) * cosh(||q||) + ωq * cos(q0) * sinh(||q||)
            sin_q0 = math.sin(q0)
            cos_q0 = math.cos(q0)
            cosh_norm = math.cosh(vec_norm)
            sinh_norm = math.sinh(vec_norm)
        
            result_a = sin_q0 * cosh_norm
            result_vec = omega_q * (cos_q0 * sinh_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        elif classification == 'S':  # Spacelike
            # Sin(q) = sin(q0) * cos(||q||) + ωq * cos(q0) * sin(||q||)
            sin_q0 = math.sin(q0)
            cos_q0 = math.cos(q0)
            cos_norm = math.cos(vec_norm)
            sin_norm = math.sin(vec_norm)
        
            result_a = sin_q0 * cos_norm
            result_vec = omega_q * (cos_q0 * sin_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        else:  # Lightlike (L)
            # Sin(q) = sin(q0) + ωq * cos(q0)
            sin_q0 = math.sin(q0)
            cos_q0 = math.cos(q0)
        
            result_a = sin_q0
            result_vec = omega_q * cos_q0
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
        
    def cos(self):
        """
        Calcula o cosseno do coquaternião seguindo as fórmulas específicas
        baseadas na classificação T/L/S do coquaternião.

        Returns:
            Coquaternion: Resultado do cosseno do coquaternião
        """
        classification = self._classify_coquaternion()
        q0 = self.a
        vec_norm = self.vec_norm()
        omega_q = self._get_omega_q()
    
        if classification == 'T':  # Timelike
            # Cos(q) = cos(q0) * cosh(||q||) - ωq * sin(q0) * sinh(||q||)
            cos_q0 = math.cos(q0)
            sin_q0 = math.sin(q0)
            cosh_norm = math.cosh(vec_norm)
            sinh_norm = math.sinh(vec_norm)
        
            result_a = cos_q0 * cosh_norm
            result_vec = omega_q * (-sin_q0 * sinh_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        elif classification == 'S':  # Spacelike
            # Cos(q) = cos(q0) * cos(||q||) - ωq * sin(q0) * sin(||q||)
            cos_q0 = math.cos(q0)
            sin_q0 = math.sin(q0)
            cos_norm = math.cos(vec_norm)
            sin_norm = math.sin(vec_norm)
        
            result_a = cos_q0 * cos_norm
            result_vec = omega_q * (-sin_q0 * sin_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        else:  # Lightlike (L)
            # Cos(q) = cos(q0) - ωq * sin(q0)
            cos_q0 = math.cos(q0)
            sin_q0 = math.sin(q0)
        
            result_a = cos_q0
            result_vec = omega_q * (-sin_q0)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
        
    def sinh(self):
        """
        Calcula o seno hiperbólico do coquaternião seguindo as fórmulas específicas
        baseadas na classificação T/L/S do coquaternião.

        Returns:
            Coquaternion: Resultado do seno hiperbólico do coquaternião
        """
        classification = self._classify_coquaternion()
        q0 = self.a
        vec_norm = self.vec_norm()
        omega_q = self._get_omega_q()
    
        if classification == 'T':  # Timelike
            # Sinh(q) = sinh(q0) * cos(||q||) + ωq * cosh(q0) * sin(||q||)
            sinh_q0 = math.sinh(q0)
            cosh_q0 = math.cosh(q0)
            cos_norm = math.cos(vec_norm)
            sin_norm = math.sin(vec_norm)
        
            result_a = sinh_q0 * cos_norm
            result_vec = omega_q * (cosh_q0 * sin_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        elif classification == 'S':  # Spacelike
            # Sinh(q) = sinh(q0) * cosh(||q||) + ωq * cosh(q0) * sinh(||q||)
            sinh_q0 = math.sinh(q0)
            cosh_q0 = math.cosh(q0)
            cosh_norm = math.cosh(vec_norm)
            sinh_norm = math.sinh(vec_norm)
        
            result_a = sinh_q0 * cosh_norm
            result_vec = omega_q * (cosh_q0 * sinh_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        else:  # Lightlike (L)
            # Sinh(q) = sinh(q0) + ωq * cosh(q0)
            sinh_q0 = math.sinh(q0)
            cosh_q0 = math.cosh(q0)
        
            result_a = sinh_q0
            result_vec = omega_q * cosh_q0
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
        
    def cosh(self):
        """
        Calcula o cosseno hiperbólico do coquaternião seguindo as fórmulas específicas
        baseadas na classificação T/L/S do coquaternião.

        Returns:
            Coquaternion: Resultado do cosseno hiperbólico do coquaternião
        """
        classification = self._classify_coquaternion()
        q0 = self.a
        vec_norm = self.vec_norm()
        omega_q = self._get_omega_q()
    
        if classification == 'T':  # Timelike
            # Cosh(q) = cosh(q0) * cos(||q||) + ωq * sinh(q0) * sin(||q||)
            cosh_q0 = math.cosh(q0)
            sinh_q0 = math.sinh(q0)
            cos_norm = math.cos(vec_norm)
            sin_norm = math.sin(vec_norm)
        
            result_a = cosh_q0 * cos_norm
            result_vec = omega_q * (sinh_q0 * sin_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        elif classification == 'S':  # Spacelike
            # Cosh(q) = cosh(q0) * cosh(||q||) + ωq * sinh(q0) * sinh(||q||)
            cosh_q0 = math.cosh(q0)
            sinh_q0 = math.sinh(q0)
            cosh_norm = math.cosh(vec_norm)
            sinh_norm = math.sinh(vec_norm)
        
            result_a = cosh_q0 * cosh_norm
            result_vec = omega_q * (sinh_q0 * sinh_norm)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        else:  # Lightlike (L)
            # Cosh(q) = cosh(q0) + ωq * sinh(q0)
            cosh_q0 = math.cosh(q0)
            sinh_q0 = math.sinh(q0)
        
            result_a = cosh_q0
            result_vec = omega_q * sinh_q0
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)

    def tanh(self):
        """
        Calcula a tangente hiperbólica do coquaternião usando a relação:
        Tanh(q) = Sinh(q) / Cosh(q)

        Returns:
            Coquaternion: Resultado da tangente hiperbólica do coquaternião
        """
        sinh_q = self.sinh()
        cosh_q = self.cosh()
        return sinh_q.__truediv__(cosh_q)
    
    def tan(self):
        """
        Calcula a tangente do coquaternião usando a relação:
        Tan(q) = Sin(q) / Cos(q)

        Returns:
            Coquaternion: Resultado da tangente do coquaternião
        """
        sin_q = self.sin()
        cos_q = self.cos()
        return sin_q.__truediv__(cos_q)
    
    def ln(self):
        """
        Calcula o logaritmo natural (base e) do coquaternião seguindo as fórmulas
        específicas baseadas na classificação T/L/S do coquaternião.

        Returns:
            Coquaternion: Resultado do logaritmo do coquaternião
        
        Raises:
            ValueError: Se o coquaternião for zero ou estiver numa configuração inválida
        """
        epsilon = 1e-15
        if (abs(self.a) < epsilon and abs(self.b) < epsilon and 
            abs(self.c) < epsilon and abs(self.d) < epsilon):
            raise ValueError("Logaritmo de coquaternião nulo é indefinido")
    
        classification = self._classify_coquaternion()
        q0 = self.a
        vec_norm = self.vec_norm()
        omega_q = self._get_omega_q()
    
        norm_mink_squared = self.a**2 + self.b**2 - self.c**2 - self.d**2

        if classification == 'T':  # Timelike
            # Log(q) = log(||q||) + ωq * atan2(q0, ||q||)
            if norm_mink_squared <= 0:
                raise ValueError("Norma de Minkowski para coquaternião timelike no logaritmo")

            norm_mink = math.sqrt(norm_mink_squared)
            log_norm = math.log(norm_mink)
            angle = math.atan2(vec_norm, q0)
        
            result_a = log_norm
            result_vec = omega_q * angle
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        elif classification == 'S':  # Spacelike
            # Log(q) = log(||q||) + ωq * arctanh(||q|| / q0)
            if q0 <= 0:
                raise ValueError("Parte real deve ser positiva para coquaternião spacelike no logaritmo")
        
            if norm_mink_squared <= 0:
                raise ValueError("Norma de Minkowski para coquaternião spacelike no logaritmo")
        
            norm_mink = math.sqrt(norm_mink_squared)
            log_norm = math.log(norm_mink)
            
            ratio = vec_norm / q0
            if abs(ratio) >= 1:
                raise ValueError("Argumento de arctanh fora do domínio válido")
        
            arctanh_value = math.atanh(ratio)
        
            result_a = log_norm
            result_vec = omega_q * arctanh_value
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)
    
        else:  # Lightlike (L)
            # Log(q) = log(q0) + (1/q0) * ωq, apenas válido se q0 > 0
            if q0 <= 0:
                raise ValueError("Parte real deve ser positiva para coquaternião lightlike no logaritmo")
        
            log_q0 = math.log(q0)
        
            result_a = log_q0
            result_vec = omega_q * (1.0 / q0)
        
            return Coquaternion(result_a, result_vec.b, result_vec.c, result_vec.d)

    def atan(self):
        """
        Calcula o arco-tangente do coquaternião usando a fórmula:
        ArcTan(q) = -ωq * Log((1 + ωq * q) / (1 - ωq * q))

        Returns:
            Coquaternion: Resultado do arco-tangente do coquaternião
    
        Raises:
            ValueError: Se ocorrer divisão por zero ou logaritmo de valor inválido
        """
        omega_q = self._get_omega_q()
        omega_q_times_q = omega_q * self
        one_plus = Coquaternion(1, 0, 0, 0) + omega_q_times_q
        one_minus = Coquaternion(1, 0, 0, 0) - omega_q_times_q

        try:
            division_result = one_plus / one_minus
            log_result = division_result.ln()
            result = omega_q * (-1) * log_result
            return result
        except Exception as e:
            raise ValueError(f"Erro no cálculo do arco-tangente: {e}")

    def norm_minkowski(self):
        """
        Calcula a norma de Minkowski do coquaternião: sqrt(a² + b² - c² - d²).

        Returns:
            float: Norma de Minkowski do coquaternião
        
        Raises:
            ValueError: Se a norma ao quadrado for negativa
        """
        norm_squared = self.a**2 + self.b**2 - self.c**2 - self.d**2
    
        if norm_squared < 0:
            raise ValueError("Norma de Minkowski ao quadrado é negativa")
    
        return math.sqrt(norm_squared)
    
    def normalize_minkowski(self):
        """
        Normaliza o coquaternião usando a norma de Minkowski.

        Returns:
            Coquaternion: Coquaternião normalizado segundo a métrica de Minkowski
        
        Raises:
            ZeroDivisionError: Se a norma de Minkowski for zero
        """
        norm_mink = self.norm_minkowski()
        epsilon = 1e-15
    
        if abs(norm_mink) < epsilon:
            raise ZeroDivisionError("Normalização de coquaternião com norma de Minkowski nula")
    
        return Coquaternion(
            self.a / norm_mink,
            self.b / norm_mink,
            self.c / norm_mink,
            self.d / norm_mink
        )
    
    def __pow__(self, exponent):
        """
        Potenciação do coquaternião (self ** exponent).
        Para coquaterniões, usa-se a fórmula: q^n = exp(n * ln(q))

        Args:
            exponent: O expoente (inteiro, real ou coquaternião)

        Returns:
            Coquaternion: Resultado da potenciação
        """
        # Casos especiais para eficiência
        if isinstance(exponent, int):
            if exponent == 0:
                return Coquaternion(1, 0, 0, 0)
            elif exponent == 1:
                return self
            elif exponent == 2:
                return self * self
            elif exponent == -1:
                return self.inverse()
    
        # Fórmula geral: q^n = exp(n * ln(q))
        try:
            ln_q = self.ln()
            n_ln_q = exponent * ln_q if isinstance(exponent, (int, float)) else Coquaternion(exponent) * ln_q
            return n_ln_q.exp()
        except Exception as e:
            raise ValueError(f"Erro no cálculo da potência: {e}")

    def ten_power(self):
        """
        Calcula 10 elevado à potência do coquaternião: 10^q.
        Usa a fórmula: 10^q = exp(q * ln(10))

        Returns:
            Coquaternion: Resultado da operação 10^q
        """
        log_10 = math.log(10)
        q_scaled = self * log_10
        return q_scaled.exp()

    def sqrt(self):
        """
        Calcula a raiz quadrada principal do coquaternião.
        Usa a fórmula: sqrt(q) = q^(1/2) = exp(0.5 * ln(q))

        Returns:
            Coquaternion: Resultado da raiz quadrada
        """
        try:
            return self.__pow__(0.5)
        except Exception as e:
            raise ValueError(f"Erro no cálculo da raiz quadrada: {e}")

    def __str__(self):
        """
        Representação em string do coquaternião de forma legível.
        Formato: a+bi+cj+dk, omitindo termos nulos e simplificando coeficientes 1.
        """
        parts = []
        epsilon = 1e-12

        def format_num(n):
            if abs(n - round(n)) < epsilon:
                num_str = str(round(n))
            else:
                num_str = f"{n:.6g}".rstrip('0').rstrip('.')
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
            term = "i" if abs(val - 1) < epsilon else f"{format_num(val)}i"

            if not parts:
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                parts.append(f"{sign}{term}")

        # Parte j
        if abs(self.c) > epsilon:
            sign = "+" if self.c > 0 else "-"
            val = abs(self.c)
            term = "j" if abs(val - 1) < epsilon else f"{format_num(val)}j"

            if not parts:
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                parts.append(f"{sign}{term}")

        # Parte k
        if abs(self.d) > epsilon:
            sign = "+" if self.d > 0 else "-"
            val = abs(self.d)
            term = "k" if abs(val - 1) < epsilon else f"{format_num(val)}k"

            if not parts:
                parts.append(f"{sign if sign == '-' else ''}{term}")
            else:
                parts.append(f"{sign}{term}")

        if not parts:
            return "0"
        else:
            result = "".join(parts)
            if result.startswith('+'):
                return result[1:]
            return result

    def __repr__(self):
        """Representação detalhada do objecto para depuração."""
        return f"Coquaternion({self.a}, {self.b}, {self.c}, {self.d})"


# Funções de Parse para as Calculadoras

def parse_quaternion_expr(expression):
    """
    Parse e avalia expressões com quaterniões, suportando operações básicas,
    potenciação (**), raiz quadrada (sqrt), divisões (divL, divR) e funções específicas.

    Args:
        expression (str): Expressão a ser avaliada

    Returns:
        Quaternion: Resultado da expressão

    Raises:
        ValueError: Se a expressão não puder ser avaliada
    """
    # Substituições de operadores
    expression = expression.replace('×', '*')
    expression = expression.replace('^', '**')
    
    # Substituir símbolos de raiz quadrada
    expression = re.sub(r'√(\d+)', r'sqrt(\1)', expression)
    expression = re.sub(r'√\(([^)]+)\)', r'sqrt(\1)', expression)
    
    # Conversões de formato
    expression = re.sub(r'(\d+)([ijk])(?!\w)', r'\1*\2', expression)
    expression = re.sub(r'([ijk])(\d+)(?!\w)', r'\1*\2', expression)
    expression = re.sub(r'(\w+\([^()]*(?:\([^()]*\)[^()]*)*\))([ijk])(?!\w)', r'\1*\2', expression)
    expression = re.sub(r'([a-oq-zA-OQ-Z_][a-oq-zA-OQ-Z0-9_]*)([ijk])(?!\w)', r'\1*\2', expression)

    # Substituir unidades imaginárias
    expression = re.sub(r'\bi\b', 'Quaternion(0,1,0,0)', expression)
    expression = re.sub(r'\bj\b', 'Quaternion(0,0,1,0)', expression)
    expression = re.sub(r'\bk\b', 'Quaternion(0,0,0,1)', expression)

    # Ambiente seguro para avaliação
    safe_env = {
        'Quaternion': Quaternion,
        'math': math,
        'pi': math.pi,
        'e': math.e,
        
        # Funções específicas de Quaterniões
        'conjugate': lambda q: q.conjugate() if isinstance(q, Quaternion) else Quaternion(q).conjugate(),
        'norm': lambda q: q.norm() if isinstance(q, Quaternion) else abs(q),
        'vectorial': lambda q: q.vectorial() if isinstance(q, Quaternion) else Quaternion(0,0,0,0),
        'real': lambda q: q.real() if isinstance(q, Quaternion) else Quaternion(q),
        'sqrt': lambda q: q.sqrt() if isinstance(q, Quaternion) else math.sqrt(q),
        'inverse': lambda q: q.inverse() if isinstance(q, Quaternion) else 1.0/q,
        'normalize': lambda q: q.normalize() if isinstance(q, Quaternion) else (q/abs(q) if q != 0 else 0),
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
        
        # Divisões específicas
        'divL': lambda q, p: (Quaternion(q) if not isinstance(q, Quaternion) else q).left_division(
                            Quaternion(p) if not isinstance(p, Quaternion) else p),
        'divR': lambda q, p: (Quaternion(q) if not isinstance(q, Quaternion) else q) / 
                            (Quaternion(p) if not isinstance(p, Quaternion) else p),
        
        # Operações especiais
        'neg': lambda q: Quaternion(-q.a, -q.b, -q.c, -q.d) if isinstance(q, Quaternion) else -q,
        'absIJK': lambda q: q.vec_norm() if isinstance(q, Quaternion) else 0,
        'sign': lambda q: q.vec_normalize() if isinstance(q, Quaternion) else Quaternion(0, 0, 0, 0),
        'pow10': lambda q: q.ten_power() if isinstance(q, Quaternion) else math.pow(10, q),
        'pow': lambda q, n: q.__pow__(n) if isinstance(q, Quaternion) else math.pow(q, n),
    }

    try:
        # Processar negações unárias
        expression = re.sub(r'(\w|\)|\d)\s*-\s*', r'\1 __MINUS__ ', expression)
        
        neg_pattern = r'-(\w+\(.*?\))'
        while re.search(neg_pattern, expression):
            expression = re.sub(neg_pattern, r'neg(\1)', expression)
        
        expression = re.sub(r'-([ijk])\b', r'neg(\1)', expression)
        expression = re.sub(r'(?<![a-zA-Z0-9_])-(\d+(\.\d+)?)', r'neg(\1)', expression)
        expression = expression.replace('__MINUS__', '-')

        # Processar negações de divisões
        neg_func_pattern = r'-\s*(divL|divR)\s*\('
        if re.search(neg_func_pattern, expression):
            expression = re.sub(neg_func_pattern, r' - neg(\1(', expression)
            
            for match in re.finditer(r'neg\((divL|divR)\(', expression):
                start_pos = match.end() - 1
                count = 1
                close_pos = start_pos
                
                for i in range(start_pos + 1, len(expression)):
                    if expression[i] == '(':
                        count += 1
                    elif expression[i] == ')':
                        count -= 1
                        if count == 0:
                            close_pos = i
                            break
                        
                if close_pos < len(expression) and count == 0:
                    expression = expression[:close_pos+1] + ')' + expression[close_pos+1:]
        
        result = eval(expression, {"__builtins__": {}}, safe_env)

        if isinstance(result, Quaternion):
            return result
        elif isinstance(result, (int, float)):
            return Quaternion(result)
        elif isinstance(result, complex):
            return Quaternion(result.real, result.imag)
        else:
            try:
                return Quaternion(float(result))
            except (TypeError, ValueError):
                raise ValueError(f"Resultado da expressão é de tipo não suportado: {type(result)}")

    except Exception as e:
        original_expression = expression
        original_expression = original_expression.replace('Quaternion(0,1,0,0)','i')
        original_expression = original_expression.replace('Quaternion(0,0,1,0)','j')
        original_expression = original_expression.replace('Quaternion(0,0,0,1)','k')
        try:
            return Quaternion.from_string(original_expression)
        except Exception as e_parse:
            import traceback
            tb_str = traceback.format_exc()
            raise ValueError(f"Erro ao avaliar expressão '{original_expression}'.\nDetalhe: {str(e)}\nParser alternativo falhou: {str(e_parse)}\nTraceback: {tb_str}")

def parse_coquaternion_expr(expression):
    """
    Parse e avalia expressões com coquaterniões, suportando operações específicas
    da álgebra de coquaterniões com métrica de Minkowski.

    Args:
        expression (str): Expressão a ser avaliada

    Returns:
        Coquaternion: Resultado da expressão

    Raises:
        ValueError: Se a expressão não puder ser avaliada
    """
    # Substituições básicas (igual aos quaterniões)
    expression = expression.replace('×', '*')
    expression = expression.replace('^', '**')
    
    expression = re.sub(r'√(\d+)', r'sqrt(\1)', expression)
    expression = re.sub(r'√\(([^)]+)\)', r'sqrt(\1)', expression)
    
    expression = re.sub(r'(\d+)([ijk])(?!\w)', r'\1*\2', expression)
    expression = re.sub(r'([ijk])(\d+)(?!\w)', r'\1*\2', expression)
    expression = re.sub(r'(\w+\([^()]*(?:\([^()]*\)[^()]*)*\))([ijk])(?!\w)', r'\1*\2', expression)
    expression = re.sub(r'([a-oq-zA-OQ-Z_][a-oq-zA-OQ-Z0-9_]*)([ijk])(?!\w)', r'\1*\2', expression)

    # Substituir unidades por Coquaternion
    expression = re.sub(r'\bi\b', 'Coquaternion(0,1,0,0)', expression)
    expression = re.sub(r'\bj\b', 'Coquaternion(0,0,1,0)', expression)
    expression = re.sub(r'\bk\b', 'Coquaternion(0,0,0,1)', expression)

    # Ambiente específico para coquaterniões
    safe_env = {
        'Coquaternion': Coquaternion,
        'math': math,
        'pi': math.pi,
        'e': math.e,
        
        # Funções específicas de Coquaterniões
        'conjugate': lambda q: q.conjugate() if isinstance(q, Coquaternion) else Coquaternion(q).conjugate(),
        'norm': lambda q: q.norm() if isinstance(q, Coquaternion) else abs(q),
        'vectorial': lambda q: q.vectorial() if isinstance(q, Coquaternion) else Coquaternion(0,0,0,0),
        'real': lambda q: q.real() if isinstance(q, Coquaternion) else Coquaternion(q),
        'sqrt': lambda q: q.sqrt() if hasattr(q, 'sqrt') and isinstance(q, Coquaternion) else math.sqrt(q),
        'inverse': lambda q: q.inverse() if isinstance(q, Coquaternion) else 1.0/q,
        'normalize': lambda q: q.normalize_minkowski() if isinstance(q, Coquaternion) else (q/abs(q) if q != 0 else 0),

        # Funções trigonométricas e hiperbólicas
        'sin': lambda q: q.sin() if isinstance(q, Coquaternion) else math.sin(q),
        'cos': lambda q: q.cos() if isinstance(q, Coquaternion) else math.cos(q),
        'tan': lambda q: q.tan() if isinstance(q, Coquaternion) else math.tan(q),
        'sinh': lambda q: q.sinh() if isinstance(q, Coquaternion) else math.sinh(q),
        'cosh': lambda q: q.cosh() if isinstance(q, Coquaternion) else math.cosh(q),
        'tanh': lambda q: q.tanh() if isinstance(q, Coquaternion) else math.tanh(q),
        'atan': lambda q: q.atan() if isinstance(q, Coquaternion) else math.atan(q),
        'exp': lambda q: q.exp() if isinstance(q, Coquaternion) else math.exp(q),
        'ln': lambda q: q.ln() if isinstance(q, Coquaternion) else math.log(q),
        'log': lambda q: q.ln() if isinstance(q, Coquaternion) else math.log(q),
        
        # Divisões específicas
        'divL': lambda q, p: (Coquaternion(q) if not isinstance(q, Coquaternion) else q).left_division(
                            Coquaternion(p) if not isinstance(p, Coquaternion) else p),
        'divR': lambda q, p: (Coquaternion(q) if not isinstance(q, Coquaternion) else q) / 
                            (Coquaternion(p) if not isinstance(p, Coquaternion) else p),
        
        # Operações especiais
        'neg': lambda q: Coquaternion(-q.a, -q.b, -q.c, -q.d) if isinstance(q, Coquaternion) else -q,
        'absIJK': lambda q: q.vec_norm() if isinstance(q, Coquaternion) else 0,
        'sign': lambda q: q._get_omega_q() if isinstance(q, Coquaternion) else Coquaternion(0, 0, 0, 0),
        'norm_mink': lambda q: q.norm_minkowski() if isinstance(q, Coquaternion) else abs(q),
        'normalize_mink': lambda q: q.normalize_minkowski() if isinstance(q, Coquaternion) else (q/abs(q) if q != 0 else 0),
        'pow': lambda q, n: q.__pow__(n) if isinstance(q, Coquaternion) else math.pow(q, n),
        'pow10': lambda q: q.ten_power() if isinstance(q, Coquaternion) else math.pow(10, q),
    }

    try:
        # Processar negações (mesmo processamento dos quaterniões)
        expression = re.sub(r'(\w|\)|\d)\s*-\s*', r'\1 __MINUS__ ', expression)
        
        neg_pattern = r'-(\w+\(.*?\))'
        while re.search(neg_pattern, expression):
            expression = re.sub(neg_pattern, r'neg(\1)', expression)
        
        expression = re.sub(r'-([ijk])\b', r'neg(\1)', expression)
        expression = re.sub(r'(?<![a-zA-Z0-9_])-(\d+(\.\d+)?)', r'neg(\1)', expression)
        expression = expression.replace('__MINUS__', '-')

        neg_func_pattern = r'-\s*(divL|divR)\s*\('
        if re.search(neg_func_pattern, expression):
            expression = re.sub(neg_func_pattern, r' - neg(\1(', expression)
            
            for match in re.finditer(r'neg\((divL|divR)\(', expression):
                start_pos = match.end() - 1
                count = 1
                close_pos = start_pos
                
                for i in range(start_pos + 1, len(expression)):
                    if expression[i] == '(':
                        count += 1
                    elif expression[i] == ')':
                        count -= 1
                        if count == 0:
                            close_pos = i
                            break
                        
                if close_pos < len(expression) and count == 0:
                    expression = expression[:close_pos+1] + ')' + expression[close_pos+1:]
        
        result = eval(expression, {"__builtins__": {}}, safe_env)

        if isinstance(result, Coquaternion):
            return result
        elif isinstance(result, (int, float)):
            return Coquaternion(result)
        elif isinstance(result, complex):
            return Coquaternion(result.real, result.imag)
        else:
            try:
                return Coquaternion(float(result))
            except (TypeError, ValueError):
                raise ValueError(f"Resultado da expressão é de tipo não suportado: {type(result)}")

    except Exception as e:
        original_expression = expression
        original_expression = original_expression.replace('Coquaternion(0,1,0,0)','i')
        original_expression = original_expression.replace('Coquaternion(0,0,1,0)','j')
        original_expression = original_expression.replace('Coquaternion(0,0,0,1)','k')
        try:
            return Coquaternion.from_string(original_expression)
        except Exception as e_parse:
            import traceback
            tb_str = traceback.format_exc()
            raise ValueError(f"Erro ao avaliar expressão '{original_expression}'.\nDetalhe: {str(e)}\nParser alternativo falhou: {str(e_parse)}\nTraceback: {tb_str}")