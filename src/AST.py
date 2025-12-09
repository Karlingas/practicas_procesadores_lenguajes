#!/usr/bin/env python
from tablaSimbolos import tablaSimbolos

# Instancia global de la tabla de símbolos para uso en los nodos
tablasimbolos = tablaSimbolos()

class AST:
    def __str__(self):
        return self.arbol()
    
    def compsem(self):
        # Método base, por defecto no hace nada
        pass

# Nodo para errores o producciones vacías
class NodoVacio(AST):
    def __init__(self, linea):
        self.tipo = "VACIO"
        self.linea = linea

    def arbol(self):
        return '( "Vacio" )'

class NodoAsignacion(AST):
    def __init__(self, id_nombre, exp, linea):
        self.id = id_nombre
        self.exp = exp
        self.linea = linea
        self.compsem()

    def compsem(self):
        # 1. Comprobar si la variable existe
        if not tablasimbolos.Existe(self.id):
            print(f"ERROR Semántico línea {self.linea}: Variable '{self.id}' no definida.")
            return

        # 2. Obtener tipo de la variable
        atributos = tablasimbolos.Valor(self.id) # (tipo, naturaleza, valor)
        tipo_var = atributos[0]
        
        # 3. Comprobar compatibilidad de tipos
        # Conversión implícita: Si variable es REAL y exp es ENTERO -> OK
        if tipo_var == 'REAL' and self.exp.tipo == 'ENTERO':
            # Se permite (conversión implícita)
            pass
        elif tipo_var != self.exp.tipo:
            print(f"ERROR Semántico línea {self.linea}: Asignación incompatible. Variable '{self.id}' es {tipo_var} y expresión es {self.exp.tipo}.")

    def arbol(self):
        return '( "Asignacion"\n  "id: %s" \n%s\n)' % (self.id, self.exp)

class NodoSi(AST):
    def __init__(self, exp, si, sino, linea):
        self.exp = exp
        self.si = si
        self.sino = sino
        self.linea = linea
        self.compsem()

    def compsem(self):
        if self.exp.tipo != 'BOOLEANO':
            print(f"ERROR Semántico línea {self.linea}: La condición del SI debe ser BOOLEANO, se encontró {self.exp.tipo}.")

    def arbol(self):
        sino_str = self.sino if self.sino else "()"
        return '( "Si" "linea: %s" %s\n %s\n %s\n )' % (self.linea, self.exp, self.si, sino_str)

class NodoMientras(AST):
    def __init__(self, exp, inst, linea):
        self.exp = exp
        self.inst = inst
        self.linea = linea
        self.compsem()

    def compsem(self):
        if self.exp.tipo != 'BOOLEANO':
            print(f"ERROR Semántico línea {self.linea}: La condición del MIENTRAS debe ser BOOLEANO, se encontró {self.exp.tipo}.")

    def arbol(self):
        return '( "Mientras" "linea: %s" %s\n %s\n )' % (self.linea, self.exp, self.inst)

class NodoLee(AST):
    def __init__(self, var, linea):
        self.var = var
        self.linea = linea
        self.compsem()
    
    def compsem(self):
        # La instrucción LEE implica variable simple (ENTERO o REAL) 
        if not tablasimbolos.Existe(self.var):
            print(f"ERROR Semántico línea {self.linea}: Variable '{self.var}' no definida en LEE.")
            return
        
        # Opcional: Validar que sea tipo simple si el enunciado lo exige estrictamente

    def arbol(self):
        return '( "Lee" "linea: %s" "Var: %s" )' % (self.linea, self.var)

class NodoEscribe(AST):
    def __init__(self, exp, linea):
        self.exp = exp
        self.linea = linea
        # ESCRIBE permite expresiones 

    def arbol(self):
        return '( "Escribe" "linea: %s" %s )' % (self.linea, self.exp)

