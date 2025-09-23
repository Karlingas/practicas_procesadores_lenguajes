import os.path

class Flujo:
    ruta = ""
    flujo = ""
    indiceFlujo = 0
    contadorLinea = 0
    contadorCaracter = 0
    caracteresEnLinea = []

    def __init__(self, ruta):
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f'El archivo {ruta} no existe.')
        
        self.ruta = ruta
        archivo = open(ruta, 'r')
        self.flujo = archivo.read()
        archivo.close()

        self.indiceFlujo = 0
        self.contadorLinea = 0
        self.contadorCaracter = 0
        self.caracteresEnLinea = []

    ''' Devuelve el siguiente carácter del flujo
    '''
    def NewCar(self):
        if self.indiceFlujo >= len(self.flujo):
            return None
        caracter = self.flujo[self.indiceFlujo]
        
        self.indiceFlujo += 1
        if caracter == '\n':
            self.contadorLinea += 1
            self.caracteresEnLinea.append(self.contadorCaracter)
            self.contadorCaracter = 0
        else:
            self.contadorCaracter += 1

        return caracter

    ''' Devuelve el flujo una posición atrás
    '''
    def Devolver(self):
        self.indiceFlujo -= 1
        if self.contadorCaracter > 0:
            self.contadorCaracter -= 1
        else:
            self.contadorLinea -= 1
            self.contadorCaracter = self.caracteresEnLinea.pop()

    ''' Retorna el numero de linea que se está leyendo
    '''
    def NumLinea(self):
        if self.contadorCaracter == 0 and self.contadorLinea > 0: # Si estamos al inicio de una nueva línea, retornamos la línea anterior
            return self.contadorLinea - 1
        return self.contadorLinea

    ''' Retorna la posición que ocupa el último carácter leído en la línea actual
    '''
    def NumCaracter(self):
        if self.contadorCaracter == 0: # Si estamos al inicio de una nueva línea, retornamos la posición del último carácter de la línea anterior
            return self.caracteresEnLinea[-1]
        return self.contadorCaracter - 1


    # Funciones adicionales al ejercicio 

    ''' Devuelve el flujo n posiciones atrás
    '''
    def DevolverN(self, n):
        n = abs(n)
        if n >= self.indiceFlujo:
            n = self.indiceFlujo - 1

        for _ in range(n):
            self.Devolver()

    ''' Avanza el flujo n posiciones adelante
    '''
    def AvanzarN(self, n):
        n = abs(n)
        if n > len(self.flujo) - self.indiceFlujo:
            n = len(self.flujo) - self.indiceFlujo

        cadena = []
        for _ in range(n):
            cadena.append(self.NewCar())
        return ''.join(cadena)
    
    ''' Reasigna el flujo a otro archivo
    '''
    def Reasignar(self, ruta):
        self.__init__(ruta)

    def __str__(self):
        return f'Ruta={self.ruta}\nFlujo:\n{self.flujo}'
    

# Pruebas
def dondeEstoy(flujo):
    print("Nº Linea: ",flujo.NumLinea())
    print("Nº Caracter: ",flujo.NumCaracter())

flujo = Flujo('archivosFlujo/prueba.txt')
print(flujo)

print(flujo.AvanzarN(12))
dondeEstoy(flujo)

flujo.DevolverN(3)
print("(3 devolver)")
dondeEstoy(flujo)

print(flujo.NewCar())
dondeEstoy(flujo)