import math


class Curva:
    pixels = []
    intermediarios = []

    def __init__(self, pixels=None, intermediarios=None):
        self.pixels = pixels or []
        self.intermediarios = intermediarios or []

    def __getattr__(self, item):
        return item.upper()

    def __getitem__(self, item):
        if item == 'pixels':
            return self.pixels
        if item == 'intermediarios':
            return self.intermediarios
        return None

    def __repr__(self):
        return {'pixels': self.pixels, 'intermediarios': self.intermediarios}

    def __str__(self):
        pixels = "'pixels': {}".format(self.pixels)
        intermediarios = "'intermediarios': {}".format(self.intermediarios)
        return "{"+pixels+", "+intermediarios+"}"

    def _set_pixels(self, pixels=None):
        if pixels:
            self.pixels=pixels
            return True
        else:
            return False

    def _set_intermediarios(self, intermediarios=None):
        if intermediarios:
            self.intermediarios=intermediarios
            return True
        else:
            return False


"""
ALGORITMO DESENVOLVIDO POR ROBERTO GEA
DISPONÍVEL EM: https://gist.github.com/Alquimista/1274149
ACESSO EM: 12/11/2019
"""

"""
Coeficiente Bionimial de Newton utilizado no polinômio de Bernstein
@param: i (int) = iésimo coeficiente da interpolação
@param: n (int) = quantidade total de pontos
"""


def binomial(i, n):
    return math.factorial(n) / float(math.factorial(i) * math.factorial(n - i))


"""
Polinômio de Bernstein = Combinação n,i * (t ^ (n-1)) * (1-t)^i
@param: t (int) = Valor paramétrico da curva
@param: i (int) = ponto atual da curva
@param: n (int) = quantidade total de pontos
"""


def bernstein(t, i, n):
    return binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


"""
Calcula a coordenada de um ponto na curva de Bézier, onde para cada novo
ponto (i) criado, tem-se f(xi) * bernstein e f(yi) * bernstein 
@param: t (int) = Valor paramétrico da curva, valor entre 0 e 1, intervalo
entre os pontos a serem criados.
@param: cPoints (Tupla inteiros) = Pontos de controle da curva a ser criada
"""

def p_bezier(t, n_points):
    n = len(n_points) - 1
    x = y = i = 0
    for i, pos in enumerate(n_points):
        bern = bernstein(t, i, n)
        x += pos.get('x') * bern  # modificado
        y += pos.get('y') * bern  # modificado
    return x, y


"""
Quantia de pontos na curva de Bézier
@param: n (int) = número de pontos a serem criados
@param: points (Tupla inteiros )= pontos de controle
"""


def bezier(n, n_points):
    response = []
    for i in range(n):
        t = i / float(n - 1)
        x, y = p_bezier(t, n_points)
        response.append({'x': x, 'y': y})
    return response
