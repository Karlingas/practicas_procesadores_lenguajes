#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv
""" dict_siguientes = {
    "Programa": ["EOF"],
    "decl_var": ["INICIO"],
    "decl_v": [")"],
    "lista_id": [":"],
    "resto_listaid": [":"],
    "Tipo_std": [";"],
    "instrucciones": [".", "SINO", ";"],
    "instrucción": [";"],
    "Inst_simple": [";"],
    "inst_e/s": [";"],
    "expresión": ["ENTONCES", "HACER", ")", ";"],
    "expresión’": ["ENTONCES", "HACER", ")", ";"],
    "expr_simple": [")", "oprel", "ENTONCES", "HACER", ";"],
    "expr_simple’": [")", "oprel", "ENTONCES", "HACER"],
    "término": ["opsuma", "O", ")", "oprel", "ENTONCES", "HACER"],
    "resto_term": ["opsuma", "O", ")", "oprel", "ENTONCES", "HACER"],
    "factor": ["opmult", "Y", "opsuma", "O", ")", "oprel", "ENTONCES", "HACER"]
} """

class Sintactico:

#Constructor de la clase que implementa el Analizador Sintactico
#Solicita el primer componente lexico 
    def __init__(self, lexico):
        self.lexico= lexico
        self.token=self.lexico.Analiza()
        self.lista_errores = []

    def Avanza(self):
        self.token = self.lexico.Analiza()

