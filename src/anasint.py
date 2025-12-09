#!/usr/bin/env python

import componentes
import flujo
import analex
import sys
from sys import argv
import AST  # Importamos el módulo con los nodos y la tabla

class Sintactico:

    def __init__(self, lexico):
        self.lexico = lexico
        self.token = self.lexico.Analiza()
        self.lista_errores = []
        # Mapa de mensajes de error...
        self.msg_dict = {
            1: "Se espera PROGRAMA", 
            2: "Se espera IDENTIFICADOR", 
            3: "Se espera ;",
            4: "Se espera .", 
            5: "Se espera VAR o INICIO", 
            6: "Se espera (",
            7: "Se espera :", 
            8: "Se espera tipo (ENTERO, REAL, BOOLEANO)", 
            9: "Se espera )",
            10: "Se espera INICIO", 
            11: "Se espera FIN", 
            12: "Instrucción no válida",
            13: "Se espera operador de asignación :=", 
            14: "Se espera ENTONCES", 
            15: "Se espera HACER",
            16: "Se espera operador relacional", 
            17: "Se espera factor",
            18: "Identificador redeclarado"
        }

    def Avanza(self):
        self.token = self.lexico.Analiza()

    def Error(self, nerr):
        linea = str(self.token.n_linea)
        error_msg = self.msg_dict.get(nerr, "Error desconocido")
        print(f"Linea: {linea} ERROR Sintáctico: {error_msg}")
        self.lista_errores.append((nerr, linea, error_msg))

    def Emparejar(self, cat, val, nerr, sync_set):
        if self.token.cat == cat and (val is None or self.token.valor == val):
            self.Avanza()
            return True
        self.Error(nerr)
        # Modo pánico simple
        if self.Token_en_set(sync_set):
            return True
        while self.token.cat != "EOF":
            self.Avanza()
            if self.token.cat == cat and (val is None or self.token.valor == val):
                self.Avanza()
                return True
            if self.Token_en_set(sync_set):
                return True
        return False

    def Token_en_set(self, token_set):
        return (self.token.cat in token_set) or \
               (self.token.cat == "PR" and self.token.valor in token_set)

    # -------------------------------------------------------------------------
    # PROGRAMA PRINCIPAL
    # -------------------------------------------------------------------------
    # <Programa> → PROGRAMA id ; <decl_var> <instrucciones> .
    def AnalizaPrograma(self):
        # Reiniciar tabla de símbolos al inicio
        AST.tablasimbolos.tabla = {} 

        if not self.Emparejar("PR", "PROGRAMA", 1, ["Identif"]): return
        if not self.Emparejar("Identif", None, 2, ["PtoComa"]): return
        if not self.Emparejar("PtoComa", None, 3, ["VAR", "INICIO"]): return

        self.AnalizaDeclVar(sync_set=["INICIO"])
        
        # Obtenemos el nodo raíz de las instrucciones
        nodo_raiz = self.AnalizaInstrucciones(sync_set=["Punto"])
        
        self.Emparejar("Punto", None, 4, ["EOF"])
        
        return nodo_raiz

    # -------------------------------------------------------------------------
    # DECLARACIONES
    # -------------------------------------------------------------------------
    def AnalizaDeclVar(self, sync_set):
        if self.token.cat == "PR" and self.token.valor == "VAR":
            self.Avanza()
            self.ProcesarLineaDeclaracion(sync_set)
        else:
            # Lambda
            if not self.Token_en_set(sync_set): self.Error(5)

    def ProcesarLineaDeclaracion(self, sync_set):
        # <lista_id> : <tipo_std> ; <decl_v>
        # 1. Obtener lista de IDs
        lista_ids = self.AnalizaListaId(["DosPtos"])
        
        if not self.Emparejar("DosPtos", None, 7, ["ENTERO", "REAL", "BOOLEANO"]): return
        
        # 2. Obtener Tipo
        tipo_dato = self.AnalizaTipoStd()
        
        # 3. Insertar en Tabla de Símbolos 
        for id_nombre in lista_ids:
            if AST.tablasimbolos.Existe(id_nombre):
                print(f"ERROR Semántico: Variable '{id_nombre}' redefinida.")
            else:
                # Insertamos (Tipo, Naturaleza, Valor=None)
                AST.tablasimbolos.Insertar(id_nombre, tipo_dato, "escalar", None)

        if not self.Emparejar("PtoComa", None, 3, ["Identif"] + sync_set): return
        
        # Recursión: <decl_v>
        self.AnalizaDeclV(sync_set)

    def AnalizaDeclV(self, sync_set):
        if self.token.cat == "Identif":
            self.ProcesarLineaDeclaracion(sync_set)
        # else: Lambda

    def AnalizaListaId(self, sync_set):
        lista = []
        if self.token.cat == "Identif":
            lista.append(self.token.nombre) # Guardamos el nombre
            self.Avanza()
            lista.extend(self.AnalizaRestoListaId(sync_set))
        return lista

    def AnalizaRestoListaId(self, sync_set):
        lista = []
        if self.token.cat == "Coma":
            self.Avanza()
            lista.extend(self.AnalizaListaId(sync_set))
        return lista

    def AnalizaTipoStd(self):
        tipo = None
        if self.token.cat == "PR" and self.token.valor in ["ENTERO", "REAL", "BOOLEANO"]:
            tipo = self.token.valor
            self.Avanza()
        else:
            self.Error(8)
            tipo = "ERROR"
        return tipo

    # -------------------------------------------------------------------------
    # INSTRUCCIONES
    # -------------------------------------------------------------------------
    def AnalizaInstrucciones(self, sync_set):
        primeros_inst = ["Identif", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
        
        if not self.Emparejar("PR", "INICIO", 10, primeros_inst + ["FIN"]): return None
        
        lista_nodos = self.AnalizaBloqueInstrucciones(sync_set=["FIN"] + primeros_inst)
        
        if not self.Emparejar("PR", "FIN", 11, sync_set): return None
        
        # Devolvemos un nodo compuesta con todas las sentencias
        return AST.NodoCompuesta(lista_nodos, 0)

    def AnalizaBloqueInstrucciones(self, sync_set):
        lista = []
        primeros_inst = ["Identif", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
        
        if self.Token_en_set(primeros_inst):
            nodo = self.AnalizaInstruccion(sync_set)
            if nodo: lista.append(nodo)
            
            if not self.Emparejar("PtoComa", None, 3, primeros_inst + ["FIN"]): return lista
            
            lista.extend(self.AnalizaBloqueInstrucciones(sync_set))
        
        return lista

    def AnalizaInstruccion(self, sync_set):
        siguiente_sync = sync_set + ["PtoComa", "SINO", "ENTONCES", "HACER"]
        linea = self.token.n_linea

        if self.token.cat == "Identif":
            return self.AnalizaInstSimple(siguiente_sync)
        
        elif self.token.cat == "PR":
            v = self.token.valor
            if v in ["LEE", "ESCRIBE"]:
                return self.AnalizaInstES(siguiente_sync)
            
            elif v == "SI":
                self.Avanza()
                condicion = self.AnalizaExpresion(siguiente_sync + ["ENTONCES"])
                if not self.Emparejar("PR", "ENTONCES", 14, ["INICIO"]): return None
                
                # Instrucción del SI
                inst_si = self.AnalizaInstruccion(siguiente_sync + ["SINO"]) 
                
                inst_sino = None
                if self.token.cat == "PR" and self.token.valor == "SINO":
                    self.Avanza()
                    inst_sino = self.AnalizaInstruccion(siguiente_sync)
                
                return AST.NodoSi(condicion, inst_si, inst_sino, linea)

            elif v == "MIENTRAS":
                self.Avanza()
                condicion = self.AnalizaExpresion(siguiente_sync + ["HACER"])
                if not self.Emparejar("PR", "HACER", 15, ["INICIO"]): return None
                instruccion = self.AnalizaInstruccion(siguiente_sync)
                return AST.NodoMientras(condicion, instruccion, linea)
            
            elif v == "INICIO":
                # Bloque anidado (Sentencia Compuesta)
                return self.AnalizaInstrucciones(siguiente_sync)
                
        self.Error(12)
        return AST.NodoVacio(linea)

    def AnalizaInstSimple(self, sync_set):
        id_nombre = self.token.nombre
        linea = self.token.n_linea
        self.Avanza() # Consumir ID
        
        if not self.Emparejar("OpAsigna", None, 13, ["Identif", "Numero", "ParentesisApertura"]): return None
        
        expresion = self.AnalizaExpresion(sync_set)
        return AST.NodoAsignacion(id_nombre, expresion, linea)

    def AnalizaInstES(self, sync_set):
        tipo = self.token.valor
        linea = self.token.n_linea
        self.Avanza()
        
        if not self.Emparejar("ParentesisApertura", None, 6, ["Identif"]): return None
        
        nodo = None
        if tipo == "LEE":
            # LEE solo acepta variables simples 
            nombre_var = self.token.nombre
            if not self.Emparejar("Identif", None, 2, ["ParentesisCierre"]): return None
            nodo = AST.NodoLee(nombre_var, linea)
        else:
            # ESCRIBE acepta expresiones 
            expr = self.AnalizaExpresion(sync_set + ["ParentesisCierre"])
            nodo = AST.NodoEscribe(expr, linea)
            
        if not self.Emparejar("ParentesisCierre", None, 9, sync_set): return None
        return nodo

    # -------------------------------------------------------------------------
    # EXPRESIONES
    # -------------------------------------------------------------------------
    # <expresion> → <expr_simple> <expresion’>
    def AnalizaExpresion(self, sync_set):
        izq = self.AnalizaExprSimple(sync_set + ["OpRel"])
        # Pasamos el nodo izquierdo como atributo heredado a la parte derecha
        return self.AnalizaExpresionPrima(sync_set, izq)

    # <expresión’> → oprel <expr_simple> | λ
    def AnalizaExpresionPrima(self, sync_set, heredado):
        if self.token.cat == "OpRel":
            op = self.token.valor
            linea = self.token.n_linea
            self.Avanza()
            dcha = self.AnalizaExprSimple(sync_set)
            # Construimos el nodo comparacion
            return AST.NodoComparacion(heredado, dcha, linea, op)
        return heredado

    # <expr_simple> → <termino> <expr_simple’>
    def AnalizaExprSimple(self, sync_set):
        izq = self.AnalizaTermino(sync_set + ["OpAdd", "O"])
        return self.AnalizaExprSimplePrima(sync_set, izq)

    # <expr_simple’> → opsuma <término> <expr_simple'> | O <término> <expr_simple'> | λ
    def AnalizaExprSimplePrima(self, sync_set, heredado):
        if self.token.cat == "OpAdd" or (self.token.cat == "PR" and self.token.valor == "O"):
            op = self.token.valor
            linea = self.token.n_linea
            self.Avanza()
            
            dcha = self.AnalizaTermino(sync_set + ["OpAdd", "O"])
            
            if op == 'O':
                 nuevo_nodo = AST.NodoLogico(heredado, dcha, linea, op)
            else:
                 nuevo_nodo = AST.NodoAritmetico(heredado, dcha, linea, op)
            
            # Recursividad pasando el nuevo nodo construido como izquierdo
            return self.AnalizaExprSimplePrima(sync_set, nuevo_nodo)
        return heredado

    # <término> → <factor> <resto_term>
    def AnalizaTermino(self, sync_set):
        izq = self.AnalizaFactor(sync_set + ["OpMult", "Y"])
        return self.AnalizaRestoTerm(sync_set, izq)

    # <resto_term> → opmult <factor> <resto_term> | Y <factor> <resto_term> | λ
    def AnalizaRestoTerm(self, sync_set, heredado):
        if self.token.cat == "OpMult" or (self.token.cat == "PR" and self.token.valor == "Y"):
            op = self.token.valor
            linea = self.token.n_linea
            self.Avanza()
            
            dcha = self.AnalizaFactor(sync_set + ["OpMult", "Y"])
            
            if op == 'Y':
                nuevo_nodo = AST.NodoLogico(heredado, dcha, linea, op)
            else:
                nuevo_nodo = AST.NodoAritmetico(heredado, dcha, linea, op)
                
            return self.AnalizaRestoTerm(sync_set, nuevo_nodo)
        return heredado

    # <factor>
    def AnalizaFactor(self, sync_set):
        linea = self.token.n_linea
        nodo = None
        
        if self.token.cat == "Identif":
            nodo = AST.NodoAccesoVariable(self.token.nombre, linea)
            self.Avanza()
            
        elif self.token.cat == "Entero":
            nodo = AST.NodoEntero(self.token.valor, linea)
            self.Avanza()
            
        elif self.token.cat == "Real":
            nodo = AST.NodoReal(self.token.valor, linea)
            self.Avanza()
            
        elif self.token.cat == "PR" and self.token.valor in ["CIERTO", "FALSO"]:
            valor = 1 if self.token.valor == "CIERTO" else 0
            nodo = AST.NodoBooleano(valor, linea)
            self.Avanza()
            
        elif self.token.cat == "ParentesisApertura":
            self.Avanza()
            nodo = self.AnalizaExpresion(["ParentesisCierre"])
            if not self.Emparejar("ParentesisCierre", None, 9, sync_set): return None
            
        elif self.token.cat == "PR" and self.token.valor == "NO":
            self.Avanza()
            hijo = self.AnalizaFactor(sync_set)
            # Simular nodo negación como comparación o nodo especial (simplificado aquí)
            # Para simplificar, asumimos que 'NO' envuelve en una expresión logica o aritmetica
            # Como no tenemos NodoNegacion, usamos una logica "FALSO O x" si fuera necesario
            # pero lo correcto seria crear NodoNegacion en AST.
            # Por ahora, usamos una estructura temporal o extendemos AST:
            # (Asumo que puedes añadir NodoNegacion a AST.py, si no, usa un hack con NodoLogico)
            nodo = AST.NodoLogico(hijo, hijo, linea, "NO") # Hack temporal si no quieres editar AST mas
            
        else:
            self.Error(17)
            if not self.Token_en_set(sync_set): self.Avanza()
            nodo = AST.NodoVacio(linea)

        return nodo

if __name__=="__main__":
    #if len(argv) < 2:
    #  print("\nUso: anasint.py <Ruta al archivo>\n")
    #  exit(1)
   
    filename = r"./Tests/Prueba1.eje" #argv[1] 
    print ("PROGRAMA FUENTE %r \n\n"  % filename)

    fl = flujo.Flujo(filename)
    anlex = analex.Analex(fl)
    S = Sintactico(anlex)
    
    arbol = S.AnalizaPrograma()
    
    if not S.lista_errores:
        print ("\n--- Analisis Finalizado EXITOSAMENTE ---")
        print ("\nTabla de Simbolos Final:\n", AST.tablasimbolos.tabla)
        print ("\nArbol de Sintaxis Abstracta (AST):\n")
        print (arbol)
    else:
        print ("\n--- Analisis Finalizado con ERRORES ---")
        print (S.lista_errores)