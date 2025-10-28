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

 def createNumList(self,first_ch):
   """Consume dígitos consecutivos del flujo, empezando por `first_ch`.

   Args:
      first_ch (str): El primer dígito ya consumido.

   Returns:
      tuple[list[str], str]: (lista_de_dígitos, primer_caracter_no_dígito)
   """
   digit_list = []
   digit_list.append(first_ch)
   next_ch = self.flujo.NewCar()

   while (next_ch.isdigit()):
      digit_list.append(next_ch)
      next_ch = self.flujo.NewCar()
   
   return (digit_list,next_ch)

 ############################################################################
 #
 #  Funcion: TrataNum
 #  Tarea:  Lee un numero del flujo
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #              ch: primera caractera tratar
 #  Devuelve: El valor numerico de la cadena leida
 #
 ############################################################################
 def TrataNum(self, ch):
   (number_int_list,next_ch) = self.createNumList(ch)

   if (next_ch == "."):
      next_ch = self.flujo.NewCar()
      (number_float_list,_) = self.createNumList(next_ch) # TODO: Si después del . no viene un número, ERROR. Tiene que ser un numero SI o SI

      int_str = "".join(number_int_list)
      float_str = "".join(number_float_list)

      ret = componentes.Real(self.flujo.NumLinea(),float(f"{int_str}.{float_str}"))
   else:
      ret = componentes.Entero(self.flujo.NumLinea(),int("".join(number_int_list)))

   self.flujo.Devolver()

   return ret

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
   ch = self.flujo.NewCar()
   if ch:
      if ch == "EOF": # EOF
         return False
      elif ch == " ":
         #TODO:acciones si hemos encontrado un blanco
         pass

      elif ch == "\r":
         #TODO: acciones si hemos encontrado un salto de linea (\r es regresión de carro)
         pass

      elif ch.isdigit(): # Número cualquiera
         return self.TrataNum(ch)
            
      elif ch == "\n":
         ## TODO: acciones al encontrar un salto de linea
         self.nlinea = self.nlinea + 1
         return self.Analiza()
      
      else:
         # TODO: se ha encontrado un caracter no permitido
         print ("ERROR LEXICO  Linea " + str(self.nlinea) + " ::  Caracter " + ch + " invalido ")
         return self.Analiza()    
      
   else:
      raise Exception("Se leyó más allá del fin de fichero")

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Prametros:  --
#  Devuelve: --
#
############################################################################

if __name__=="__main__":
   script =argv
   filename = "/home/calberto/Documents/Uni/7moCuatri/ProcesadoresLenguajes/Practicas/practicas_procesadores_lenguajes/Tests/1"
   txt=open(filename)
   print ("PROGRAMA FUENTE %r \n\n"  % filename)
   i=0
   fl = flujo.Flujo(filename)
   analex=Analex(fl)
   c = analex.Analiza()
   while c:
      print (c)
      c = analex.Analiza()
      print("\n")
   i = i + 1
   print("\n")

