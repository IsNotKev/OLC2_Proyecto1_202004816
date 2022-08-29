from ctypes.wintypes import FLOAT
from random import vonmisesvariate
from sre_parse import WHITESPACE
from ts import Simbolo
from ts import TIPO_DATO
from expresiones import *
from instrucciones import *
import ts as TS
import math


def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    consola = 'Ejecutando...'
    if instrucciones != None:
        for instr in instrucciones :
            if isinstance(instr, Imprimir) : consola += procesar_imprimir(instr, ts) 
            elif isinstance(instr,Definicion): procesar_definicion(instr,ts)
            elif isinstance(instr,Asignacion): procesar_asignacion(instr,ts)
            elif isinstance(instr, If): consola += procesar_if(instr,ts)
            elif isinstance(instr,IfElse): consola += procesar_ifelse(instr,ts)
            elif isinstance(instr,While): consola += procesar_while(instr,ts)
            elif isinstance(instr,Funcion): procesar_funcion(instr,ts)
            elif isinstance(instr,Llamado): consola += procesar_llamado(instr,ts)
            elif isinstance(instr,Match): consola += procesar_match(instr,ts)

    return consola

def procesar_match(instr,ts):
    val = resolver_expresion(instr.exp,ts)
    for opcion in instr.opciones:
        print(opcion.coincidencias)
        if opcion.coincidencias == TIPO_DATO.VOID:
            return procesar_instrucciones(opcion.instrucciones,ts)[13:]
        else:
            for coincidencia in opcion.coincidencias:
                cc = resolver_expresion(coincidencia,ts)
                if val.tipo == cc.tipo and val.val == cc.val:
                    return procesar_instrucciones(opcion.instrucciones,ts)[13:]
    
    return ""

def procesar_llamado(instr,ts):
    funcion = ts.obtenerFuncion(instr.id)

    ts_local = TS.TablaDeSimbolos()

    if len(instr.parametros) == len(funcion.parametros):
        for num in range(0,len(funcion.parametros),1):
            val = resolver_expresion(instr.parametros[num], ts)
            nsimbolo = Simbolo(funcion.parametros[num].id,funcion.parametros[num].tipo_var, funcion.parametros[num].tipo_dato,val)
            ts_local.agregarSimbolo(nsimbolo)

        return procesar_instrucciones(funcion.instrucciones,ts_local)[13:]
    else:
        print("Error en cantidad de Parametros")
        return "Error en cantidad de Parametros"

def procesar_funcion(instr,ts):
    ts.agregarFuncion(instr)

def procesar_while(instr, ts):
    val = resolver_expresion(instr.exp, ts)
    if val.tipo == TIPO_DATO.BOOLEAN:
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        consolaaux = ""
        while resolver_expresion(instr.exp, ts_local).val :          
            consolaaux += procesar_instrucciones(instr.instrucciones, ts_local)[13:]
        
        return consolaaux
    else:
        return "Error -> While necesita un bool"

def procesar_ifelse(instr, ts):
    val = resolver_expresion(instr.exp, ts)
    if val.tipo == TIPO_DATO.BOOLEAN:
        if val.val:
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            return procesar_instrucciones(instr.instrIfVerdadero, ts_local)[13:]
        else:
            if isinstance(instr.instrIfFalso, If) or isinstance(instr.instrIfFalso, IfElse):
                ts_local = TS.TablaDeSimbolos(ts.simbolos)
                return procesar_instrucciones([instr.instrIfFalso], ts_local)[13:]
            else:
                ts_local = TS.TablaDeSimbolos(ts.simbolos)
                return procesar_instrucciones(instr.instrIfFalso, ts_local)[13:]
    else:
        return "Error -> Debe de ser expresion booleana"

def procesar_if(instr, ts):
    val = resolver_expresion(instr.exp, ts)
    if val.tipo == TIPO_DATO.BOOLEAN:
        if val.val:
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            return procesar_instrucciones(instr.instrucciones, ts_local)[13:]
        else:
            return ""
    else:
        return "Error -> Debe de ser expresion booleana"

