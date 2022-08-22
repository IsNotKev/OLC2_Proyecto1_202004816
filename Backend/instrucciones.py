class Instruccion:
    '''This is an abstract class'''

class Imprimir(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''
    def __init__(self,  cad, parametros) :
        self.cad = cad
        self.parametros = parametros

class Definicion(Instruccion) :
    '''
        Esta clase representa la instrucción de definición de variables.
    '''

    def __init__(self, id, tipo_var, tipo_dato, dato) :
        self.id = id
        self.tipo_var = tipo_var
        self.tipo_dato = tipo_dato
        self.dato = dato

class Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, exp) :
        self.id = id
        self.exp = exp

class If(Instruccion) : 
    def __init__(self, exp, instrucciones = []) :
        self.exp = exp
        self.instrucciones = instrucciones

class IfElse(Instruccion) : 

    def __init__(self, exp, instrIfVerdadero = [], instrIfFalso = []) :
        self.exp= exp
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso

class While(Instruccion):
    def __init__(self, exp, instrucciones = []):
        self.exp = exp
        self.instrucciones = instrucciones

class Funcion(Instruccion):
    def __init__(self, id, parametros,tipo_dato, instrucciones):
        self.id = id
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.tipo_dato = tipo_dato

class Parametro(Instruccion):
    def __init__(self, id, tipo_dato,tipo_var):
        self.id = id
        self.tipo_dato = tipo_dato
        self.tipo_var = tipo_var

class Llamado(Instruccion):
    def __init__(self,id,parametros):
        self.id = id
        self.parametros = parametros

class Match(Instruccion):
    def __init__(self, exp, opciones):
        self.exp = exp
        self.opciones = opciones

class OpcionMatch(Instruccion):
    def __init__(self, coincidencias, instrucciones):
        self.coincidencias = coincidencias
        self.instrucciones = instrucciones

class ToString(Instruccion):
    def __init__(self, dato):
        self.dato = dato