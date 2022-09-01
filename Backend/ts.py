from enum import Enum

class TIPO_DATO(Enum) :
    INT64 = 1
    FLOAT64 = 2
    BOOLEAN = 3
    STRING = 4
    ISTRING = 5
    CHAR = 6
    VOID = 7
    VECINT64 = 9
    VECFLOAT64 = 10
    VECBOOLEAN = 11
    VECSTRING = 12
    VECISTRING = 13
    VECCHAR = 14
    USIZE = 15

class TIPO_VAR(Enum):
    MUTABLE = 1
    INMUTABLE = 2

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo_var, tipo_dato,valor, capacity = None) :
        self.id = id
        self.tipo_var = tipo_var
        self.tipo_dato = tipo_dato
        self.valor = valor
        self.capacity = capacity

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
            if simbolo.tipo_dato != TIPO_DATO.VOID:
                if simbolo.tipo_dato == simbolo.valor.tipo:        
                    self.simbolos[simbolo.id] = simbolo
                elif simbolo.tipo_dato == TIPO_DATO.USIZE and simbolo.valor.tipo == TIPO_DATO.INT64 and simbolo.valor.val >= 0:
                    self.simbolos[simbolo.id] = simbolo
                else:
                    print('Error al asignar')
            else:
                simbolo.tipo_dato = simbolo.valor.tipo
                self.simbolos[simbolo.id] = simbolo

        else:
            self.simbolos[simbolo.id] = simbolo
    
    def agregarFuncion(self, funcion):
        self.funciones[funcion.id] = funcion
    
    def obtenerFuncion(self, id):
        if not id in self.funciones :
            print('Error: funcion ', id, ' no definida.')
        else:
            return self.funciones[id]

    def obtenerSimbolo(self, id) :
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
        else:
            return self.simbolos[id]

    def obtenerSimboloV(self, id, ubicacion):
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
        else:
            if len(ubicacion) > 1:
                return self.simboloRecursivo((self.simbolos[id]).valor.val[ubicacion[0]] , ubicacion)
            else:
                return (self.simbolos[id]).valor.val[ubicacion[0]]  

    def simboloRecursivo(self,vec,ubicacion):
        if len(ubicacion) > 1:
            ubicacion.pop(0)
            return self.simboloRecursivo(vec.val[ubicacion[0]], ubicacion)
        else:
            return vec


    def actualizarSimbolo(self, id, nval) :
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
        else :
            simboloAux = self.obtenerSimbolo(id)
            if simboloAux.tipo_var == TIPO_VAR.MUTABLE:
                if nval.tipo == simboloAux.tipo_dato:
                    simboloAux.valor = nval               
                    self.simbolos[simboloAux.id] = simboloAux
                elif simboloAux.tipo_dato == TIPO_DATO.USIZE and nval.tipo == TIPO_DATO.INT64 and nval.val >= 0:
                    simboloAux.valor = nval
                    self.simbolos[simboloAux.id] = simboloAux
                else:
                    print('Error al asignar')
            else:
                print('No se puede actualizar una variable Inmutable')