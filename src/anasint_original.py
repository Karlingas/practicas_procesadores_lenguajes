#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv

class Sintactico:
    def __init__(self, lexico):
        """ Constructor de la clase que implementa el Analizador Sintactico
        Solicita el primer componente lexico """ 

        self.lexico= lexico
        self.token=self.lexico.Analiza()
        self.lista_errores = []
        self.msg_dict = {
            1: "Se espera PROGRAMA", 
            2: "Se espera IDENTIFICADOR", 
            3: "Se espera ;",
            4: "Se espera .", 
            5: "Se espera VAR o INICIO", 
            6: "Se espera (",
            7: "Se espera :", 
            8: "Se espera tipo", 
            9: "Se espera )",
            10: "Se espera INICIO", 
            11: "Se espera FIN", 
            12: "Instrucción no válida",
            13: "Se espera operador de asignación :=", 
            14: "Se espera ENTONCES", 
            15: "Se espera HACER",
            16: "Se espera operador relacional", 
            17: "Se espera factor (Id, Num, (, NO, CIERTO, FALSO)"
        }

    def Avanza(self):
        '''Avanza al siguiente elemento léxico'''
        self.token = self.lexico.Analiza()

    def Error(self, nerr):
        '''Muestra los mensajes de error y los añade a una lista'''
        linea = str(self.token.n_linea)

        error_msg = self.msg_dict.get(nerr, "Error desconocido")
        print(f"Linea: {linea} ERROR: {error_msg}")
        self.lista_errores.append((nerr, linea, error_msg))

    
    def Emparejar(self, cat, val, nerr, sync_set):
        ''' Modo Pánico. Lanza error si el token actual no es el esperado. 
            Intenta sincronizar para seguir analizando en caso de error. '''
        if self.token.cat == cat and (val is None or self.token.valor == val):
            # Todo perfecto
            self.Avanza()
            return True
        self.Error(nerr)

        if self.Token_en_set(sync_set):    # Si esta en los siguientes esperados 
            return True                     # Asumimos que el token faltaba y continuamos

        # Consumimos tokens no válidos si los hay
        while self.token.cat != "EOF":
            if self.token.cat == cat and (val is None or self.token.valor == val):
                self.Avanza()
                return True
            if self.Token_en_set(sync_set):
                return True
            self.Avanza()
        return False  # No se ha conseguido la sincronizacion

    def Token_en_set(self, token_set):
        '''Devuelve si el token actual está en token_set'''
        return (self.token.cat in token_set) or \
               (self.token.cat == "PR" and self.token.valor in token_set) # Si es una PR hay que comprobar el valor (que PR es en concreto)


    '''REGLAS GRAMATICALES'''

    # <Programa> → PROGRAMA id ; <decl_var> <instrucciones> .
    def AnalizaPrograma(self):
        if not self.Emparejar("PR", "PROGRAMA", 1, ["Identif", "PtoComa", "VAR", "INICIO"]):
            return
        if not self.Emparejar("Identif", None, 2, ["PtoComa", "VAR", "INICIO"]):
            return
        if not self.Emparejar("PtoComa", None, 3, ["VAR", "INICIO"]):
            return

        self.AnalizaDeclVar(sync_set=["INICIO"]) # Pasamos quien sigue después
        self.AnalizaInstrucciones(sync_set=["Punto"])
        
        self.Emparejar("Punto", None, 4, ["EOF"])

    # <decl_var> → VAR ( <lista_id> : <tipo_std> ; <decl_v> ) | λ
    def AnalizaDeclVar(self, sync_set):
        if self.token.cat == "PR" and self.token.valor == "VAR":
            self.Avanza()
            
            self.AnalizaListaId(sync_set=["DosPtos"])
            self.Emparejar("DosPtos", None, 7, ["ENTERO", "REAL", "BOOLEANO", "PtoComa"])
            self.AnalizaTipoStd()
            self.Emparejar("PtoComa", None, 3, ["Identif"] + sync_set)
            
            # Recursividad para las declaraciones adicionales
            self.AnalizaDeclV(sync_set) 
        else:
            # λ (Lambda), Si no es VAR no hacemos nada (siempre que venga algo válido después)
            if not self.Token_en_set(sync_set):
                # Si lo que viene no es INICIO, entonces sí es un error
                self.Error(5)

    # <decl_v> → <lista_id> : <tipo_std> ; <decl_v> | λ -> Recursivo
    def AnalizaDeclV(self, sync_set):
        if self.token.cat == "Identif":
            # Parte repetitiva
            self.AnalizaListaId(sync_set=["DosPtos"])
            self.Emparejar("DosPtos", None, 7, ["ENTERO", "REAL", "BOOLEANO", "PtoComa"])
            self.AnalizaTipoStd()
            self.Emparejar("PtoComa", None, 3, ["Identif"] + sync_set)
            
            self.AnalizaDeclV(sync_set) 
        else:
            # λ (Fin de la recursion)
            pass

    # <lista_id> → id <resto_listaid>
    def AnalizaListaId(self, sync_set):
        # lo que venga después de id debe ser aceptado por resto_listaid
        siguiente_sync = sync_set + ["Coma"]
        self.Emparejar("Identif", None, 2, siguiente_sync)
        self.AnalizaRestoListaId(sync_set)

    # <resto_listaid> → , <lista_id> | λ
    def AnalizaRestoListaId(self, sync_set):
        if self.token.cat == "Coma":
            self.Avanza()
            self.AnalizaListaId(sync_set) # Vuelve a llamar a ListaId
        else:
            # λ
            pass

    # <Tipo_std> → ENTERO | REAL | BOOLEANO
    def AnalizaTipoStd(self):
        if self.token.cat == "PR" and self.token.valor in ["ENTERO", "REAL", "BOOLEANO"]:
            self.Avanza()
        else:
            self.Error(8)

    # <instrucciones> → INICIO ( <instrucción> ; )* FIN
    def AnalizaInstrucciones(self, sync_set):
        primeros_inst = ["Identif", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
        
        if not self.Emparejar("PR", "INICIO", 10, primeros_inst + ["FIN"]):
            return
        
        # cadena recursiva de instrucciones
        self.AnalizaBloqueInstrucciones(sync_set=["FIN"] + primeros_inst)
        
        if not self.Emparejar("PR", "FIN", 11, sync_set):
            return 

    # Función auxiliar recursiva para ( <instrucción> ; )*
    def AnalizaBloqueInstrucciones(self, sync_set):
        primeros_inst = ["Identif", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
        
        # Si el token actual puede empezar una instrucción
        if self.Token_en_set(primeros_inst):
            self.AnalizaInstruccion(sync_set)
            if not self.Emparejar("PtoComa", None, 3, primeros_inst + ["FIN"]):
                return 
            
            # RECURSION para ver si hay otra instrucción
            self.AnalizaBloqueInstrucciones(sync_set)
        else:
            # λ (Si encontramos FIN o algo del sync_set)
            pass

    # <instrucción>
    def AnalizaInstruccion(self, sync_set):
        siguiente_sync = sync_set + ["PtoComa", "SINO", "ENTONCES", "HACER"]

        if self.token.cat == "Identif":
            self.AnalizaInstSimple(siguiente_sync)
        elif self.token.cat == "PR":
            v = self.token.valor
            if v in ["LEE", "ESCRIBE"]:
                self.AnalizaInstES(siguiente_sync)
            elif v == "SI":
                self.Avanza()
                self.AnalizaExpresion(siguiente_sync + ["ENTONCES"])
                if not self.Emparejar("PR", "ENTONCES", 14, ["INICIO"]):
                    return 
                self.AnalizaInstrucciones(siguiente_sync + ["SINO"])
                if self.token.cat == "PR" and self.token.valor == "SINO":
                    self.Avanza()
                    self.AnalizaInstrucciones(siguiente_sync)
            elif v == "MIENTRAS":
                self.Avanza()
                self.AnalizaExpresion(siguiente_sync + ["HACER"])
                if not self.Emparejar("PR", "HACER", 15, ["INICIO"]):
                    return 
                self.AnalizaInstrucciones(siguiente_sync)
            else:
                self.Error(12)
        else:
            self.Error(12)

    # <Inst_simple> → id opasigna <expresión>
    def AnalizaInstSimple(self, sync_set):
        self.Avanza() # Id
        if not self.Emparejar("OpAsigna", None, 13, ["Identif", "Numero", "ParentesisApertura", "NO"]):
            return 
        self.AnalizaExpresion(sync_set)

    # <inst_e/s>
    def AnalizaInstES(self, sync_set):
        tipo = self.token.valor 
        self.Avanza()
        if not self.Emparejar("ParentesisApertura", None, 6, ["Identif", "Numero"]):
            return 
        if tipo == "LEE":
            if not self.Emparejar("Identif", None, 2, ["ParentesisCierre"]):
                return 
        else:
            self.AnalizaExprSimple(sync_set + ["ParentesisCierre"]) 
        if not self.Emparejar("ParentesisCierre", None, 9, sync_set):
            return 

    # <expresion> → <expr_simple> <expresion’>
    def AnalizaExpresion(self, sync_set):
        self.AnalizaExprSimple(sync_set + ["OpRel"])
        self.AnalizaExpresionPrima(sync_set)

    # <expresión’> → oprel <expr_simple> | λ
    def AnalizaExpresionPrima(self, sync_set):
        if self.token.cat == "OpRel":
            self.Avanza()
            self.AnalizaExprSimple(sync_set)
        # λ

    # <expr_simple> → <termino> <expr_simple’>
    def AnalizaExprSimple(self, sync_set):
        self.AnalizaTermino(sync_set + ["OpAdd", "O"])
        self.AnalizaExprSimplePrima(sync_set)

    # <expr_simple’> → opsuma <término> | O <término> | λ
    # Lo hacemos recursivo para poder hacer "a + b + c"
    def AnalizaExprSimplePrima(self, sync_set):
        if self.token.cat == "OpAdd" or (self.token.cat == "PR" and self.token.valor == "O"):
            self.Avanza()
            self.AnalizaTermino(sync_set + ["OpAdd", "O"])
            # Llamada recursiva para permitir múltiples sumas o multiplicaciones: 1 + 2 + 3
            self.AnalizaExprSimplePrima(sync_set) 
        # λ

    # <término> → <factor> <resto_term>
    def AnalizaTermino(self, sync_set):
        self.AnalizaFactor(sync_set + ["OpMult", "Y"])
        self.AnalizaRestoTerm(sync_set)

    # <resto_term> → opmult <factor> <resto_term> | Y <factor> <resto_term> | λ
    def AnalizaRestoTerm(self, sync_set):
        if self.token.cat == "OpMult" or (self.token.cat == "PR" and self.token.valor == "Y"):
            self.Avanza()
            self.AnalizaFactor(sync_set + ["OpMult", "Y"])
            self.AnalizaRestoTerm(sync_set)
        # λ

    # <factor> → id | num | ( <expresión> ) | NO <factor> | CIERTO | FALSO
    def AnalizaFactor(self, sync_set):
        validos = ["Identif", "Numero", "Entero", "Real"]
        
        if self.token.cat in validos:
            self.Avanza()
        elif self.token.cat == "PR" and self.token.valor in ["CIERTO", "FALSO"]:
            self.Avanza()
        elif self.token.cat == "PR" and self.token.valor == "NO":
            self.Avanza()
            self.AnalizaFactor(sync_set) # Recursión: NO factor
        elif self.token.cat == "ParentesisApertura":
            self.Avanza()
            self.AnalizaExpresion(["ParentesisCierre"])
            if not self.Emparejar("ParentesisCierre", None, 9, sync_set):
                return 
        else: # Puede ser varios tóken, por lo que lanzamos el error sin llamar a Emparejar
            self.Error(17) # Se esperaba factor
            # Sincronización
            if not self.Token_en_set(sync_set):
                self.Avanza()
       

 
########################################################
##
## Programa principal que lanza el analizador sintactico
####################################################
if __name__=="__main__":
    if len(argv) < 2:
      print("\nUso: anasint.py <Ruta al archivo>\n")
      exit(1)
   
    filename = argv[1] 
    #filename = "./Tests/Prueba1_MAL.eje"
    print ("PROGRAMA FUENTE %r \n\n"  % filename)

    fl = flujo.Flujo(filename)
    anlex=analex.Analex(fl)
    S = Sintactico(anlex)
    S.AnalizaPrograma()
    if not S.lista_errores:
        print ("Analisis sintactico SATISFACTORIO. Fichero :", filename, "CORRECTO")
    else:
        print ("Analisis sintactico CON ERRORES. Fichero :", filename, "ERRONEO")
        print ("\nLista de errores: (Nºerror, línea, mensaje)\n", S.lista_errores)