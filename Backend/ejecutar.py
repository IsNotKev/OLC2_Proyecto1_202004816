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
    return consola

def procesar_imprimir(instr, ts) :
    return '\n> ' + resolver_cadena(instr.cad, ts)

def resolver_cadena(expCad, ts) :
    if isinstance(expCad, ExpresionDobleComilla) :
        return expCad.val
    else:
        return str(resolver_expresion_aritmetica(expCad, ts).val)
    #else :
    #    print('Error: Expresión cadena no válida')

def resolver_expresion_aritmetica(expNum, ts) :
    if isinstance(expNum, ExpresionBinaria) :
        
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)

        if(exp1.tipo == exp2.tipo):
            if expNum.operador == OPERACION_ARITMETICA.MAS : return ExpresionNumero(exp1.val + exp2.val,exp1.tipo)
            if expNum.operador == OPERACION_ARITMETICA.MENOS : return ExpresionNumero(exp1.val - exp2.val,exp1.tipo)
            if expNum.operador == OPERACION_ARITMETICA.POR : return ExpresionNumero(exp1.val * exp2.val,exp1.tipo)
            if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : return ExpresionNumero(exp1.val / exp2.val,TIPO_DATO.FLOAT64)
            if expNum.operador == OPERACION_ARITMETICA.POTENCIA : return ExpresionNumero(exp1.val^exp2.val, exp1.tipo )
        else:
            return ExpresionDobleComilla("Error -> No son del mismo tipo")
        
    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return ExpresionNumero(exp.val*-1,exp.tipo)
    elif isinstance(expNum, ExpresionNumero) :
        return expNum
    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id)