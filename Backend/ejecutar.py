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
    if(len(instr.parametros)==0):
        return '\n> ' + resolver_expresion(instr.cad, ts).val
    else:
        cadena = resolver_expresion(instr.cad, ts).val
        cad_aux = ""
        error = False
        for param in instr.parametros:
            aux = resolver_expresion(param, ts)
            print(param)
            if(isinstance(aux, ExpresionLogicaTF)):
                if(aux.val):
                   aux = "true"
                else:
                   aux = "false"
            else:
                aux = str(aux.val)

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


#def resolver_cadena(expCad, ts) :
#  if isinstance(expCad, ExpresionDobleComilla) :
#       return expCad.val
#   else :
#       print('Error: Expresión cadena no válida')

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
    elif isinstance(exp, ExpresionLogicaTF):
        return exp
    elif isinstance(exp, ExpresionDobleComilla) :
        return exp
    elif isinstance(exp, ExpresionBinaria) :
        
        exp1 = resolver_expresion(exp.exp1, ts)
        exp2 = resolver_expresion(exp.exp2, ts)

        if(exp1.tipo == exp2.tipo):
            if exp.operador == OPERACION_ARITMETICA.MAS : return ExpresionNumero(exp1.val + exp2.val,exp1.tipo)
            if exp.operador == OPERACION_ARITMETICA.MENOS : return ExpresionNumero(exp1.val - exp2.val,exp1.tipo)
            if exp.operador == OPERACION_ARITMETICA.POR : return ExpresionNumero(exp1.val * exp2.val,exp1.tipo)
            if exp.operador == OPERACION_ARITMETICA.DIVIDIDO : return ExpresionNumero(exp1.val / exp2.val,TIPO_DATO.FLOAT64)
            if exp.operador == OPERACION_ARITMETICA.MODULO : return ExpresionNumero(exp1.val % exp2.val,exp1.tipo)  
        else:
            return ExpresionDobleComilla("Error -> No son del mismo tipo", TIPO_DATO.STRING)
        
    elif isinstance(exp, ExpresionPotencia) :
        exp1 = resolver_expresion(exp.exp1, ts)
        exp2 = resolver_expresion(exp.exp2, ts)

        if(exp1.tipo == exp2.tipo):
            if(exp1.tipo == exp.tipo):
                return ExpresionNumero(exp1.val ** exp2.val, exp.tipo)
        
        return ExpresionDobleComilla("Error -> No son del mismo tipo", TIPO_DATO.STRING)
       
    elif isinstance(exp, ExpresionNegativo) :
        exp = resolver_expresion(exp.exp, ts)
        return ExpresionNumero(exp.val*-1,exp.tipo)
    elif isinstance(exp, ExpresionNumero) :
        return exp
    elif isinstance(exp, ExpresionIdentificador) :
        return ts.obtener(exp.id)
    else :
        print('Error: Expresión cadena no válida')


'''def resolver_expresion_aritmetica(expNum, ts) :
    if isinstance(expNum, ExpresionBinaria) :
        
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)

        if(exp1.tipo == exp2.tipo):
            if expNum.operador == OPERACION_ARITMETICA.MAS : return ExpresionNumero(exp1.val + exp2.val,exp1.tipo)
            if expNum.operador == OPERACION_ARITMETICA.MENOS : return ExpresionNumero(exp1.val - exp2.val,exp1.tipo)
            if expNum.operador == OPERACION_ARITMETICA.POR : return ExpresionNumero(exp1.val * exp2.val,exp1.tipo)
            if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : return ExpresionNumero(exp1.val / exp2.val,TIPO_DATO.FLOAT64)
            if expNum.operador == OPERACION_ARITMETICA.MODULO : return ExpresionNumero(exp1.val % exp2.val,exp1.tipo)  
        else:
            return ExpresionDobleComilla("Error -> No son del mismo tipo")
        
    elif isinstance(expNum, ExpresionPotencia) :
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)

        if(exp1.tipo == exp2.tipo):
            if(exp1.tipo == expNum.tipo):
                return ExpresionNumero(exp1.val ** exp2.val, expNum.tipo)
        
        return ExpresionDobleComilla("Error -> No son del mismo tipo")
       
    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return ExpresionNumero(exp.val*-1,exp.tipo)
    elif isinstance(expNum, ExpresionNumero) :
        return expNum
    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id)'''