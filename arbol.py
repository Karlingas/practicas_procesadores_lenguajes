class arbol:
    def __init__(self, elto):
        self.elto = elto
        self.izdo = None
        self.dcho = None
    
    def Inserta(self, value):
        if value < self.elto:
            if self.izdo is None:
                self.izdo = arbol(value)
            else:
                self.izdo.Inserta(value)
        elif value > self.elto:
            if self.dcho is None:
                self.dcho = arbol(value)
            else:
                self.dcho.Inserta(value)
        else:
            print("El elemento ya está en el árbol, no se permiten duplicados.")
            return
    
    def Esta(self, value):
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
        # Imprime en inorden
        resultado = ""
        if self.izdo is not None:
            resultado += str(self.izdo) + ", "
        resultado += str(self.elto)
        if self.dcho is not None:
            resultado += ", " + str(self.dcho)
        return resultado
    
    def Modificar(self, viejo, nuevo):
        if viejo == self.elto:
            self.elto = nuevo
        elif viejo < self.elto:
            if self.izdo is not None:
                self.izdo.Modificar(viejo, nuevo)
        else:
            if self.dcho is not None:
                self.dcho.Modificar(viejo, nuevo)
    
    def Valor(self):
        return self.elto