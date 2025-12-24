#!/usr/bin/env python
from tablaSimbolos import tablaSimbolos

# Instancia global de la tabla de símbolos para uso en los nodos
tablasimbolos = tablaSimbolos()

class AST:
    # Para los errores del semántico
    error_semantico = False

    def __str__(self):
        # Llama a arbol con indentación 0 por defecto
        return self.arbol(0)
    
    def __repr__(self):
        return self.__str__()
    
    def compsem(self):
        pass

# Nodo para errores o producciones vacías
class NodoVacio(AST):
    def __init__(self, linea):
        self.tipo = "VACIO"
        self.linea = linea

    def arbol(self, indent=0):
        tab = "    " * indent
        return f"{tab}( \"Vacio\" )"

class NodoAsignacion(AST):
    def __init__(self, id_nombre, exp, linea):
        self.id = id_nombre
        self.exp = exp
        self.linea = linea
        self.compsem()

    def compsem(self):
        if not tablasimbolos.Existe(self.id):
            print(f"ERROR Semántico línea {self.linea}: Variable '{self.id}' no definida.")
            return

        atributos = tablasimbolos.Valor(self.id)
        tipo_var = atributos[0]
        
        if tipo_var == 'REAL' and self.exp.tipo == 'ENTERO':
            pass
        elif tipo_var != self.exp.tipo:
            AST.error_semantico = True
            print(f"ERROR Semántico línea {self.linea}: Asignación incompatible. Variable '{self.id}' es {tipo_var} y expresión es {self.exp.tipo}.")

    def arbol(self, indent=0):
        tab = "    " * indent
        # Llamamos a arbol del hijo con indent + 1
        return f'{tab}( "Asignacion"\n{tab}    "id: {self.id}"\n{self.exp.arbol(indent+1)}\n{tab})'

class NodoSi(AST):
    def __init__(self, exp, si, sino, linea):
        self.exp = exp
        self.si = si
        self.sino = sino
        self.linea = linea
        self.compsem()

    def compsem(self):
        if self.exp.tipo != 'BOOLEANO':
            AST.error_semantico = True
            print(f"ERROR Semántico línea {self.linea}: La condición del SI debe ser BOOLEANO, se encontró {self.exp.tipo}.")

    def arbol(self, indent=0):
        tab = "    " * indent
        # Manejo especial para sino (si es None o es nodo)
        sino_str = self.sino.arbol(indent+1) if self.sino else f"{tab}    ()"
        
        return f'{tab}( "Si" "linea: {self.linea}"\n{self.exp.arbol(indent+1)}\n{self.si.arbol(indent+1)}\n{sino_str}\n{tab})'

class NodoMientras(AST):
    def __init__(self, exp, inst, linea):
        self.exp = exp
        self.inst = inst
        self.linea = linea
        self.compsem()

    def compsem(self):
        if self.exp.tipo != 'BOOLEANO':
            print(f"ERROR Semántico línea {self.linea}: La condición del MIENTRAS debe ser BOOLEANO, se encontró {self.exp.tipo}.")

    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Mientras" "linea: {self.linea}"\n{self.exp.arbol(indent+1)}\n{self.inst.arbol(indent+1)}\n{tab})'

class NodoLee(AST):
    def __init__(self, var, linea):
        self.var = var
        self.linea = linea
        self.compsem()
    
    def compsem(self):
        if not tablasimbolos.Existe(self.var):
            AST.error_semantico = True
            print(f"ERROR Semántico línea {self.linea}: Variable '{self.var}' no definida en LEE.")
            return

    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Lee" "linea: {self.linea}" "Var: {self.var}" )'

class NodoEscribe(AST):
    def __init__(self, exp, linea):
        self.exp = exp
        self.linea = linea

    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Escribe" "linea: {self.linea}"\n{self.exp.arbol(indent+1)}\n{tab})'

