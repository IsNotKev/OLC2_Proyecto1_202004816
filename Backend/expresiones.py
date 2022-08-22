from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4
    MODULO = 5

class OPERACION_LOGICA(Enum) :
    MAYOR_QUE = 1
    MENOR_QUE = 2
    IGUAL = 3
    DIFERENTE = 4
    MAYORIGUAL = 5
    MENORIGUAL = 6
    AND = 7
    OR = 8

class ExpresionNumerica:
    '''
        Esta clase representa una expresión numérica
    '''

class ExpresionBinaria(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Binaria.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionPotencia(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Binaria.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, tipo) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.tipo = tipo

class ExpresionNegativo(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Negativa.
        Esta clase recibe la expresion
    '''
    def __init__(self, exp) :
        self.exp = exp


class ExpresionNumero(ExpresionNumerica) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

    def __init__(self, val, tipo) :
        self.val = val
        self.tipo = tipo

class ExpresionIdentificador(ExpresionNumerica) :
    '''
        Esta clase representa un identificador.
    '''

    def __init__(self, id) :
        self.id = id

class ExpresionCadena :
    '''
        Esta clase representa una Expresión de tipo cadena.
    '''

class ExpresionConcatenar(ExpresionCadena) :
    '''
        Esta clase representa una Expresión de tipo cadena.
        Recibe como parámetros las 2 expresiones a concatenar
    '''

    def __init__(self, exp1, exp2) :
        self.exp1 = exp1
        self.exp2 = exp2

class ExpresionDobleComilla(ExpresionCadena) :
    '''
        Esta clase representa una cadena entre comillas doble.
        Recibe como parámetro el valor del token procesado por el analizador léxico
    '''

    def __init__(self, val, tipo) :
        self.val = val
        self.tipo = tipo

class ExpresionCaracter(ExpresionCadena) :
    def __init__(self, val, tipo) :
        self.val = val
        self.tipo = tipo


class ExpresionLogica :
    '''
       Esta clase representa una Expresión de tipo Logica.
    '''
    
class ExpresionRelacionalBinaria(ExpresionLogica):
    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionLogicaBinaria(ExpresionLogica):
    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador

class ExpresionNot(ExpresionLogica) :
    def __init__(self, exp) :
        self.exp = exp

class ExpresionLogicaTF(ExpresionLogica):
    def __init__(self, val, tipo) :
        self.val = val
        self.tipo = tipo

class ExpresionSentencia:
    '''
       Esta clase representa una Expresión de tipo Sentencia.
    '''

class ExpresionIf(ExpresionSentencia):
    def __init__(self, exp, instrIfVerdadero = [], instrIfFalso = []) :
        self.exp= exp
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso

class ExpresionMatch(ExpresionSentencia):
    def __init__(self,exp,opciones):
        self.exp = exp
        self.opciones = opciones
        