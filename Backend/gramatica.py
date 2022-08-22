
reservadas = {
    'println': 'PRINTLN',
    'powf'   : 'POWF',
    'pow'    : 'POW',
    'i64'    : 'INT',
    'f64'    : 'FLOAT',
    'bool'   : 'BOOLEAN',
    'char'   : 'CHAR',
    'str'    : 'ISTRING',
    'String' : 'STRING',
    'true'   : 'TRUE',
    'false'  : 'FALSE',
    'let'    : 'LET',
    'mut'    : 'MUT',
    'if'     : 'IF',
    'else'   : 'ELSE',
    'while'  : 'WHILE',
    'for'    : 'FOR',
    'in'     : 'IN',
    'fn'     : 'FN'
}

tokens  = [
#    'FLECHA',
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
    'ADMIR',
    'I'
] + list(reservadas.values())

# Tokens
#t_FLECHA    = r'->'
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
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_OR        = r'\|\|'
t_AND       = r'&&'
t_ADMIR     = r'!'
t_I         = r'&'


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
from ts import TIPO_VAR

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
    '''instruccion      :   imprimir_instr
                        |   definicion_instr 
                        |   asignacion_instr
                        |   if_instr
                        |   while_instr
                        |   funcion_instr
                        |   llamado_instr'''
    t[0] = t[1]

def p_llamado_instr(t):
    'llamado_instr      :   ID PARIZQ PARDER PTCOMA'
    t[0] = Llamado(t[1],[])

def p_llamado_instr_CP(t):
    'llamado_instr      :   ID PARIZQ llparams PARDER PTCOMA'
    t[0] = Llamado(t[1],t[3])

def p_lllamadoparams(t):
    'llparams           :   llparams COMA expresion'
    t[1].append(t[3])
    t[0] = t[1]

def p_llamadoparams(t):
    'llparams           :   expresion'
    t[0] = [t[1]]

def p_funcion_intr_SP(t):
    'funcion_instr    :   FN ID PARIZQ PARDER statement'
    t[0] = Funcion(t[2],[],TIPO_DATO.VOID,t[5])

#def p_funcion_ctipo_intr_SP(t):
#    'funcion_instr    :   FN ID PARIZQ PARDER FLECHA tipos statement'
#    t[0] = Funcion(t[2],[],t[6],t[7])

def p_funcion_intr(t):
    'funcion_instr    :   FN ID PARIZQ fparam PARDER statement'
    t[0] = Funcion(t[2],t[4],TIPO_DATO.VOID,t[6])

#def p_funcion_ctipo_intr(t):
#    'funcion_instr    :   FN ID PARIZQ fparam PARDER FLECHA tipos statement'
#    t[0] = Funcion(t[2],t[4],t[7],t[8])

def p_listafparams(t):
    'fparam         :       fparam COMA fparametro'
    t[1].append(t[3])
    t[0] = t[1]

def p_fparams(t):
    'fparam         :       fparametro'
    t[0] = [t[1]]

def p_fparametro(t):
    'fparametro     :       ID DOSPUNTOS tipos'
    t[0] = Parametro(t[1],t[3],TIPO_VAR.INMUTABLE)

def p_fparametro_mut(t):
    'fparametro     :       MUT ID DOSPUNTOS tipos'
    t[0] = Parametro(t[2],t[4],TIPO_VAR.MUTABLE)

def p_while_instr(t) :
    'while_instr     : WHILE expresion statement'
    t[0] =While(t[2], t[3])

def p_if_instr(t) :
    'if_instr           : IF expresion statement'
    t[0] =If(t[2], t[3])

def p_if_else_instr(t) :
    'if_instr     : IF expresion statement ELSE statement'
    t[0] =IfElse(t[2], t[3], t[5])

def p_if_elseif_instr(t) :
    'if_instr     : IF expresion statement ELSE if_instr'
    t[0] =IfElse(t[2], t[3], t[5])

def p_statement(t):
    'statement          :   LLAVIZQ instrucciones LLAVDER'
    t[0] = t[2]

def p_statement_vacio(t):  
    'statement          :   LLAVIZQ LLAVDER'
    t[0] = []

def p_asignacion_instr(t) :
    'asignacion_instr   : ID IGUAL expresion PTCOMA'
    t[0] = Asignacion(t[1], t[3])

def p_instruccion_definicionMT(t):
    '''definicion_instr :   LET MUT ID DOSPUNTOS tipos IGUAL expresion PTCOMA'''
    t[0] = Definicion(t[3],TIPO_VAR.MUTABLE, t[5],t[7])

def p_instruccion_definicionIT(t):
    '''definicion_instr :   LET ID DOSPUNTOS tipos IGUAL expresion PTCOMA'''
    t[0] = Definicion(t[2],TIPO_VAR.INMUTABLE, t[4], t[6])

def p_instruccion_definicionM(t):
    '''definicion_instr :   LET MUT ID IGUAL expresion PTCOMA'''
    t[0] = Definicion(t[3],TIPO_VAR.MUTABLE, TIPO_DATO.VOID, t[5])

