#!/usr/bin/env python

import componentes
#import errores k e esto
import flujo
import string
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
 #  Prametros: ch: primera caractera tratar
 #  Devuelve: El valor numerico de la cadena leida
 #
 ############################################################################
 def TrataNum(self, ch):
   (number_int_list,next_ch) = self.createNumList(ch) 

   if (next_ch == "."):
      next_ch = self.flujo.NewCar()
      (number_float_list,_) = self.createNumList(next_ch)

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
 #  Parametros: ch: Primer caracter a tratar
 #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
 #
 ############################################################################
 def TrataIdent(self, flujo, ch):
   ident_str = ch
   next_ch = flujo.NewCar()
    
   while (next_ch.isalnum()):
      ident_str += next_ch
      next_ch = flujo.NewCar()
   
   flujo.Devolver()

   if ident_str in Analex.PR:
      return componentes.PR(flujo.NumLinea(),ident_str)
   else:
      return componentes.Identif(flujo.NumLinea(), ident_str, None)
   

   
 
  ############################################################################
  #
  #  Funcion: TrataIdent
  #  Tarea:  Lee identificadores
  #  Prametros:  ch: Primer caracter a tratar
  #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
  #
  ############################################################################
 def TrataComent(self):
   comment = ""
   ch = self.flujo.NewCar()
   while ch != "\n" and ch != "EOF": # Mientras no sea fin de linea o fin de fichero
      comment += ch
      ch = self.flujo.NewCar()
   
   return componentes.Comment(self.flujo.NumLinea(), comment)

 ############################################################################
 #
 #  Funcion: EliminaBlancos
 #  Tarea:  Descarta todos los caracteres blancos que hay en el flujo de entrada
 #  Parametros: -
 #  Devuelve: --
 #
 ############################################################################
 def EliminaBlancos(self):
   # El blanco ya lo hemos consumido
   ch = self.flujo.NewCar()
   while ch == " " or ch == "\t" or ch == "\r":
       ch = self.flujo.NewCar()

   self.flujo.Devolver() # Devuelve el primer char no-blanco

 ############################################################################
 #
 #  Funcion: Analiza
 #  Tarea:  Identifica los diferentes componentes lexicos
 #  Parametros:  --
 #  Devuelve: Devuelve un componente lexico
 #
 ############################################################################
 def Analiza(self):
   l = ""

   ch = self.flujo.NewCar()
   if ch:
      # Para saber el final de fichero
      if ch == "EOF": # EOF
         return False
      
      # 1 Los comentarios
      elif ch == "%":
         next_ch = self.flujo.NewCar()

         if next_ch == "%":
            return self.TrataComent()
         else:
            self.flujo.Devolver()
            return componentes.Identif(self.flujo.NumLinea(), "%", None)
         
      # 2 Los espacios en blanco, tabulaciones y saltos de linea   
      elif ch == " " or ch == "\t" or ch == "\r":
         self.EliminaBlancos()
         return self.Analiza()

      elif ch == "\n":
         ## acciones al encontrar un salto de linea
         self.nlinea = self.nlinea + 1
         return self.Analiza()
      
      # 3 y 5 Identificadores que, ya que detecta lo que es texto, aprovechamos y detectamos palabras reservadas
      elif ch in string.ascii_letters: # Identificador o palabra reservada
         return self.TrataIdent(self.flujo, ch)
      
      # 4 Numeros enteros y reales
      elif ch.isdigit(): # Número cualquiera
         return self.TrataNum(ch)
      
      # 6 Operadores

      # Relacionales
      elif ch == "<":
         next_ch = self.flujo.NewCar()
         if next_ch == "=":
            return componentes.OpRel(self.flujo.NumLinea(), "<=")
         elif next_ch == ">":
            return componentes.OpRel(self.flujo.NumLinea(), "<>")
         else:
            self.flujo.Devolver()
            return componentes.OpRel(self.flujo.NumLinea(), "<")
      
      elif ch == ">":
         next_ch = self.flujo.NewCar()
         if next_ch == "=":
            return componentes.OpRel(self.flujo.NumLinea(), ">=")
         else:
            return componentes.OpRel(self.flujo.NumLinea(), ">")
      
      elif ch == "=":
         return componentes.OpRel(self.flujo.NumLinea(), "=")
      

      # Aritmeticos
      elif ch == "+":
         return componentes.OpAdd(self.flujo.NumLinea(), "+")
      
      elif ch == "-":
         return componentes.OpAdd(self.flujo.NumLinea(), "-")
      
      elif ch == "*":
         return componentes.OpMult(self.flujo.NumLinea(), "*")
      
      elif ch == "/":
         return componentes.OpMult(self.flujo.NumLinea(), "/")
      
      # Asignacion
      elif ch == ":": 
         next_ch = self.flujo.NewCar()
         if next_ch == "=":
            return componentes.OpAsigna(self.flujo.NumLinea())
         else:
            self.flujo.Devolver()
            return componentes.DosPtos(self.flujo.NumLinea()) # Cuenta como parte de 7 simbolos, pero tenemos que detectarlo para la asignacion 
         
      # 7 simbolos 
      elif ch == ";":
         return componentes.PtoComa(self.flujo.NumLinea()) 

      elif ch == ",":
         return componentes.Coma(self.flujo.NumLinea()) 

      elif ch == ".":
         return componentes.Punto(self.flujo.NumLinea()) 
      
      elif ch == "(":
         return componentes.ParentesisApertura(self.flujo.NumLinea())
      
      elif ch == ")":
         return componentes.ParentesisCierre(self.flujo.NumLinea())

      else:
         # Se ha encontrado un caracter no permitido
         print ("ERROR LEXICO  Linea " + str(self.nlinea) + " ::  Caracter " + ch + " invalido ")
         return self.Analiza()    
      
   else:
      raise Exception("Se leyó más allá del fin de fichero")

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Parametros:  --
#  Devuelve: --
#
############################################################################

if __name__=="__main__":
   if len(argv) < 2:
      print("\nUso: analex.py <Ruta al archivo>\n")
      exit(1)
   
   filename = argv[1]
   txt=open(filename)

   print ("PROGRAMA FUENTE %r \n\n"  % filename)
   i=0
   fl = flujo.Flujo(filename)
   analex=Analex(fl)
   c = analex.Analiza()
   while c:
      print (c)
      c = analex.Analiza()
      #print("\n") # Si quito esto sale igual que el suyo
   i = i + 1
   print("\n")

