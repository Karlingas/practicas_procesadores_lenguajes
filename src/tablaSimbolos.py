# Esta es la clase que contiene la lógica de la tabla de símbolos

''' Para esto se tiene en cuenta que la información que se almacena para cada tipo de variable es (sujeto a cambios):

        Variables escalar: Identificador (String), Tipo (String), Naturaleza (String), valor (Int/Double/String)

        No harian falta otros tipos, ya que en nuestro lenguaje no va ni a haber vectores ni llamadas a funciones.
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

    def Existe(self, identificador):
        """
        Verifica si un identificador existe en la tabla.

        Args:
            identificador (str): Identificador a buscar.

        Returns:
            bool: 'True' si el identificador está en la tabla, 'False' en caso contrario.
        """
        if identificador in self.tabla:
            return True
        return False

    def Valor(self, identificador):
        """
        Obtiene los atributos asociados a un identificador.

        Args:
            identificador (str): .

        Returns:
            tupla: Valor asociado al identificador.

        Raises:
            Exception: Si el identificador no existe en la tabla.
        """
        if identificador not in self.tabla:
            raise noID
        return self.tabla[identificador]

    def __str__(self):
        """
        Devuelve una representación en cadena de la tabla de símbolos.

        Returns:
            str: Contenido actual de la tabla como string.
        """
        return str(self.tabla)

    # Versiones específicas para escalares

    def Insertar(self, identificador, tipo, naturaleza, valor):
        """
        Inserta una variable escalar con sus atributos.

        Args:
            identificador (str): Nombre del identificador.
            tipo (str): Tipo de dato.
            direccion (int): Dirección de memoria.
            tamaño (int): Tamaño del dato.
            valor (int | float | str): Valor de la variable.
        """
        atributos = (tipo, naturaleza, valor)
        self.tabla[identificador] = atributos

    def ModificarTipo(self, identificador, tipoNuevo):
        '''
        Modifica el tipo de la variable asociada al identificador.

        Args:
            identificador (str): id de la variable cuyo tipo se quiere cambiar
            tipoNuevo (str): Tipo nuevo que tendrá la variable

        Raises:
            Exception: Si el identificador no existe.        
        '''

        if identificador not in self.tabla:
            raise noID
        
        self.tabla[identificador][0]=tipoNuevo


    def ModificarNaturaleza(self, identificador, naturalezaNueva):
        '''
        Modifica la naturaleza de la variable asociada al identificador.

        Args:
            identificador (str): id de la variable cuyo tipo se quiere cambiar
            naturalezaNueva (str): Naturaleza    nueva que tendrá la variable

        Raises:
            Exception: Si el identificador no existe.        
        '''

        if identificador not in self.tabla:
            raise noID
        
        self.tabla[identificador][1]=naturalezaNueva


    def ModificarValor(self, identificador, valorNuevo):
        '''
        Modifica el valor de la variable asociada al identificador.

        Args:
            identificador (str): id de la variable cuyo tipo se quiere cambiar
            valorNuevo (str): Valor nuevo que tendrá la variable

        Raises:
            Exception: Si el identificador no existe.        
        '''

        if identificador not in self.tabla:
            raise noID
        
        self.tabla[identificador][0]=valorNuevo

    # Modifica todo de una
    def ModificarGeneral(self, identificador, tipoNuevo, naturalezaNueva, valorNuevo):
        '''
        Modifica todos los datos de la variable asociada al identificador.

        Args:
            identificador (str): id de la variable cuyo tipo se quiere cambiar
            tipoNuevo (str): Tipo nuevo que tendrá la variable
            naturalezaNueva (str): Naturaleza    nueva que tendrá la variable
            valorNuevo (str): Valor nuevo que tendrá la variable

        Raises:
            Exception: Si el identificador no existe.        
        '''

        if identificador not in self.tabla:
            raise noID
        
        entrada=[tipoNuevo, naturalezaNueva, valorNuevo]

        self.tabla[identificador]=entrada

