from doctest import ELLIPSIS_MARKER
from enum import Enum

class TIPO_DATO(Enum) :
    INT64 = 1
    FLOAT64 = 2
    BOOLEAN = 3
    STRING = 4
    ISTRING = 5
    CHAR = 6
    VOID = 7

class TIPO_VAR(Enum):
    MUTABLE = 1
    INMUTABLE = 2

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo_var, tipo_dato,valor) :
        self.id = id
        self.tipo_var = tipo_var
        self.tipo_dato = tipo_dato
        self.valor = valor

class Funcion():
    def __init__(self, id, parametros, instrucciones, tipo_dato):
        self.id = id
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.tipo_dato = tipo_dato
        

class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = {}, funciones = {}) :
        self.simbolos = simbolos
        self.funciones = funciones

    def agregarSimbolo(self, simbolo) :
        if simbolo.valor != None:
            if simbolo.tipo_dato == simbolo.valor.tipo:        
                self.simbolos[simbolo.id] = simbolo
            else:
                print('Error al asignar')
        else:
            self.simbolos[simbolo.id] = simbolo
    
    def obtenerSimbolo(self, id) :
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')

        return self.simbolos[id]

    def actualizarSimbolo(self, id, nval) :
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
        else :
            simboloAux = self.obtenerSimbolo(id)
            if simboloAux.tipo_var == TIPO_VAR.MUTABLE:
                if nval.tipo == simboloAux.tipo_dato:
                    simboloAux.valor = nval               
                    self.simbolos[simboloAux.id] = simboloAux
                else:
                    print('Error al asignar')
            else:
                print('No se puede actualizar una variable Inmutable')