# Funcion que muestra los mensajes de error
    def Error(self, nerr):
        error_msg = "Error desconocido"
        linea = str(self.token.n_linea)
        
        if nerr == 1: 
            error_msg = "Se espera PROGRAMA"
        elif nerr == 2: 
            error_msg = "Se espera IDENTIFICADOR"
        elif nerr == 3: 
            error_msg = "Se espera ;"
        elif nerr == 4: 
            error_msg = "Se espera ."
        elif nerr == 5: 
            error_msg = "Se espera VAR o INICIO"
        elif nerr == 6: 
            error_msg = "Se espera ("
        elif nerr == 7: 
            error_msg = "Se espera :"
        elif nerr == 8: 
            error_msg = "Se espera tipo (ENTERO, REAL, BOOLEANO)"
        elif nerr == 9: 
            error_msg = "Se espera )"
        elif nerr == 10: 
            error_msg = "Se espera INICIO"
        elif nerr == 11: 
            error_msg = "Se espera FIN"
        elif nerr == 12: 
            error_msg = "Se espera una instrucción válida (Id, LEE, ESCRIBE, SI, MIENTRAS)"
        elif nerr == 13: 
            error_msg = "Se espera operador de asignación :="
        elif nerr == 14: 
            error_msg = "Se espera ENTONCES"
        elif nerr == 15: 
            error_msg = "Se espera HACER"
        elif nerr == 16: 
            error_msg = "Se espera operador relacional"
        elif nerr == 17: 
            error_msg = "Se espera factor (Id, Num, (, NO, CIERTO, FALSO)"
        
        print(f"Linea: {linea} ERROR: {error_msg}")

        self.lista_errores.add((nerr,linea,error_msg))


    # <Programa> → PROGRAMA id ; <decl_var> <instrucciones> .
    def AnalizaPrograma(self):
        if self.token.cat != "PR" or self.token.valor != "PROGRAMA":
            self.Error(1)
            return False 
        self.Avanza()

        if self.token.cat != "Identif":
            self.Error(2)
            return False
        self.Avanza()

        if self.token.cat != "PtoComa":
            self.Error(3)
            return False
        self.Avanza()

        if not self.AnalizaDeclVar(): return False
        if not self.AnalizaInstrucciones(): return False

        if self.token.cat != "Punto":
            self.Error(4)
            return False
        self.Avanza()
        
        print("El programa es sintácticamente correcto.")
        return True

    # <decl_var> → VAR ( <lista_id> : <tipo_std> ; <decl_v> ) | λ
    def AnalizaDeclVar(self):
        if self.token.cat == "PR" and self.token.valor == "VAR":
            self.Avanza()
            
            if self.token.cat != "ParentesisApertura":
                self.Error(6)
                return False
            self.Avanza()

            if not self.AnalizaListaId(): return False

            if self.token.cat != "DosPtos":
                self.Error(7)
                return False
            self.Avanza()

            if not self.AnalizaTipoStd(): return False

            if self.token.cat != "PtoComa":
                self.Error(3)
                return False
            self.Avanza()

            # Recursión
            if not self.AnalizaDeclV(): return False

            if self.token.cat != "ParentesisCierre":
                self.Error(9)
                return False
            self.Avanza()
            return True
            
        # Producción Lambda (λ) si el siguiente es INICIO
        elif self.token.cat == "PR" and self.token.valor == "INICIO":
            return True
        else:
            self.Error(5)
            return False

    # <decl_v> → ( <lista_id> : <tipo_std> ; )* -> Recursivo
    def AnalizaDeclV(self):
        if self.token.cat == "ParentesisApertura":
            self.Avanza()

            if not self.AnalizaListaId(): return False

            if self.token.cat != "DosPtos":
                self.Error(7)
                return False
            self.Avanza()

            if not self.AnalizaTipoStd(): return False

            if self.token.cat != "PtoComa":
                self.Error(3)
                return False
            self.Avanza()

            # Llamada recursiva
            return self.AnalizaDeclV()
        
        # λ
        return True

    # <lista_id> → id <resto_listaid>
    def AnalizaListaId(self):
        if self.token.cat != "Identif":
            self.Error(2)
            return False
        self.Avanza()
        return self.AnalizaRestoListaId()

    # <resto_listaid> → , <lista_id> | λ
    def AnalizaRestoListaId(self):
        if self.token.cat == "Coma":
            self.Avanza()
            return self.AnalizaListaId()
        return True

    # <Tipo_std> → ENTERO | REAL | BOOLEANO
    def AnalizaTipoStd(self):
        if self.token.cat == "PR" and self.token.valor in ["ENTERO", "REAL", "BOOLEANO"]:
            self.Avanza()
            return True
        self.Error(8)
        return False

    # <instrucciones> → INICIO ( <instrucción> ; )* FIN
    def AnalizaInstrucciones(self):
        if self.token.cat != "PR" or self.token.valor != "INICIO":
            self.Error(10)
            return False
        self.Avanza()

        if not self.AnalizaBloqueInstrucciones(): return False

        if self.token.cat != "PR" or self.token.valor != "FIN":
            self.Error(11)
            return False
        self.Avanza()
        return True

    # Auxiliar recursivo para el bloque de instrucciones
    def AnalizaBloqueInstrucciones(self):
        # Primeros(<instrucción>) = {id, LEE, ESCRIBE, SI, MIENTRAS}
        es_instruccion = (self.token.cat == "Identif") or \
                         (self.token.cat == "PR" and self.token.valor in ["LEE", "ESCRIBE", "SI", "MIENTRAS"])
        
        if es_instruccion:
            if not self.AnalizaInstruccion(): return False
            
            if self.token.cat != "PtoComa":
                self.Error(3)
                return False
            self.Avanza()

            # Recursión
            return self.AnalizaBloqueInstrucciones()
        
        # λ (si viene FIN)
        return True

    # <instrucción>
    def AnalizaInstruccion(self):
        if self.token.cat == "Identif":
            return self.AnalizaInstSimple()
            
        elif self.token.cat == "PR":
            v = self.token.valor
            if v == "LEE" or v == "ESCRIBE":
                return self.AnalizaInstES()
            elif v == "SI":
                self.Avanza()
                if not self.AnalizaExpresion(): return False
                
                if self.token.cat != "PR" or self.token.valor != "ENTONCES":
                    self.Error(14)
                    return False
                self.Avanza()
                
                if not self.AnalizaInstrucciones(): return False
                
                if self.token.cat == "PR" and self.token.valor == "SINO":
                    self.Avanza()
                    if not self.AnalizaInstrucciones(): return False
                return True
                
            elif v == "MIENTRAS":
                self.Avanza()
                if not self.AnalizaExpresion(): return False
                
                if self.token.cat != "PR" or self.token.valor != "HACER":
                    self.Error(15)
                    return False
                self.Avanza()
                
                return self.AnalizaInstrucciones()
                
        self.Error(12)
        return False

    # <Inst_simple> → id opasigna <expresión>
    def AnalizaInstSimple(self):
        # Se asume que el Id ya se verificó en el lookahead, pero lo consumimos
        if self.token.cat != "Identif":
            self.Error(2)
            return False
        self.Avanza()

        if self.token.cat != "OpAsigna":
            self.Error(13)
            return False
        self.Avanza()

        return self.AnalizaExpresion()

    # <inst_e/s>
    def AnalizaInstES(self):
        tipo = self.token.valor # LEE o ESCRIBE
        self.Avanza()
        
        if self.token.cat != "ParentesisApertura":
            self.Error(6)
            return False
        self.Avanza()

        if tipo == "LEE":
            if self.token.cat != "Identif":
                self.Error(2)
                return False
            self.Avanza()
        else: # ESCRIBE
            if not self.AnalizaExprSimple(): return False

        if self.token.cat != "ParentesisCierre":
            self.Error(9)
            return False
        self.Avanza()
        return True

    # <expresión>
    def AnalizaExpresion(self):
        if not self.AnalizaExprSimple(): return False
        return self.AnalizaExpresionPrima()

    # <expresión’> → oprel <expr_simple> | λ
    def AnalizaExpresionPrima(self):
        if self.token.cat == "OpRel":
            self.Avanza()
            return self.AnalizaExprSimple()
        return True

    # <expr_simple>
    def AnalizaExprSimple(self):
        if not self.AnalizaTermino(): return False
        return self.AnalizaExprSimplePrima()

    # <expr_simple’> → OpAdd <término> | O <término> | λ
    # Nota: Tu clase se llama OpAdd (no OpSuma)
    def AnalizaExprSimplePrima(self):
        es_suma = (self.token.cat == "OpAdd")
        es_or = (self.token.cat == "PR" and self.token.valor == "O")

        if es_suma or es_or:
            self.Avanza()
            if not self.AnalizaTermino(): return False
            # Recursividad
            return self.AnalizaExprSimplePrima()
        return True

    # <término>
    def AnalizaTermino(self):
        if not self.AnalizaFactor(): return False
        return self.AnalizaRestoTerm()

    # <resto_term> → OpMult <factor> | Y <factor> | λ
    def AnalizaRestoTerm(self):
        es_mult = (self.token.cat == "OpMult")
        es_and = (self.token.cat == "PR" and self.token.valor == "Y")

        if es_mult or es_and:
            self.Avanza()
            if not self.AnalizaFactor(): return False
            # Recursividad
            return self.AnalizaRestoTerm()
        return True

    # <factor> → id | num | ( <expresión> ) | NO <factor> | CIERTO | FALSO
    def AnalizaFactor(self):
        if self.token.cat == "Identif":
            self.Avanza()
            return True
        
        # Aceptamos Numero o sus herederos Entero/Real
        elif self.token.cat in ["Numero", "Entero", "Real"]:
            self.Avanza()
            return True
            
        elif self.token.cat == "PR" and self.token.valor in ["CIERTO", "FALSO"]:
            self.Avanza()
            return True
            
        elif self.token.cat == "ParentesisApertura":
            self.Avanza()
            if not self.AnalizaExpresion(): return False
            if self.token.cat != "ParentesisCierre":
                self.Error(9)
                return False
            self.Avanza()
            return True
            
        elif self.token.cat == "PR" and self.token.valor == "NO":
            self.Avanza()
            return self.AnalizaFactor()
            
        else:
            self.Error(17)
            return False
       

 
########################################################
##
## Programa principal que lanza el analizador sintactico
####################################################
if __name__=="__main__":
    if len(argv) < 2:
      print("\nUso: anasint.py <Ruta al archivo>\n")
      exit(1)
   
    filename = argv[1]


    print ("PROGRAMA FUENTE %r \n\n"  % filename)

    fl = flujo.Flujo(filename)
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