def p_instruccion_definicionI(t):
    '''definicion_instr :   LET ID IGUAL expresion PTCOMA'''
    t[0] = Definicion(t[2],TIPO_VAR.INMUTABLE,TIPO_DATO.VOID,t[4])

def p_tiposInt(t):
    '''tipos            :   INT'''
    t[0] = TIPO_DATO.INT64

def p_tiposFloat(t):
    '''tipos            :   FLOAT'''
    t[0] = TIPO_DATO.FLOAT64

def p_tiposBool(t):
    '''tipos            :   BOOLEAN'''
    t[0] = TIPO_DATO.BOOLEAN

def p_tiposChar(t):
    '''tipos            :   CHAR'''
    t[0] = TIPO_DATO.CHAR

def p_tiposStr(t):
    '''tipos            :   STRING'''
    t[0] = TIPO_DATO.STRING

def p_tiposIStr(t):
    '''tipos            :   I ISTRING'''
    t[0] = TIPO_DATO.ISTRING

def p_instruccion_imprimir(t) :
    '''imprimir_instr     : PRINTLN ADMIR PARIZQ CADENA PARDER PTCOMA'''
    t[0] =Imprimir(ExpresionDobleComilla(t[4], TIPO_DATO.ISTRING),parametros=[])

def p_instruccion_imprimir_p(t) :
    '''imprimir_instr     : PRINTLN ADMIR PARIZQ CADENA pparam PARDER PTCOMA'''
    t[0] =Imprimir(ExpresionDobleComilla(t[4], TIPO_DATO.ISTRING), t[5])

def p_lpparam(t):
    '''pparam                : pparam COMA expresion'''
    t[1].append(t[3])
    t[0] = t[1]

def p_pparam(t):
    '''pparam                :  COMA expresion'''
    t[0] = [t[2]]

def p_expresion_binaria(t):
    '''expresion        : expresion MAS expresion
                        | expresion MENOS expresion
                        | expresion POR expresion
                        | expresion DIVIDIDO expresion
                        | expresion MODULO expresion'''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    elif t[2] == '*': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR)
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)
    elif t[2] == '%': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MODULO)

def p_expresion_potencia_I(t):
    'expresion : INT DOSPUNTOS DOSPUNTOS POW PARIZQ expresion COMA expresion PARDER'
    t[0] = ExpresionPotencia(t[6],t[8],TIPO_DATO.INT64)

def p_expresion_potencia_F(t):
    'expresion : FLOAT DOSPUNTOS DOSPUNTOS POWF PARIZQ expresion COMA expresion PARDER'
    t[0] = ExpresionPotencia(t[6],t[8],TIPO_DATO.FLOAT64)

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = ExpresionNegativo(t[2])

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion : ENTERO'''
    t[0] = ExpresionNumero(t[1],TIPO_DATO.INT64)

def p_expresion_numberd(t):
    '''expresion : DECIMAL'''
    t[0] = ExpresionNumero(t[1],TIPO_DATO.FLOAT64)

def p_expresion_cadena(t) :
    'expresion     : CADENA'
    t[0] = ExpresionDobleComilla(t[1],TIPO_DATO.ISTRING)

def p_expresion_logicaT(t) :
    'expresion     : TRUE'
    t[0] = ExpresionLogicaTF(True, TIPO_DATO.BOOLEAN)

def p_expresion_logicaF(t) :
    'expresion    : FALSE'
    t[0] = ExpresionLogicaTF(False, TIPO_DATO.BOOLEAN)

def p_expresion_id(t):
    'expresion     : ID'
    t[0] = ExpresionIdentificador(t[1])

def p_expresion_relacional(t):
    '''expresion     :      expresion MAYQUE expresion
                        |   expresion MENQUE expresion
                        |   expresion IGUALQUE expresion
                        |   expresion NIGUALQUE expresion
                        |   expresion MAYORIGUAL expresion
                        |   expresion MENORIGUAL expresion
                        |   expresion OR expresion
                        |   expresion AND expresion''' 
    
    if t[2] == '>'    : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE)
    elif t[2] == '<'  : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MENOR_QUE)
    elif t[2] == '==' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.IGUAL)
    elif t[2] == '!=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.DIFERENTE)
    elif t[2] == '>=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MAYORIGUAL)
    elif t[2] == '<=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MENORIGUAL)
    elif t[2] == '||'     : t[0] = ExpresionLogicaBinaria(t[1],t[3], OPERACION_LOGICA.OR)
    elif t[2] == '&&'   : t[0] = ExpresionLogicaBinaria(t[1],t[3], OPERACION_LOGICA.AND)

def p_expresion_logica_unaria(t):
    'expresion       :   ADMIR expresion %prec NOT'
    t[0] = ExpresionNot(t[2])

# Error sintactico
def p_error(p):
    print(f'Error de sintaxis {p.value!r} en {p.lineno!r}')

from ply.yacc import yacc
parser = yacc(debug=True)


def parse(input) :
    return parser.parse(input)