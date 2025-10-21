#!/usr/bin/env python

import componentes
#import errores k e esto
import flujo
import string
import sys
import os
from sys import argv

class Analex:
#############################################################################
##  Conjunto de palabras reservadas para comprobar si un identificador es PR
#############################################################################
 PR = frozenset(["PROGRAMA", "VAR", "ENTERO", "REAL", "BOOLEANO", "INICIO", "FIN", "SI", "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "Y", "O", "NO", "CIERTO","FALSO"])

 ############################################################################
 #
 #  Funcion: __init__
 #  Tarea:  Constructor de la clase
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #  Devuelve: --
 #
 ############################################################################
 def __init__(self, flujo):
    self.flujo= flujo
    self.poserror= 0
    self.nlinea=1


 ############################################################################
 #
 #  Funcion: TrataNum
 #  Tarea:  Lee un numero del flujo
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #              ch: primera caractera tratar
 #  Devuelve: El valor numerico de la cadena leida
 #
 ############################################################################
 def TrataNum(self,flujo, ch):
 
  #TODO:Completar
  pass

 ############################################################################
 #
 #  Funcion: TrataIdent
 #  Tarea:  Lee identificadores
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #              ch: Primer caracter a tratar
 #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
 #
 ############################################################################
 def TrataIdent(self,flujo, ch):
    #TODO:Completar
    pass
 
  ############################################################################
  #
  #  Funcion: TrataIdent
  #  Tarea:  Lee identificadores
  #  Prametros:  flujo:  flujo de caracteres de entrada
  #              ch: Primer caracter a tratar
  #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
  #
  ############################################################################
 def TrataComent(self, flujo):
    #TODO: Completar
    pass

 ############################################################################
 #
 #  Funcion: EliminaBlancos
 #  Tarea:  Descarta todos los caracteres blancos que hay en el flujo de entrada
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #  Devuelve: --
 #
 ############################################################################
 def EliminaBlancos(self,flujo):
    #TODO: Completar
    pass

 ############################################################################
 #
 #  Funcion: Analiza
 #  Tarea:  Identifica los diferentes componentes lexicos
 #  Prametros:  --
 #  Devuelve: Devuelve un componente lexico
 #
 ############################################################################
 def Analiza(self):
    l = ""
    ch = self.flujo.siguiente()
    if ch == " ":
       #TODO:acciones si hemos encontrado un blanco
       pass
    elif ch == "\r":
       #TODO: acciones si hemos encontrado un salto de linea
       pass
    elif ch.isinstance(int): # Número cualquiera
        ch_next = self.flujo.siguiente()
        if (ch_next == " "):
            return self.Analiza()
        elif (ch_next == "."):
           ch_next_next = self.flujo.siguiente()
           if (ch_next_next.isinstance(int)):
                while(siguiente siga siendo numero):
                   aceptar
                   if (espacio):
                      return self.Analiza()
        while(siguiente siga siendo numero):
            aceptar
            siguiente char
            if (espacio):
                return self.Analiza()
            
    elif ch == "\n":
        ## TODO: acciones al encontrar un salto de linea
        self.nlinea = self.nlinea + 1
        return self.Analiza()
    elif ch:
        # TODO: se ha encontrado un caracter no permitido
        print ("ERROR LEXICO  Linea " + str(self.nlinea) + " ::  Caracter " + ch + " invalido ")
        return self.Analiza()
    else:
        # TODO: el final de fichero
        return componentes.EOF()

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Prametros:  --
#  Devuelve: --
#
############################################################################

if __name__=="__main__":
    script, filename=argv
    txt=open(filename)
    print ("PROGRAMA FUENTE %r"  % filename)
    i=0
    fl = flujo.Flujo(txt)
    analex=Analex(fl)
    c = analex.Analiza()
    while c.cat != "EOF":
        print (c)
        c = analex.Analiza()
    i = i + 1

