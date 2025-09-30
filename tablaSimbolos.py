# Esta es la clase que contine la logica de la tabla de simbolos

''' Para esto se tiene en cuenta que la información que se almacena para cada tipo de variable es (sujeto a cambios):

        Variables escalar: tipo (String), dirección (Int), tamaño (Int) y valor (Int/Double/String)
        variables vectoriales: tipo base (String), dirección inicial (Int), tamaño de las dimensiones (Int)
        funciones: número de argumentos (Int), tupla con los tipos de argumentos de entrada (tupla de Strings) y tupla con los tipos de argumentos devueltos (tupla de Strings)  
'''
noID=Exception("Id no encontrado en la tabla de simbolos")
class tablaSimbolos():
    def __init__(self):
        self.tabla = self.Crear()

    def Crear(self):
        return {}
    
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
    
    # Versiones genéricas

    def Insertar(self, id, valor):
        self.tabla[id] = valor

    def Modificar(self, id, valor):     
        if id not in self.tabla:
            raise noID
        self.tabla[id] = valor
    
    # Versiones específicas para escalares

    def InsertarEscalar(self, id, tipo, direccion, tamaño, valor):
        atributos=(tipo,direccion,tamaño,valor)
        self.tabla[id]= atributos

    def ModificarEscalar(self,id,tipo=0,direccion=0,tamaño=0,valor=0):
        if id not in self.tabla:
            raise noID
        
        if tipo ==0:
            tipo= self.tabla[id][0]

        if direccion==0:
            direccion=self.tabla[id][1]
        
        if tamaño ==0:
            tamaño=self.tabla[id][2]

        if valor ==0:
            valor=self.tabla[id][3]

        self.tabla[id]=(tipo,direccion,tamaño,valor)

    # Versiones específicas para vectoriales

    def InsertarVectorial(self,id,tipoBase,dirInicial,tamDimen):
        atributos=(tipoBase,dirInicial,tamDimen)
        self.tabla[id]=atributos

    def ModificarVectorial(self,id,tipoBase=0, dirInicial=0,tamDimen=0):
        if id not in self.tabla:
            raise noID
        
        if tipoBase ==0:
            tipoBase= self.tabla[id][0]

        if dirInicial==0:
            dirInicial=self.tabla[id][1]
        
        if tamDimen ==0:
            tamDimen=self.tabla[id][2]

        self.tabla[id]=(tipoBase,dirInicial,tamDimen)

    # Versiones específicas para funciones

    def InsertarFuncion(self,id,numArg,argEntrada,argSalida):
        atributos=(numArg,argEntrada,argSalida)
        self.tabla[id]=atributos    

    def ModificarFuncion(self,id,numArg=0,argEntrada=0,argSalida=0):
        if id not in self.tabla:
            raise noID
        
        if numArg ==0:
            numArg= self.tabla[id][0]

        if argEntrada==0:
            argEntrada=self.tabla[id][1]
        
        if argSalida ==0:
            argSalida=self.tabla[id][2]

        self.tabla[id]=(numArg,argEntrada,argSalida)

    
# Ejercicio 2 de Practica 1


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
    
    
tabla.InsertarEscalar("entero_1","Entero", 10300,64,10)
tabla.InsertarVectorial("vector_2","Double",10400,64)
tabla.InsertarFuncion("funcion_3",3,("Entero,String,Double"),"Entero")
print(tabla)

tabla.ModificarEscalar("entero_1","Double",2,3,4)
tabla.ModificarVectorial("vector_2","String",333,1)
tabla.ModificarFuncion("funcion_3",4,("Entero", "String","Boolean","Double"),("String","Boolean"))
print(tabla)