class NodoCompuesta(AST):
    def __init__(self, lsen, linea):
        self.lsen = lsen
        self.linea = linea

    def arbol(self, indent=0):
        tab = "    " * indent
        r = ""
        if self.lsen:
            for sent in self.lsen:
                if sent: 
                    # Importante: indentamos cada sentencia interna
                    r += sent.arbol(indent + 1) + "\n"
        return f'{tab}( "Compuesta"\n{r}{tab})'

class NodoComparacion(AST):
    def __init__(self, izq, dcha, linea, op):
        self.izq = izq
        self.dcha = dcha
        self.linea = linea
        self.op = op
        self.tipo = 'BOOLEANO'
        self.compsem()

    def compsem(self):
        tipos_validos = ['ENTERO', 'REAL']
        if self.izq.tipo not in tipos_validos or self.dcha.tipo not in tipos_validos:
             AST.error_semantico = True
             print(f"ERROR Semántico línea {self.linea}: Comparación invalida entre {self.izq.tipo} y {self.dcha.tipo}.")

    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Comparacion" "op: {self.op}" "tipo: {self.tipo}" "linea: {self.linea}"\n{self.izq.arbol(indent+1)}\n{self.dcha.arbol(indent+1)}\n{tab})'

class NodoAritmetico(AST):
    def __init__(self, izq, dcha, linea, op):
        self.izq = izq
        self.dcha = dcha
        self.linea = linea
        self.op = op
        self.tipo = None
        self.compsem()

    def compsem(self):
        if self.izq.tipo == 'REAL' or self.dcha.tipo == 'REAL':
            self.tipo = 'REAL'
        elif self.izq.tipo == 'ENTERO' and self.dcha.tipo == 'ENTERO':
            self.tipo = 'ENTERO'
        else:
            self.tipo = 'ERROR'
            AST.error_semantico = True
            print(f"ERROR Semántico línea {self.linea}: Operación aritmética inválida entre {self.izq.tipo} y {self.dcha.tipo}.")

    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Aritmetica" "op: {self.op}" "tipo: {self.tipo}" "linea: {self.linea}"\n{self.izq.arbol(indent+1)}\n{self.dcha.arbol(indent+1)}\n{tab})'
        
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
             AST.error_semantico = True
             print(f"ERROR Semántico línea {self.linea}: Operación lógica '{self.op}' requiere operandos booleanos.")

    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Logica" "op: {self.op}" "tipo: {self.tipo}"\n{self.izq.arbol(indent+1)}\n{self.dcha.arbol(indent+1)}\n{tab})'

class NodoEntero(AST):
    def __init__(self, valor, linea):
        self.valor = valor
        self.linea = linea
        self.tipo = 'ENTERO'
    
    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Entero" "valor: {self.valor}" "tipo: {self.tipo}" )'


class NodoReal(AST):
    def __init__(self, valor, linea):
        self.valor = valor
        self.linea = linea
        self.tipo = 'REAL'
    
    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Real" "valor: {self.valor}" "tipo: {self.tipo}" )'

class NodoBooleano(AST):
    def __init__(self, valor, linea):
        self.valor = valor
        self.linea = linea
        self.tipo = 'BOOLEANO'
    
    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "Booleano" "valor: {self.valor}" "tipo: {self.tipo}" )'

class NodoAccesoVariable(AST):
    def __init__(self, var, linea):
        self.var = var
        self.linea = linea
        self.tipo = None
        self.compsem()

    def compsem(self):
        if not tablasimbolos.Existe(self.var):
            AST.error_semantico = True
            print(f"ERROR Semántico línea {self.linea}: Variable '{self.var}' no declarada.")
            self.tipo = 'ERROR'
        else:
            atributos = tablasimbolos.Valor(self.var)
            self.tipo = atributos[0]

    def arbol(self, indent=0):
        tab = "    " * indent
        return f'{tab}( "AccesoVariable" "v: {self.var}" "tipo: {self.tipo}" )'