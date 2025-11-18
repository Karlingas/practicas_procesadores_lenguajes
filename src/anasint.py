#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv


class Sintactico:
#Constructor de la clase que implementa el Analizador Sintactico
#Solicita el primer componente lexico 
    def __init__(self, lexico):
        self.lexico= lexico
        self.token=self.lexico.Analiza()

    def Avanza(self):
        self.token = self.lexico.Analiza()

# Funcion que muestra los mensajes de error
    def Error(self, nerr):
        if nerr == 1:
            print ("Linea: " + str(self.token.linea) + "  ERROR Se espera PROGRAMA")
        elif nerr==2:
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera IDENTIFICADOR")


    def AnalizaPrograma(self):
        # Verificar inicio del programa
        if self.token.cat != "PR" or self.token.valor != "PROGRAMA":
            self.Error(1)
            return False
        self.Avanza()

        # Verificar identificador
        if self.token.cat != "Identif":
            self.Error(2)
            return False
        self.Avanza()

        # Verificar punto y coma
        if self.token.cat != "PtoComa":
            self.Error(3)
            return False
        self.Avanza()

        # Analizar cuerpo del programa
        self.AnalizaDeclVar()
        self.AnalizaInstrucciones()

        # Verificar punto final
        if self.token.cat != "Punto":
            self.Error(4)
            return False
        self.Avanza()

        return True
    
       

 
########################################################
##
## Programa principal que lanza el analizador sintactico
####################################################
if __name__=="__main__":
    script, filename=argv
    txt=open(filename)
    print ("Este es tu fichero %r" % filename)
    fl = flujo.Flujo(txt)
    anlex=analex.Analex(fl)
    S = Sintactico(anlex)
    if S.AnalizaPrograma():
        print ("Analisis sintactico SATISFACTORIO. Fichero :", filename, "CORRECTO")
    else:
        print ("Analisis sintactico CON ERRORES. Fichero :", filename, "ERRONEO")

'''
        if self.token.cat != "PR" or self.token.valor != "PROGRAMA":
            self.Error (1,self.token)  #raise errores.ErrorSintactico("Se espera la palabra reservada PROGRAMA")  #error 1
            return False
        else:
            self.token = self.lexico.Analiza()
            if self.token.cat != "Identif":
                self.Error(2,self.token)  # raise errores.ErrorSintactico("Se espera IDENTIFICADOR")  #error 2
                return False
        #TODO: metodo incompleto'''