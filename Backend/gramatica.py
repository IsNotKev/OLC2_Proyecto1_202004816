

reservadas = {
    'println': 'PRINTLN',
    'powf'   : 'POWF',
    'pow'    : 'POW',
    'i64'    : 'INT',
    'f64'    : 'FLOAT',
    'bool'   : 'BOOLEAN',
    'char'   : 'CHAR',
    '&str'   : 'ISTRING',
    'String' : 'STRING',
    'true'   : 'TRUE',
    'false'  : 'FALSE'
}

tokens  = [
    'PTCOMA',
    'DOSPUNTOS',
    'COMA',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    #'CONCAT',
    'MAYORIGUAL',
    'MENORIGUAL',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'OR',
    'AND',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
    'ADMIR'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_DOSPUNTOS = r':'
t_COMA      = r','
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_MODULO    = r'%'
#t_CONCAT    = r'&'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_OR        = r'\|\|'
t_AND       = r'&&'
t_ADMIR     = r'!'


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')    # Check for reserved words
     return t

def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print(f'Caracter no reconocido {t.value[0]!r} en la linea {t.lexer.lineno}')
    t.lexer.skip(1)

# Construyendo el analizador léxico
from ply import lex
lex.lex()

############################################# PARSER #######################################

#Precedencia
precedence = (
    #('left','CONCAT'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','MODULO'),
    ('right','UMENOS', 'NOT')
    )

from expresiones import *
from instrucciones import *
from ts import TIPO_DATO

def p_init(t) :
    'inicio            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      :   imprimir_instr'''
    t[0] = t[1]

def p_instruccion_imprimir(t) :
    '''imprimir_instr     : PRINTLN ADMIR PARIZQ CADENA PARDER PTCOMA'''
    t[0] =Imprimir(ExpresionDobleComilla(t[4], TIPO_DATO.STRING),parametros=[])

def p_instruccion_imprimir_p(t) :
    '''imprimir_instr     : PRINTLN ADMIR PARIZQ CADENA pparam PARDER PTCOMA'''
    t[0] =Imprimir(ExpresionDobleComilla(t[4], TIPO_DATO.STRING), t[5])

def p_lpparam(t):
    '''pparam                : pparam COMA expresion_cadena 
                            |  pparam COMA expresion_numerica 
                            |  pparam COMA expresion_relacional
                            |  pparam COMA expresion_logica'''
    t[1].append(t[3])
    t[0] = t[1]

def p_pparam(t):
    '''pparam                :  COMA expresion_cadena 
                            |   COMA expresion_numerica 
                            |   COMA expresion_relacional
                            |   COMA expresion_logica'''
    t[0] = [t[2]]

def p_expresion_binaria(t):
    '''expresion_numerica : expresion_numerica MAS expresion_numerica
                        | expresion_numerica MENOS expresion_numerica
                        | expresion_numerica POR expresion_numerica
                        | expresion_numerica DIVIDIDO expresion_numerica
                        | expresion_numerica MODULO expresion_numerica'''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    elif t[2] == '*': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR)
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)
    elif t[2] == '%': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MODULO)

def p_expresion_potencia_I(t):
    'expresion_numerica : INT DOSPUNTOS DOSPUNTOS POW PARIZQ expresion_numerica COMA expresion_numerica PARDER'
    t[0] = ExpresionPotencia(t[6],t[8],TIPO_DATO.INT64)

def p_expresion_potencia_F(t):
    'expresion_numerica : FLOAT DOSPUNTOS DOSPUNTOS POWF PARIZQ expresion_numerica COMA expresion_numerica PARDER'
    t[0] = ExpresionPotencia(t[6],t[8],TIPO_DATO.FLOAT64)

def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion_numerica %prec UMENOS'
    t[0] = ExpresionNegativo(t[2])

def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion_numerica PARDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion_numerica : ENTERO'''
    t[0] = ExpresionNumero(t[1],TIPO_DATO.INT64)

def p_expresion_numberd(t):
    '''expresion_numerica : DECIMAL'''
    t[0] = ExpresionNumero(t[1],TIPO_DATO.FLOAT64)

def p_expresion_cadena(t) :
    'expresion_cadena     : CADENA'
    t[0] = ExpresionDobleComilla(t[1],TIPO_DATO.STRING)

def p_expresion_logicaT(t) :
    'expresion_logica     : TRUE'
    t[0] = ExpresionLogicaTF(True, TIPO_DATO.BOOLEAN)

def p_expresion_logicaF(t) :
    'expresion_logica    : FALSE'
    t[0] = ExpresionLogicaTF(False, TIPO_DATO.BOOLEAN)

def p_expresion_relacionalD(t) :
    '''expresion_relacional    : expresion_cadena
                            |   expresion_numerica
                            |   expresion_logica'''
    t[0] = t[1]

def p_expresion_agrupacionRelacional(t):
    'expresion_relacional : PARIZQ expresion_relacional PARDER'  
    t[0] = t[2]

def p_expresion_relacional(t):
    '''expresion_relacional     : expresion_relacional MAYQUE expresion_relacional
                            |   expresion_relacional MENQUE expresion_relacional
                            |   expresion_relacional IGUALQUE expresion_relacional
                            |   expresion_relacional NIGUALQUE expresion_relacional
                            |   expresion_relacional MAYORIGUAL expresion_relacional
                            |   expresion_relacional MENORIGUAL expresion_relacional
                            |   expresion_relacional OR expresion_relacional
                            |   expresion_relacional AND expresion_relacional''' 
    
    if t[2] == '>'    : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE)
    elif t[2] == '<'  : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MENOR_QUE)
    elif t[2] == '==' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.IGUAL)
    elif t[2] == '!=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.DIFERENTE)
    elif t[2] == '>=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MAYORIGUAL)
    elif t[2] == '<=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MENORIGUAL)
    elif t[2] == '||'     : t[0] = ExpresionLogicaBinaria(t[1],t[3], OPERACION_LOGICA.OR)
    elif t[2] == '&&'   : t[0] = ExpresionLogicaBinaria(t[1],t[3], OPERACION_LOGICA.AND)

def p_expresion_logica_unaria(t):
    'expresion_relacional       :   ADMIR expresion_relacional %prec NOT'
    t[0] = ExpresionNot(t[2])

# Error sintactico
def p_error(p):
    print(f'Error de sintaxis {p.value!r}')

from ply.yacc import yacc
parser = yacc(debug=True)


def parse(input) :
    return parser.parse(input)