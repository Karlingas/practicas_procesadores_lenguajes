class Arbol:
    def __init__(self, elto):
        """
        Inicializa un nuevo nodo del árbol binario de búsqueda.

        Args:
            elto: Valor del nodo.
        """
        self.elto = elto
        self.izdo = None  # Subárbol izquierdo
        self.dcho = None  # Subárbol derecho

    def Inserta(self, value):
        """
        Inserta un nuevo valor en el árbol manteniendo el orden del árbol binario de búsqueda.

        Args:
            value: Valor a insertar en el árbol.

        Notas:
            - Si el valor ya existe, no se inserta y se imprime un mensaje.
        """
        if value < self.elto:
            if self.izdo is None:
                self.izdo = Arbol(value)
            else:
                self.izdo.Inserta(value)
        elif value > self.elto:
            if self.dcho is None:
                self.dcho = Arbol(value)
            else:
                self.dcho.Inserta(value)
        else:
            print("El elemento ya está en el árbol, no se permiten duplicados.")
            return

    def Esta(self, value):
        """
        Verifica si un valor está presente en el árbol.

        Args:
            value: Valor a buscar.

        Returns:
            bool: True si el valor está en el árbol, False en caso contrario.
        """
        if value == self.elto:
            return True
        elif value < self.elto:
            if self.izdo is None:
                return False
            else:
                return self.izdo.Esta(value)
        else:
            if self.dcho is None:
                return False
            else:
                return self.dcho.Esta(value)

    def __str__(self):
        """
        Devuelve una representación en cadena del árbol en recorrido inorden.

        Returns:
            str: Cadena con los elementos del árbol ordenados de menor a mayor.
        """
        resultado = ""
        if self.izdo is not None:
            resultado += str(self.izdo) + ", "
        resultado += str(self.elto)
        if self.dcho is not None:
            resultado += ", " + str(self.dcho)
        return resultado

    def Modificar(self, viejo, nuevo):
        """
        Modifica un valor existente en el árbol, reemplazándolo por uno nuevo.

        Args:
            viejo: Valor a buscar y reemplazar.
            nuevo: Nuevo valor que sustituirá al antiguo.

        Notas:
            - No cambia la estructura del árbol (puede romper el orden si el nuevo valor no respeta el orden binario).
            - Solo reemplaza el primer nodo encontrado con el valor antiguo.
        """
        if viejo == self.elto:
            self.elto = nuevo
        elif viejo < self.elto:
            if self.izdo is not None:
                self.izdo.Modificar(viejo, nuevo)
        else:
            if self.dcho is not None:
                self.dcho.Modificar(viejo, nuevo)

    def Valor(self):
        """
        Devuelve el valor almacenado en el nodo actual.

        Returns:
            Cualquier tipo: Valor del nodo.
        """
        return self.elto
