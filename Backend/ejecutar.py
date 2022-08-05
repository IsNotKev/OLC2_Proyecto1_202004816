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
    else :
        print('Error: Expresión cadena no válida')