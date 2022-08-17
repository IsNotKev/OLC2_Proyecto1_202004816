from ts import Simbolo
from ts import TIPO_DATO
from expresiones import *
from instrucciones import *
import ts as TS


def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    consola = 'Ejecutando...'
    print(instrucciones)
    if instrucciones != None:
        for instr in instrucciones :
            if isinstance(instr, Imprimir) : consola += procesar_imprimir(instr, ts) 
            elif isinstance(instr,Definicion): procesar_definicion(instr,ts)
            elif isinstance(instr,Asignacion): procesar_asignacion(instr,ts)

    return consola

def procesar_imprimir(instr, ts) :
    if(len(instr.parametros)==0):
        return '\n> ' + resolver_expresion(instr.cad, ts).val
    else:
        cadena = resolver_expresion(instr.cad, ts).val
        cad_aux = ""
        error = False
        for param in instr.parametros:
            aux = resolver_expresion(param, ts)
            aux = to_text(aux)

            escribir = True
            primero = False
            for c in cadena:
                if(escribir):
                    if(c == "{" and not primero):
                        escribir = False
                    else:
                        cad_aux += c
                else:
                    if(c == "}"):
                        escribir = True
                        primero = True
                        cad_aux = cad_aux + aux
                    elif(c == "{"):
                        escribir = True
                        cad_aux = cad_aux + "{{"
                        error = False
                        primero = False
                    elif(c != " "):
                        error = True
                        cad_aux = "> Error dentro de {}"
                        break

            cadena = cad_aux
            cad_aux = ""    

            if(error):
                break

        return '\n> ' + cadena

def resolver_expresion(exp, ts):
    if isinstance(exp, ExpresionRelacionalBinaria):
        exp1 = resolver_expresion(exp.exp1, ts)
        exp2 = resolver_expresion(exp.exp2, ts)
        if(exp1.tipo == exp2.tipo):
            if exp.operador == OPERACION_LOGICA.MAYOR_QUE : return ExpresionLogicaTF(exp1.val > exp2.val, TIPO_DATO.BOOLEAN)
            if exp.operador == OPERACION_LOGICA.MENOR_QUE : return ExpresionLogicaTF(exp1.val < exp2.val, TIPO_DATO.BOOLEAN)
            if exp.operador == OPERACION_LOGICA.IGUAL : return ExpresionLogicaTF(exp1.val == exp2.val, TIPO_DATO.BOOLEAN)
            if exp.operador == OPERACION_LOGICA.DIFERENTE : return ExpresionLogicaTF(exp1.val != exp2.val, TIPO_DATO.BOOLEAN)
            if exp.operador == OPERACION_LOGICA.MAYORIGUAL : return ExpresionLogicaTF(exp1.val >= exp2.val, TIPO_DATO.BOOLEAN)
            if exp.operador == OPERACION_LOGICA.MENORIGUAL : return ExpresionLogicaTF(exp1.val <= exp2.val, TIPO_DATO.BOOLEAN)
        else:
            return ExpresionDobleComilla("Error -> No son del mismo tipo", TIPO_DATO.STRING)
    elif isinstance(exp, ExpresionLogicaBinaria):
        exp1 = resolver_expresion(exp.exp1, ts)
        exp2 = resolver_expresion(exp.exp2, ts)
        if(exp1.tipo == TIPO_DATO.BOOLEAN and exp2.tipo == TIPO_DATO.BOOLEAN):
            if exp.operador == OPERACION_LOGICA.OR : return ExpresionLogicaTF(exp1.val or exp2.val, TIPO_DATO.BOOLEAN)
            if exp.operador == OPERACION_LOGICA.AND : return ExpresionLogicaTF(exp1.val and exp2.val, TIPO_DATO.BOOLEAN)
        else:
            return ExpresionDobleComilla("Error -> No son del tipo boolean", TIPO_DATO.STRING)
    elif isinstance(exp, ExpresionNot):
        exp1 = resolver_expresion(exp.exp, ts)
        if(exp1.tipo == TIPO_DATO.BOOLEAN):
            return ExpresionLogicaTF(not exp1.val, TIPO_DATO.BOOLEAN)
        else:
            return ExpresionDobleComilla("Error -> No son de tipo boolean", TIPO_DATO.STRING)
    elif isinstance(exp, ExpresionBinaria) :
        
        exp1 = resolver_expresion(exp.exp1, ts)
        exp2 = resolver_expresion(exp.exp2, ts)

        if((exp1.tipo == TIPO_DATO.INT64 and exp2.tipo == TIPO_DATO.INT64 ) or (exp1.tipo == TIPO_DATO.FLOAT64 and exp2.tipo == TIPO_DATO.FLOAT64 )):
            if exp.operador == OPERACION_ARITMETICA.MAS : return ExpresionNumero(exp1.val + exp2.val,exp1.tipo)
            if exp.operador == OPERACION_ARITMETICA.MENOS : return ExpresionNumero(exp1.val - exp2.val,exp1.tipo)
            if exp.operador == OPERACION_ARITMETICA.POR : return ExpresionNumero(exp1.val * exp2.val,exp1.tipo)
            if exp.operador == OPERACION_ARITMETICA.DIVIDIDO : return ExpresionNumero(exp1.val / exp2.val,TIPO_DATO.FLOAT64)
            if exp.operador == OPERACION_ARITMETICA.MODULO : return ExpresionNumero(exp1.val % exp2.val,exp1.tipo)  
        else:
            return ExpresionDobleComilla("Error -> No se puede operar", TIPO_DATO.STRING)
        
    elif isinstance(exp, ExpresionPotencia) :
        exp1 = resolver_expresion(exp.exp1, ts)
        exp2 = resolver_expresion(exp.exp2, ts)

        if((exp1.tipo == TIPO_DATO.INT64 and exp2.tipo == TIPO_DATO.INT64 ) or (exp1.tipo == TIPO_DATO.FLOAT64 and exp2.tipo == TIPO_DATO.FLOAT64 )):
            if(exp1.tipo == exp.tipo):
                return ExpresionNumero(exp1.val ** exp2.val, exp.tipo)
            else:
                return ExpresionDobleComilla("Error -> No es del tipo correcto", TIPO_DATO.STRING)
        else:
            return ExpresionDobleComilla("Error -> No se puede operar", TIPO_DATO.STRING)
                  
    elif isinstance(exp, ExpresionNegativo) :
        exp = resolver_expresion(exp.exp, ts)
        if(exp.tipo == TIPO_DATO.INT64 or exp1.tipo == TIPO_DATO.FLOAT64):
            return ExpresionNumero(exp.val*-1,exp.tipo)
        else:
            return ExpresionDobleComilla("Error -> No se puede operar", TIPO_DATO.STRING)
    elif isinstance(exp, ExpresionNumero) or isinstance(exp, ExpresionLogicaTF) or isinstance(exp, ExpresionDobleComilla):
        return exp
    elif isinstance(exp, ExpresionIdentificador) :
        return ts.obtenerSimbolo(exp.id).valor
    else :
        print('Error: Expresión no válida')

def procesar_definicion(instr, ts):
    simbolo = TS.Simbolo(instr.id,instr.tipo_var,instr.tipo_dato,instr.dato)
    ts.agregarSimbolo(simbolo)

def to_text(valor):
    if(isinstance(valor, ExpresionLogicaTF)):
        if(valor.val):
           return "true"
        else:
           return "false"
    else:
        return str(valor.val)

def procesar_asignacion(instr,ts):
    val = resolver_expresion(instr.exp, ts)
    ts.actualizarSimbolo(instr.id, val)