def procesar_imprimir(instr, ts) :
    if(len(instr.parametros)==0):
        return '\n> ' + resolver_expresion(instr.cad, ts).val
    else:
        cadena = resolver_expresion(instr.cad, ts).val
        cad_aux = ""
        error = False
        for param in instr.parametros:
            aux = resolver_expresion(param, ts)
            aux = to_text(aux,ts)

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
            if exp.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                if exp1.tipo == TIPO_DATO.INT64 :
                    return ExpresionNumero(math.trunc(exp1.val / exp2.val),exp1.tipo)
                else:
                    return ExpresionNumero(exp1.val / exp2.val,exp1.tipo)
            if exp.operador == OPERACION_ARITMETICA.MODULO : return ExpresionNumero(exp1.val % exp2.val,exp1.tipo)  
        elif exp1.tipo == TIPO_DATO.STRING and exp2.tipo == TIPO_DATO.ISTRING:
            return ExpresionDobleComilla(exp1.val + exp2.val,TIPO_DATO.STRING)
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
        if(exp.tipo == TIPO_DATO.INT64 or exp.tipo == TIPO_DATO.FLOAT64):
            return ExpresionNumero(exp.val*-1,exp.tipo)
        else:
            return ExpresionDobleComilla("Error -> No se puede operar", TIPO_DATO.STRING)
    elif isinstance(exp, ExpresionIf):
        cond = resolver_expresion(exp.exp,ts)
        if cond.tipo == TIPO_DATO.BOOLEAN:
            if cond.val:
                return resolver_expresion(exp.instrIfVerdadero,ts)
            else:
                return resolver_expresion(exp.instrIfFalso,ts)
        else:
            return ExpresionDobleComilla("Error -> Expresion If Necesita boolean", TIPO_DATO.STRING)
    elif isinstance(exp, ExpresionMatch):
        val = resolver_expresion(exp.exp,ts)
        for opcion in exp.opciones:
            if opcion.coincidencias == TIPO_DATO.VOID:
                return resolver_expresion(opcion.instrucciones,ts)
            else:
                for coincidencia in opcion.coincidencias:
                    cc = resolver_expresion(coincidencia,ts)
                    if cc.tipo == val.tipo and cc.val == val.val:
                        return resolver_expresion(opcion.instrucciones,ts)
        
        print("No hay coincidencias")
        return ExpresionDobleComilla("No hay coincidencias", TIPO_DATO.STRING)
    elif isinstance(exp,ToString):
        val = resolver_expresion(exp.dato,ts)
        return ExpresionDobleComilla(to_text(val),TIPO_DATO.STRING)
    elif isinstance(exp,Abs):
        val = resolver_expresion(exp.dato,ts)
        if val.tipo == TIPO_DATO.INT64 or val.tipo == TIPO_DATO.FLOAT64:
            return ExpresionNumero(abs(val.val), val.tipo)
        else:
            return ExpresionDobleComilla("No se puede realizar la funcion abs.", TIPO_DATO.STRING)
    elif isinstance(exp,Sqrt):
        val = resolver_expresion(exp.dato,ts)
        if val.tipo == TIPO_DATO.INT64 or val.tipo == TIPO_DATO.FLOAT64:
            return ExpresionNumero(math.sqrt(val.val), TIPO_DATO.FLOAT64)
        else:
            return ExpresionDobleComilla("No se puede realizar la funcion sqrt.", TIPO_DATO.STRING)
    elif isinstance(exp, Casteo):         
        return casteo(exp,ts)
    elif isinstance(exp, ExpresionNumero) or isinstance(exp, ExpresionLogicaTF) or isinstance(exp, ExpresionDobleComilla) or isinstance(exp,ExpresionCaracter):
        return exp
    elif isinstance(exp, ExpresionIdentificador) :
        return ts.obtenerSimbolo(exp.id).valor
    elif isinstance(exp,ExpresionVec):
        if type(exp.val) == type([]):
            return exp
        elif isinstance(exp.val,ValoresRepetidos):
            cant = resolver_expresion(exp.val.cant,ts)
            if cant.tipo == TIPO_DATO.INT64:
                val = []
                dato = resolver_expresion(exp.val.dato,ts)
                for i in range(0,cant.val):
                    val.append(dato)
                return ExpresionVec(val, TIPO_DATO.VOID)
    elif isinstance(exp,ExpresionIdVectorial):
        ub = resolver_expresion(exp.ubicacion,ts)
        if ub.tipo == TIPO_DATO.INT64 and ub.val >= 0:
            return ts.obtenerSimboloV(exp.id, ub.val)
        else:
            print('Error: Necesita un entero positivo')
    else :
        print('Error: Expresión no válida')

def casteo(exp,ts):
    val = resolver_expresion(exp.dato,ts) 

    if val.tipo == exp.casteo:
        return val
    elif val.tipo == TIPO_DATO.INT64 and exp.casteo == TIPO_DATO.FLOAT64:
        return ExpresionNumero(val.val, TIPO_DATO.FLOAT64)
    elif val.tipo == TIPO_DATO.FLOAT64 and exp.casteo == TIPO_DATO.INT64:
        return ExpresionNumero(math.trunc(val.val), TIPO_DATO.INT64)
    elif val.tipo == TIPO_DATO.CHAR and exp.casteo == TIPO_DATO.INT64:
        return ExpresionNumero( ord(val.val), TIPO_DATO.INT64)
    
    return ExpresionDobleComilla("Error -> No se puede realizar casteo", TIPO_DATO.STRING)

def procesar_definicion(instr, ts):   
    val = resolver_expresion(instr.dato, ts)  

    if val.tipo == TIPO_DATO.VOID and type(val.val) == type([]):

            if comprobar_vector(val.val,ts,TIPO_DATO.INT64):
                val.tipo = TIPO_DATO.VECINT64
            elif comprobar_vector(val.val,ts,TIPO_DATO.FLOAT64):
                val.tipo = TIPO_DATO.VECFLOAT64
            elif comprobar_vector(val.val,ts,TIPO_DATO.BOOLEAN):   
                val.tipo = TIPO_DATO.VECBOOLEAN
            elif comprobar_vector(val.val,ts,TIPO_DATO.CHAR):
                val.tipo = TIPO_DATO.VECCHAR
            elif comprobar_vector(val.val,ts,TIPO_DATO.ISTRING):
                val.tipo = TIPO_DATO.VECISTRING
            elif comprobar_vector(val.val,ts,TIPO_DATO.STRING):
                val.tipo = TIPO_DATO.VECSTRING
            else:
                print('Vector Incorrecto')

    simbolo = TS.Simbolo(instr.id,instr.tipo_var,instr.tipo_dato,val)
    ts.agregarSimbolo(simbolo)

def comprobar_vector(vector,ts,tipo):
    for n in vector:
        if resolver_expresion(n,ts).tipo != tipo:
            return False
    
    return True

def to_text(valor,ts):
    if(isinstance(valor, ExpresionLogicaTF)):
        if(valor.val):
           return "true"
        else:
           return "false"
    elif isinstance(valor,ExpresionVec):
        tt = '['
        for v in valor.val:
            tt += to_text(v,ts) + ', '
        tt = tt[:-2]
        tt += ']'
        return tt
    else:
        return str(valor.val)

def procesar_asignacion(instr,ts):
    val = resolver_expresion(instr.exp, ts)
    ts.actualizarSimbolo(instr.id, val)