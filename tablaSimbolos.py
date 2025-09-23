# Esta es la clase que contine la logica de la tabla de simbolos

noID=Exception("Id no encontrado en la tabla de simbolos")
class tablaSimbolos():
    def __init__(self):
        self.tabla = self.Crear()

    def Crear(self):
        return {}
    
    def Insertar(self, id, valor):
        self.tabla[id] = valor

    def Modificar(self, id, valor):     # Especificar más para cada atributo en el futuro
        if id not in self.tabla:
            raise noID
        self.tabla[id] = valor
    
    def Existe(self, id):
        if id in self.tabla:
            return True
        return False
    
    def Valor(self, id):
        if id not in self.tabla:
            raise noID
        return self.tabla[id]
    
    def __str__(self):
        return str(self.tabla)

# Ejercicio 2 de Practica 1

def main():
    tabla = tablaSimbolos()
    tabla.Insertar("x", ("Entero", 10,10000))
    tabla.Insertar("y", ("Cadena", "Hola Mundo",10100))
    print(tabla)

    tabla.Insertar("z", ("Booleano", True,10200))
    tabla.Modificar("x", ("Real", 3.14,10000))
    print(tabla)

    print(tabla.Existe("x"))
    print(tabla.Existe("a"))
    print(tabla.Valor("y"))

main()