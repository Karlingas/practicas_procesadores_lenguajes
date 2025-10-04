# TODO: Documentar con comentarios docstring

class AST:
    def __init__(self): pass
    def mostrar(self): pass             # muestra la expresion utilizando parentesis
    def numero_operaciones(self): pass  # muestra el numero de operaciones en la expresion
    def interpreta(self): pass          # evalua la expresion

class Numero(AST):
    def __init__(self, value):
        self.value = value
    
    def mostrar(self):
        return str(self.value)
    
    def numero_operaciones(self):
        return 0
    
    def interpreta(self):
        return self.value
    
class Operacion(AST):
    def __init__(self, op, izda, dcha):
        self.SOPORTED_OPERATORS = {'+', '-', '*', '/'}
        self.op= op
        self.izda= izda
        self.dcha= dcha
    
    def mostrar(self):
        return '(' + self.izda.mostrar() + self.op + self.dcha.mostrar() + ')'
    
    def numero_operaciones(self):
        return 1 + self.izda.numero_operaciones() + self.dcha.numero_operaciones()
    
    def interpreta(self):
        if self.SOPORTED_OPERATORS.__contains__(self.op):
            if self.op == '+':
                return self.izda.interpreta() + self.dcha.interpreta()
            elif self.op == '-':
                return self.izda.interpreta() - self.dcha.interpreta()
            elif self.op == '*':
                return self.izda.interpreta() * self.dcha.interpreta()
            elif self.op == '/':
                return self.izda.interpreta() / self.dcha.interpreta()
        else:
            raise Exception("Operador no soportado: " + self.op + " actualmente solo se soportan " + str(self.SOPORTED_OPERATORS))

'''
PRUEBA DEL CODIGO
'''
# Introducimos el ´arbol de la expresi´on 4*5+3*2
num1=Numero(4)
num2=Numero(5)
num3=Numero(3)
num4=Numero(2)
arbol1=Operacion('*',num1,num2) # 4*5
arbol2=Operacion('*',num3,num4) # 3*2
arbol_final=Operacion('+',arbol1,arbol2) # arbol1+arbol2
# Accedemos al ´arbol de tres formas diferentes mediante funciones miembro
print('El arbol contiene la expresion:', arbol_final.mostrar())
print('El arbol contiene en total %d operaciones' % arbol_final.numero_operaciones())
print('La expresion se evalua como:', arbol_final.interpreta())