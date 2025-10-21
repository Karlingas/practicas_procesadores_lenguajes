# Esta es la clase que contiene la lógica de la tabla de símbolos

''' Para esto se tiene en cuenta que la información que se almacena para cada tipo de variable es (sujeto a cambios):

        Variables escalar: tipo (String), dirección (Int), tamaño (Int) y valor (Int/Double/String)
        variables vectoriales: tipo base (String), dirección inicial (Int), tamaño de las dimensiones (Int)
        funciones: número de argumentos (Int), tupla con los tipos de argumentos de entrada (tupla de Strings) y tupla con los tipos de argumentos devueltos (tupla de Strings)  
'''

noID = Exception("Id no encontrado en la tabla de simbolos")

class tablaSimbolos():
    """
    Clase que implementa una tabla de símbolos para almacenar información
    sobre variables escalares, vectoriales y funciones en un entorno de ejecución o compilación.
    """

    def __init__(self):
        """
        Inicializa una nueva tabla de símbolos vacía.
        """
        self.tabla = self.Crear()

    def Crear(self):
        """
        Crea y retorna una nueva tabla de símbolos vacía.

        Returns:
            dict: Diccionario vacío para almacenar identificadores.
        """
        return {}

    def Existe(self, id):
        """
        Verifica si un identificador existe en la tabla.

        Args:
            id (str): Identificador a buscar.

        Returns:
            bool: True si el identificador está en la tabla, False en caso contrario.
        """
        if id in self.tabla:
            return True
        return False

    def Valor(self, id):
        """
        Obtiene los atributos asociados a un identificador.

        Args:
            id (str): Identificador a consultar.

        Returns:
            tuple: Atributos del identificador.

        Raises:
            Exception: Si el identificador no existe en la tabla.
        """
        if id not in self.tabla:
            raise noID
        return self.tabla[id]

    def __str__(self):
        """
        Devuelve una representación en cadena de la tabla de símbolos.

        Returns:
            str: Contenido actual de la tabla como string.
        """
        return str(self.tabla)

    # Versiones genéricas

    def Insertar(self, id, valor):
        """
        Inserta un identificador con sus atributos genéricos.

        Args:
            id (str): Identificador.
            valor (tuple): Atributos asociados.
        """
        self.tabla[id] = valor

    def Modificar(self, id, valor):     
        """
        Modifica los atributos de un identificador existente.

        Args:
            id (str): Identificador.
            valor (tuple): Nuevos atributos.

        Raises:
            Exception: Si el identificador no existe.
        """
        if id not in self.tabla:
            raise noID
        self.tabla[id] = valor

    # Versiones específicas para escalares

    def InsertarEscalar(self, id, tipo, direccion, tamaño, valor):
        """
        Inserta una variable escalar con sus atributos.

        Args:
            id (str): Nombre del identificador.
            tipo (str): Tipo de dato.
            direccion (int): Dirección de memoria.
            tamaño (int): Tamaño del dato.
            valor (int | float | str): Valor de la variable.
        """
        atributos = (tipo, direccion, tamaño, valor)
        self.tabla[id] = atributos

    def ModificarEscalar(self, id, tipo=0, direccion=0, tamaño=0, valor=0):
        """
        Modifica una variable escalar manteniendo los valores anteriores si no se proporcionan nuevos.

        Args:
            id (str): Identificador.
            tipo (str, optional): Nuevo tipo de dato.
            direccion (int, optional): Nueva dirección de memoria.
            tamaño (int, optional): Nuevo tamaño.
            valor (int | float | str, optional): Nuevo valor.

        Raises:
            Exception: Si el identificador no existe.
        """
        if id not in self.tabla:
            raise noID

        if tipo == 0:
            tipo = self.tabla[id][0]
        if direccion == 0:
            direccion = self.tabla[id][1]
        if tamaño == 0:
            tamaño = self.tabla[id][2]
        if valor == 0:
            valor = self.tabla[id][3]

        self.tabla[id] = (tipo, direccion, tamaño, valor)

    # Versiones específicas para vectoriales

    def InsertarVectorial(self, id, tipoBase, dirInicial, tamDimen):
        """
        Inserta una variable vectorial con sus atributos.

        Args:
            id (str): Identificador.
            tipoBase (str): Tipo base del vector.
            dirInicial (int): Dirección inicial en memoria.
            tamDimen (int): Tamaño de las dimensiones.
        """
        atributos = (tipoBase, dirInicial, tamDimen)
        self.tabla[id] = atributos

    def ModificarVectorial(self, id, tipoBase=0, dirInicial=0, tamDimen=0):
        """
        Modifica una variable vectorial manteniendo los valores anteriores si no se proporcionan nuevos.

        Args:
            id (str): Identificador.
            tipoBase (str, optional): Nuevo tipo base.
            dirInicial (int, optional): Nueva dirección inicial.
            tamDimen (int, optional): Nuevo tamaño de dimensiones.

        Raises:
            Exception: Si el identificador no existe.
        """
        if id not in self.tabla:
            raise noID

        if tipoBase == 0:
            tipoBase = self.tabla[id][0]
        if dirInicial == 0:
            dirInicial = self.tabla[id][1]
        if tamDimen == 0:
            tamDimen = self.tabla[id][2]

        self.tabla[id] = (tipoBase, dirInicial, tamDimen)

    # Versiones específicas para funciones

    def InsertarFuncion(self, id, numArg, argEntrada, argSalida):
        """
        Inserta una función con su información de firma.

        Args:
            id (str): Identificador de la función.
            numArg (int): Número de argumentos.
            argEntrada (tuple): Tipos de argumentos de entrada.
            argSalida (tuple): Tipos de argumentos de salida.
        """
        atributos = (numArg, argEntrada, argSalida)
        self.tabla[id] = atributos    

    def ModificarFuncion(self, id, numArg=0, argEntrada=0, argSalida=0):
        """
        Modifica los atributos de una función, manteniendo los valores anteriores si no se proporcionan nuevos.

        Args:
            id (str): Identificador de la función.
            numArg (int, optional): Nuevo número de argumentos.
            argEntrada (tuple, optional): Nuevos tipos de entrada.
            argSalida (tuple, optional): Nuevos tipos de salida.

        Raises:
            Exception: Si el identificador no existe.
        """
        if id not in self.tabla:
            raise noID

        if numArg == 0:
            numArg = self.tabla[id][0]
        if argEntrada == 0:
            argEntrada = self.tabla[id][1]
        if argSalida == 0:
            argSalida = self.tabla[id][2]

        self.tabla[id] = (numArg, argEntrada, argSalida)


    
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