class NodoCompuesta(AST):
    def __init__(self, lsen, linea):
        self.lsen = lsen
        self.linea = linea

    def arbol(self):
        r = ""
        if self.lsen:
            for sent in self.lsen:
                if sent: r += str(sent) + "\n"
        return '( "Compuesta"\n %s)' % r

class NodoComparacion(AST):
    def __init__(self, izq, dcha, linea, op):
        self.izq = izq
        self.dcha = dcha
        self.linea = linea
        self.op = op
        self.tipo = 'BOOLEANO' # Resultado de comparación siempre es bool
        self.compsem()

    def compsem(self):
        # Comprobar que los operandos sean comparables (numeros)
        tipos_validos = ['ENTERO', 'REAL']
        if self.izq.tipo not in tipos_validos or self.dcha.tipo not in tipos_validos:
             print(f"ERROR Semántico línea {self.linea}: Comparación invalida entre {self.izq.tipo} y {self.dcha.tipo}.")

    def arbol(self):
        return '( "Comparacion" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)

class NodoAritmetico(AST):
    def __init__(self, izq, dcha, linea, op):
        self.izq = izq
        self.dcha = dcha
        self.linea = linea
        self.op = op
        self.tipo = None
        self.compsem()

    def compsem(self):
        # Inferencia de tipos y validación
        # Si alguno es REAL, el resultado es REAL 
        if self.izq.tipo == 'REAL' or self.dcha.tipo == 'REAL':
            self.tipo = 'REAL'
        elif self.izq.tipo == 'ENTERO' and self.dcha.tipo == 'ENTERO':
            self.tipo = 'ENTERO'
        else:
            self.tipo = 'ERROR'
            print(f"ERROR Semántico línea {self.linea}: Operación aritmética inválida entre {self.izq.tipo} y {self.dcha.tipo}.")

    def arbol(self):
        return '( "Aritmetica" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)
        
class NodoLogico(AST):
    def __init__(self, izq, dcha, linea, op):
        self.izq = izq
        self.dcha = dcha
        self.linea = linea
        self.op = op
        self.tipo = 'BOOLEANO'
        self.compsem()

    def compsem(self):
        if self.izq.tipo != 'BOOLEANO' or self.dcha.tipo != 'BOOLEANO':
             print(f"ERROR Semántico línea {self.linea}: Operación lógica '{self.op}' requiere operandos booleanos.")

    def arbol(self):
        return '( "Logica" "op: %s" "tipo: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.izq, self.dcha)

class NodoEntero(AST):
    def __init__(self, valor, linea):
        self.valor = valor
        self.linea = linea
        self.tipo = 'ENTERO'
    
    def arbol(self):
        return '( "Entero" "valor: %s" "tipo: %s" )' % (self.valor, self.tipo)


class NodoReal(AST):
    def __init__(self, valor, linea):
        self.valor = valor
        self.linea = linea
        self.tipo = 'REAL'
    
    def arbol(self):
        return '( "Real" "valor: %s" "tipo: %s" )' % (self.valor, self.tipo)

class NodoBooleano(AST):
    def __init__(self, valor, linea):
        self.valor = valor
        self.linea = linea
        self.tipo = 'BOOLEANO'
    
    def arbol(self):
        return '( "Booleano" "valor: %s" "tipo: %s" )' % (self.valor, self.tipo)

class NodoAccesoVariable(AST):
    def __init__(self, var, linea):
        self.var = var
        self.linea = linea
        self.tipo = None
        self.compsem()

    def compsem(self):
        if not tablasimbolos.Existe(self.var):
            print(f"ERROR Semántico línea {self.linea}: Variable '{self.var}' no declarada.")
            self.tipo = 'ERROR'
        else:
            # Recuperamos el tipo de la tabla
            atributos = tablasimbolos.Valor(self.var)
            self.tipo = atributos[0]

    def arbol(self):
        return '( "AccesoVariable" "v: %s" "tipo: %s" )' % (self.var, self.tipo)