#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv
import AST 

class Sintactico:

#Constructor de la clase que implementa el Analizador Sintactico
#Solicita el primer componente lexico 
    def __init__(self, lexico):
        self.lexico= lexico
        self.token=self.lexico.Analiza()
        self.lista_errores_sintactico = []
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
        self.token = self.lexico.Analiza()

    def ErrorAnasint(self, nerr):
        '''Muestra los mensajes de error del análisis SINTÁCTICO'''
        linea = str(self.token.n_linea)

        error_msg = self.msg_dict.get(nerr, "Error desconocido")
        print(f"Linea: {linea} ERROR: {error_msg}")
        self.lista_errores_sintactico.append((nerr, linea, error_msg))

    
    def Emparejar(self, cat, val, nerr, sync_set):
        '''Modo Pánico'''
        if self.token.cat == cat and (val is None or self.token.valor == val):
            # Todo perfecto
            self.Avanza()
            return True
        self.ErrorAnasint(nerr)

        if self.Token_en_set(sync_set):    # Si esta en los siguientes esperados 
            """ if self.token.cat == "Identif":
                self.Avanza() """
            return True                     # Asumimos que el token faltaba y continuamos

        # Recuperación, consumimos tokens no válidos
        while self.token.cat != "EOF":
            if self.token.cat == cat and (val is None or self.token.valor == val):
                self.Avanza()
                return True
            if self.Token_en_set(sync_set):
                return True
            self.Avanza()
        return False

    def Token_en_set(self, token_set):
        '''Devuelve si el token actual está en token_set'''
        return (self.token.cat in token_set) or \
               (self.token.cat == "PR" and self.token.valor in token_set)


    '''REGLAS GRAMATICALES'''

    # <Programa> → PROGRAMA id ; <decl_var> <instrucciones> .
    def AnalizaPrograma(self):
        # inicilizar la tabla de símbolos
        AST.tablasimbolos.tabla = {} 

        if not self.Emparejar("PR", "PROGRAMA", 1, ["Identif", "PtoComa", "VAR", "INICIO"]):
            return
        if not self.Emparejar("Identif", None, 2, ["PtoComa", "VAR", "INICIO"]):
            return
        if not self.Emparejar("PtoComa", None, 3, ["VAR", "INICIO"]):
            return

        self.AnalizaDeclVar(sync_set=["INICIO"]) # Pasamos quien sigue después
        
        nodo_raiz = self.AnalizaInstrucciones(sync_set=["Punto"])
        
        self.Emparejar("Punto", None, 4, ["EOF"])
        
        return nodo_raiz

    # <decl_var> → VAR ( <lista_id> : <tipo_std> ; <decl_v> ) | λ
    def AnalizaDeclVar(self, sync_set):
        if self.token.cat == "PR" and self.token.valor == "VAR":
            self.Avanza()
            # Método auxiliar para la insercion en la tabla de símbolos
            self.ProcesarLineaDeclaracion(sync_set)
        else:
            # λ (Lambda), Si no es VAR no hacemos nada (siempre que venga algo válido después)
            if not self.Token_en_set(sync_set):
                # Si lo que viene no es INICIO, entonces sí es un error
                self.ErrorAnasint(5)

    # Procesa la declaración y los inserta en la tabla de símbolos
    def ProcesarLineaDeclaracion(self, sync_set):
        # <lista_id> : <tipo_std> ; <decl_v>
        
        # lista de IDs de las variables declaradas.
        lista_ids = self.AnalizaListaId(["DosPtos"])
        
        if not self.Emparejar("DosPtos", None, 7, ["ENTERO", "REAL", "BOOLEANO", "PtoComa"]): 
            return
        
        # Obtenemos el tipo de las variables declaradas.
        tipo_dato = self.AnalizaTipoStd()
        
        # para insertar todo en la tabla de símbolos
        for id_nombre in lista_ids:
            if AST.tablasimbolos.Existe(id_nombre): # Comprobar que no existen varios objetos con el mismo nombre
                AST.AST.ErrorSemantico("VAR_REDEF", self.token.n_linea, id_nombre)
            else:
                AST.tablasimbolos.Insertar(id_nombre, tipo_dato, "escalar", None) # id, tipo, naturaleza, valor

        if not self.Emparejar("PtoComa", None, 3, ["Identif"] + sync_set): 
            return
        
        # Recursión con <decl_v>
        self.AnalizaDeclV(sync_set)

    # <decl_v> → <lista_id> : <tipo_std> ; <decl_v> | λ -> Recursivo
    def AnalizaDeclV(self, sync_set):
        if self.token.cat == "Identif":
            # ahora la lógica ka lleva el metodo auxiliar para guardarlo en la tabla
            self.ProcesarLineaDeclaracion(sync_set)
        else:
            # λ (Fin de la recursion)
            pass

    # <lista_id> → id <resto_listaid>
    def AnalizaListaId(self, sync_set):
        # lo que venga después de id debe ser aceptado por resto_listaid
        lista_ids = []
        if self.token.cat == "Identif": # Como tiene que ser un ID, si es una PR se irá al else y dará error
            lista_ids.append(self.token.nombre) # Guardamos el nombre
            siguiente_sync = sync_set + ["Coma"]
            self.Avanza() # Consumimos el ID manualmente aquí porque necesitamos su valor antes
        else:
            self.Emparejar("Identif", None, 2, siguiente_sync) # error
   
        lista_ids.extend(self.AnalizaRestoListaId(sync_set))
        return lista_ids

    # <resto_listaid> → , <lista_id> | λ
    def AnalizaRestoListaId(self, sync_set):
        lista_ids = []
        if self.token.cat == "Coma":
            self.Avanza()
            lista_ids.extend(self.AnalizaListaId(sync_set)) 
        else:
            # λ
            pass
        return lista_ids

    # <Tipo_std> → ENTERO | REAL | BOOLEANO
    def AnalizaTipoStd(self):
        tipo = None
        if self.token.cat == "PR" and self.token.valor in ["ENTERO", "REAL", "BOOLEANO"]:
            tipo = self.token.valor
            self.Avanza()
        else:
            self.ErrorAnasint(8)
            tipo = "ERROR"
        return tipo

    # <instrucciones> → INICIO ( <instrucción> ; )* FIN
    def AnalizaInstrucciones(self, sync_set):
        primeros_inst = ["Identif", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
        
        if not self.Emparejar("PR", "INICIO", 10, primeros_inst + ["FIN"]):
            return None
        
        # cadena recursiva de instrucciones
        lista_nodos = self.AnalizaBloqueInstrucciones(sync_set=["FIN"] + primeros_inst) # Guardamos la lista de nodos sentencia
        
        if not self.Emparejar("PR", "FIN", 11, sync_set):
            return None
        
        # Devolvemos un nodo compuesta con todas las sentencias
        return AST.NodoCompuesta(lista_nodos, 0)

    # Función auxiliar recursiva para ( <instrucción> ; )*
    def AnalizaBloqueInstrucciones(self, sync_set):
        lista = []
        primeros_inst = ["Identif", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
        
        # Si el token actual puede empezar una instrucción
        if self.Token_en_set(primeros_inst):
            # Guardamos el nodo de la instrucción
            nodo = self.AnalizaInstruccion(sync_set)
            if nodo: 
                lista.append(nodo)

            if not self.Emparejar("PtoComa", None, 3, primeros_inst + ["FIN"]):
                return lista
            
            # RECURSION para ver si hay otra instrucción
            # Extendemos la lista actual con lo que venga de la recursión
            lista.extend(self.AnalizaBloqueInstrucciones(sync_set))
        else:
            # λ (Si encontramos FIN o algo del sync_set)
            pass
        
        return lista

    # <instrucción>
    def AnalizaInstruccion(self, sync_set):
        siguiente_sync = sync_set + ["PtoComa", "SINO", "ENTONCES", "HACER"]
        linea = self.token.n_linea
        nodo_resultante = AST.NodoVacio(linea) # Por defecto, en caso de que haya un error

        if self.token.cat == "Identif":
            nodo_resultante = self.AnalizaInstSimple(siguiente_sync)
        
        elif self.token.cat == "PR":
            v = self.token.valor
            if v in ["LEE", "ESCRIBE"]:
                nodo_resultante = self.AnalizaInstES(siguiente_sync)
            
            elif v == "SI":
                self.Avanza()
                #AnalizaExpresion devuelve un nodo condicion
                condicion = self.AnalizaExpresion(siguiente_sync + ["ENTONCES"])
                if not self.Emparejar("PR", "ENTONCES", 14, ["INICIO"]):
                    return None
                
                # Guaramos instrucción SI
                inst_si = self.AnalizaInstruccion(siguiente_sync + ["SINO"])
                
                inst_sino = None
                if self.token.cat == "PR" and self.token.valor == "SINO":
                    self.Avanza()
                    # Guardamos instrucción SINO
                    inst_sino = self.AnalizaInstruccion(siguiente_sync)
                
                nodo_resultante = AST.NodoSi(condicion, inst_si, inst_sino, linea)

            elif v == "MIENTRAS":
                self.Avanza()
                # guardamos condicion y cuerpo
                condicion = self.AnalizaExpresion(siguiente_sync + ["HACER"])
                if not self.Emparejar("PR", "HACER", 15, ["INICIO"]):
                    return None
                instruccion = self.AnalizaInstruccion(siguiente_sync)
                
                nodo_resultante = AST.NodoMientras(condicion, instruccion, linea)
            
            elif v == "INICIO":
                # Bloque anidado, llamamos a AnalizaInstrucciones que devuelve NodoCompuesta
                nodo_resultante = self.AnalizaInstrucciones(siguiente_sync)
            else:
                self.ErrorAnasint(12)
        else:
            self.ErrorAnasint(12)
        
        return nodo_resultante

    # <Inst_simple> → id opasigna <expresión>
    def AnalizaInstSimple(self, sync_set):
        id_nombre = self.token.nombre
        linea = self.token.n_linea
        self.Avanza() # Id
        
        if not self.Emparejar("OpAsigna", None, 13, ["Identif", "Numero", "ParentesisApertura", "NO"]):
            return None
        
        # Obtenemos el nodo expresión y creamos la Asignación
        expresion = self.AnalizaExpresion(sync_set)
        # Si tiene valor es un literal, guardamos su valor en la tabla
        if hasattr(expresion, 'valor'):
            try:
                AST.tablasimbolos.ModificarValor(id_nombre, expresion.valor)
            except Exception as e:
                print(f"Error: No se pudo actualizar valor en tabla: {e}")
        else: # Si es una expresión, guardamos su AST como objeto
            try:
                AST.tablasimbolos.ModificarValor(id_nombre, expresion) 
            except Exception as e:
                # Si la variable no existe en la tabla es un error semántico previo asi que no hacemos nada
                pass

        return AST.NodoAsignacion(id_nombre, expresion, linea)

    # <inst_e/s>
    def AnalizaInstES(self, sync_set):
        tipo = self.token.valor
        linea = self.token.n_linea
        self.Avanza()
        if not self.Emparejar("ParentesisApertura", None, 6, ["Identif", "Numero"]):
            return None
        
        nodo = None
        if tipo == "LEE":
            # solo variables
            nombre_var = self.token.nombre
            if not self.Emparejar("Identif", None, 2, ["ParentesisCierre"]):
                return None
            nodo = AST.NodoLee(nombre_var, linea)
        elif tipo == "ESCRIBE":# ESCRIBE
            # acepta expresiones
            expr = self.AnalizaExpresion(sync_set + ["ParentesisCierre"])
            nodo = AST.NodoEscribe(expr, linea)
        else:
            self.ErrorAnasint(12) # No se muy bien qué error debería ir
            return None

        if not self.Emparejar("ParentesisCierre", None, 9, sync_set):
            return None
        return nodo

    # <expresion> → <expr_simple> <expresion’>
    def AnalizaExpresion(self, sync_set):
        # Obtenemos parte izquierda y la pasamos como heredada
        izq = self.AnalizaExprSimple(sync_set + ["OpRel"])
        return self.AnalizaExpresionPrima(sync_set, izq)

    # <expresión’> → oprel <expr_simple> | λ
    def AnalizaExpresionPrima(self, sync_set, heredado):
        if self.token.cat == "OpRel":
            op = self.token.valor
            linea = self.token.n_linea
            self.Avanza()
            dcha = self.AnalizaExprSimple(sync_set)
            # Construimos nodo comparacion
            return AST.NodoComparacion(heredado, dcha, linea, op)
        # λ -> Si no hay parte derecha, devolvemos lo que heredamos
        return heredado

    # <expr_simple> → <termino> <expr_simple’>
    def AnalizaExprSimple(self, sync_set):
        # Parte izquierda y la pasamos
        izq = self.AnalizaTermino(sync_set + ["OpAdd", "O"])
        return self.AnalizaExprSimplePrima(sync_set, izq)

    # <expr_simple’> → opsuma <término> | O <término> | λ
    # Lo hacemos recursivo para poder hacer "a + b + c +..."
    def AnalizaExprSimplePrima(self, sync_set, heredado):
        if self.token.cat == "OpAdd" or (self.token.cat == "PR" and self.token.valor == "O"):
            op = self.token.valor
            linea = self.token.n_linea
            self.Avanza()
            
            dcha = self.AnalizaTermino(sync_set + ["OpAdd", "O"])
            
            # Creamos el nodo binario (Aritmetico o Logico)
            if op == 'O':
                 nuevo_nodo = AST.NodoLogico(heredado, dcha, linea, op)
            else:
                 nuevo_nodo = AST.NodoAritmetico(heredado, dcha, linea, op)

            # Llamada recursiva para permitir múltiples sumas o multiplicaciones: 1 + 2 + 3
            # Pasamos el nuevo nodo como izquierdo para la siguiente operación
            return self.AnalizaExprSimplePrima(sync_set, nuevo_nodo) 
        # λ
        return heredado

    # <término> → <factor> <resto_term>
    def AnalizaTermino(self, sync_set):
        # Obtenemos factor y lo pasamos
        izq = self.AnalizaFactor(sync_set + ["OpMult", "Y"])
        return self.AnalizaRestoTerm(sync_set, izq)

    # <resto_term> → opmult <factor> <resto_term> | Y <factor> <resto_term> | λ
    def AnalizaRestoTerm(self, sync_set, heredado):
        if self.token.cat == "OpMult" or (self.token.cat == "PR" and self.token.valor == "Y"):
            op = self.token.valor
            linea = self.token.n_linea
            self.Avanza()
            
            dcha = self.AnalizaFactor(sync_set + ["OpMult", "Y"])
            
            #Creamos el nodo binario como antes
            if op == 'Y':
                nuevo_nodo = AST.NodoLogico(heredado, dcha, linea, op)
            else:
                nuevo_nodo = AST.NodoAritmetico(heredado, dcha, linea, op)

            return self.AnalizaRestoTerm(sync_set, nuevo_nodo)
        # λ
        return heredado

    # <factor> → id | num | ( <expresión> ) | NO <factor> | CIERTO | FALSO
    def AnalizaFactor(self, sync_set):
        validos = ["Identif", "Numero", "Entero", "Real"]
        linea = self.token.n_linea
        nodo = None
        
        # Construcción de nodos hoja 
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
        elif self.token.cat == "PR" and self.token.valor == "NO":
            self.Avanza()
            hijo = self.AnalizaFactor(sync_set) # Recursión: NO factor
            # negación usando NodoLogico
            nodo = AST.NodoLogico(hijo, hijo, linea, "NO")
        elif self.token.cat == "ParentesisApertura":
            self.Avanza()
            nodo = self.AnalizaExpresion(["ParentesisCierre"])
            if not self.Emparejar("ParentesisCierre", None, 9, sync_set):
                return None
        else:
            self.ErrorAnasint(17) # Se esperaba factor
            # Sincronización si falló el factor
            if not self.Token_en_set(sync_set):
                self.Avanza()
            nodo = AST.NodoVacio(linea)
       
        return nodo

 
########################################################
##
## Programa principal que lanza el analizador sintactico
####################################################
if __name__=="__main__":
    """ if len(argv) < 2:
      print("\nUso: anasint.py <Ruta al archivo>\n")
      exit(1)
   
    filename = argv[1]  """
    filename = "./Tests/Prueba2.eje"
    print ("PROGRAMA FUENTE %r \n\n"  % filename)

    fl = flujo.Flujo(filename)
    anlex=analex.Analex(fl)
    S = Sintactico(anlex)
    
    arbol = S.AnalizaPrograma()

    if not S.lista_errores_sintactico:
        print ("\nAnálisis SINTÁCTICO SATISFACTORIO.")
    else:
        print ("\nAnálisis SINTÁCTICO CON ERRORES.")
        print ("\nLista de errores sintácticos: (Nºerror, línea, mensaje)\n", S.lista_errores_sintactico)

    # TODO: Indicar si el analisis SEMÁNTICO termino SATISFACTORIAMENTE o CON ERRORES
    if not AST.AST.lista_errores_semantico:
        print ("\nAnálisis SEMÁNTICO SATISFACTORIO.")
    else:
        print ("\nAnálisis SEMÁNTICO FINALIZADO CON ERRORES.")
        print ("\nLista errores semánticos: (Línea, Mensaje)\n", AST.AST.lista_errores_semantico)

    print ("\nTabla de Simbolos Final:\n", AST.tablasimbolos.tabla)

    print ("\nArbol de Sintaxis (AST):\n")
    print(arbol)