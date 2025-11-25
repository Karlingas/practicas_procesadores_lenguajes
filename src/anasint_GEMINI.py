import componentes
import flujo
import analex
import sys
from sys import argv

class Sintactico:
    def __init__(self, lexico):
        self.lexico = lexico
        self.token = self.lexico.Analiza()
        self.lista_errores = []

    def Avanza(self):
        self.token = self.lexico.Analiza()

    def Error(self, nerr):
        error_msg = "Error desconocido"
        linea = str(self.token.n_linea)
        msg_dict = {
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
            13: "Se espera :=", 
            14: "Se espera ENTONCES",
            15: "Se espera HACER", 
            16: "Se espera op. relacional", 
            17: "Se espera factor"
        }
        if nerr in msg_dict:
            error_msg = msg_dict[nerr]
        
        print(f"Linea: {linea} ERROR: {error_msg}")
        self.lista_errores.append((nerr, linea, error_msg))

    # --- NUEVO MÉTODO CORE PARA MODO PÁNICO ---
    # sync_set: Lista de tokens (categorias o valores) que esperamos DESPUÉS de este token.
    # Sirve para saber si el programador olvidó el token actual (Inserción) o si hay basura (Borrado).
    def emparejar(self, cat, val, nerr, sync_set):
        # 1. ÉXITO
        if self.token.cat == cat and (val is None or self.token.valor == val):
            self.Avanza()
            return True
        
        self.Error(nerr)

        # 2. RECUPERACIÓN: INSERCIÓN (El token esperado falta, pero el siguiente es correcto)
        # Si el token actual está en el set de sincronización, asumimos que el esperado "existe virtualmente".
        if self.token.cat in sync_set or (self.token.cat == "PR" and self.token.valor in sync_set):
            return True 
        
        # 3. RECUPERACIÓN: MODO PÁNICO (Borrado de basura)
        # Saltamos tokens hasta encontrar el esperado o uno de sincronización
        while self.token.cat != "EOF":
            if self.token.cat == cat and (val is None or self.token.valor == val):
                self.Avanza()
                return True
            if self.token.cat in sync_set or (self.token.cat == "PR" and self.token.valor in sync_set):
                return True
            self.Avanza()
        return False

    # <Programa> → PROGRAMA id ; <decl_var> <instrucciones> .
    def AnalizaPrograma(self):
        # Si falta PROGRAMA, esperamos id, ;, VAR o INICIO
        self.emparejar("PR", "PROGRAMA", 1, ["Identif", "PtoComa", "VAR", "INICIO"])
        
        # Si falta Id, esperamos ;
        self.emparejar("Identif", None, 2, ["PtoComa", "VAR", "INICIO"])
        
        # Si falta ;, esperamos VAR o INICIO
        self.emparejar("PtoComa", None, 3, ["VAR", "INICIO"])

        self.AnalizaDeclVar()
        self.AnalizaInstrucciones()

        self.emparejar("Punto", None, 4, ["EOF"])
        
        if not self.lista_errores:
            print("El programa es sintácticamente correcto.")
        else:
            print("Proceso finalizado con errores recuperados.")
        return True

    # <decl_var> → VAR ( <lista_id> : <tipo_std> ; <decl_v> ) | λ
    def AnalizaDeclVar(self):
        if self.token.cat == "PR" and self.token.valor == "VAR":
            self.Avanza()
            self.emparejar("ParentesisApertura", None, 6, ["Identif"])
            self.AnalizaListaId()
            self.emparejar("DosPtos", None, 7, ["ENTERO", "REAL", "BOOLEANO"])
            self.AnalizaTipoStd()
            self.emparejar("PtoComa", None, 3, ["ParentesisCierre", "Identif"]) # Siguiente puede ser ) o nueva decl
            self.AnalizaDeclV()
            self.emparejar("ParentesisCierre", None, 9, ["INICIO"])
        elif self.token.cat == "PR" and self.token.valor == "INICIO":
            return True # Lambda
        else:
            self.Error(5)
            # Sincronización básica: buscar INICIO
            while self.token.cat != "EOF" and not (self.token.cat == "PR" and self.token.valor == "INICIO"):
                self.Avanza()
        return True

    # <decl_v> Recursivo
    def AnalizaDeclV(self):
        if self.token.cat == "ParentesisApertura": # Inicio de nueva declaración
            self.Avanza()
            self.AnalizaListaId()
            self.emparejar("DosPtos", None, 7, ["ENTERO", "REAL", "BOOLEANO"])
            self.AnalizaTipoStd()
            self.emparejar("PtoComa", None, 3, ["ParentesisApertura", "ParentesisCierre"])
            self.AnalizaDeclV()
        return True

    # <lista_id>
    def AnalizaListaId(self):
        self.emparejar("Identif", None, 2, ["Coma", "DosPtos"]) # Siguientes: , o :
        self.AnalizaRestoListaId()
        return True

    # <resto_listaid>
    def AnalizaRestoListaId(self):
        if self.token.cat == "Coma":
            self.Avanza()
            self.AnalizaListaId()
        return True

    # <Tipo_std>
    def AnalizaTipoStd(self):
        if self.token.cat == "PR" and self.token.valor in ["ENTERO", "REAL", "BOOLEANO"]:
            self.Avanza()
        else:
            self.Error(8) # Asumimos que el tipo estaba ahí para seguir
        return True

    # <instrucciones>
    def AnalizaInstrucciones(self):
        self.emparejar("PR", "INICIO", 10, ["Identif", "LEE", "ESCRIBE", "SI", "MIENTRAS", "FIN"])
        self.AnalizaBloqueInstrucciones()
        self.emparejar("PR", "FIN", 11, ["Punto", "SINO", "EOF"])
        return True

    # Bloque de instrucciones (Recursivo)
    def AnalizaBloqueInstrucciones(self):
        first_inst = ["Identif", "LEE", "ESCRIBE", "SI", "MIENTRAS"]
        followers = ["FIN", "SINO"] # Tokens que cierran bloque

        is_inst = (self.token.cat == "Identif") or (self.token.cat == "PR" and self.token.valor in first_inst)

        if is_inst:
            self.AnalizaInstruccion()
            # Si falta punto y coma, recuperamos si viene otra instrucción o FIN
            self.emparejar("PtoComa", None, 3, first_inst + followers)
            self.AnalizaBloqueInstrucciones()
        elif not (self.token.cat == "PR" and self.token.valor in followers):
            # No es instrucción ni FIN/SINO -> Basura
            self.Error(12)
            self.Avanza() 
            self.AnalizaBloqueInstrucciones() # Reintentar
        return True

    # <instrucción>
    def AnalizaInstruccion(self):
        if self.token.cat == "Identif":
            self.AnalizaInstSimple()
        elif self.token.cat == "PR":
            v = self.token.valor
            if v in ["LEE", "ESCRIBE"]:
                self.AnalizaInstES()
            elif v == "SI":
                self.Avanza()
                self.AnalizaExpresion()
                self.emparejar("PR", "ENTONCES", 14, ["INICIO"])
                self.AnalizaInstrucciones()
                if self.token.cat == "PR" and self.token.valor == "SINO":
                    self.Avanza()
                    self.AnalizaInstrucciones()
            elif v == "MIENTRAS":
                self.Avanza()
                self.AnalizaExpresion()
                self.emparejar("PR", "HACER", 15, ["INICIO"])
                self.AnalizaInstrucciones()
        # Si llegamos aquí sin coincidencia, el error se maneja en el caller (BloqueInstrucciones)
        return True

    # <Inst_simple>
    def AnalizaInstSimple(self):
        self.Avanza() # Id consumido
        self.emparejar("OpAsigna", None, 13, ["Identif", "Numero", "ParentesisApertura", "NO"]) # Sync con First(Expr)
        self.AnalizaExpresion()
        return True

    # <inst_e/s>
    def AnalizaInstES(self):
        tipo = self.token.valor 
        self.Avanza()
        self.emparejar("ParentesisApertura", None, 6, ["Identif", "Numero"])
        
        if tipo == "LEE":
            self.emparejar("Identif", None, 2, ["ParentesisCierre"])
        else:
            self.AnalizaExprSimple()

        self.emparejar("ParentesisCierre", None, 9, ["PtoComa"])
        return True

    # <expresión>
    def AnalizaExpresion(self):
        self.AnalizaExprSimple()
        self.AnalizaExpresionPrima()
        return True

    def AnalizaExpresionPrima(self):
        if self.token.cat == "OpRel":
            self.Avanza()
            self.AnalizaExprSimple()
        return True

    # <expr_simple>
    def AnalizaExprSimple(self):
        self.AnalizaTermino()
        self.AnalizaExprSimplePrima()
        return True

    def AnalizaExprSimplePrima(self):
        if self.token.cat == "OpAdd" or (self.token.cat == "PR" and self.token.valor == "O"):
            self.Avanza()
            self.AnalizaTermino()
            self.AnalizaExprSimplePrima()
        return True

    # <término>
    def AnalizaTermino(self):
        self.AnalizaFactor()
        self.AnalizaRestoTerm()
        return True

    def AnalizaRestoTerm(self):
        if self.token.cat == "OpMult" or (self.token.cat == "PR" and self.token.valor == "Y"):
            self.Avanza()
            self.AnalizaFactor()
            self.AnalizaRestoTerm()
        return True

    # <factor>
    def AnalizaFactor(self):
        validos = ["Identif", "Numero", "Entero", "Real"]
        
        if self.token.cat in validos:
            self.Avanza()
        elif self.token.cat == "PR" and self.token.valor in ["CIERTO", "FALSO"]:
            self.Avanza()
        elif self.token.cat == "ParentesisApertura":
            self.Avanza()
            self.AnalizaExpresion()
            self.emparejar("ParentesisCierre", None, 9, ["OpMult", "OpAdd", "PtoComa", "HACER", "ENTONCES"])
        elif self.token.cat == "PR" and self.token.valor == "NO":
            self.Avanza()
            self.AnalizaFactor()
        else:
            self.Error(17)
            # En factor, simplemente retornamos True asumiendo que el factor existía 
            # para no romper la evaluación de expresiones complejas.
        return True
    

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
    if S.AnalizaPrograma() and not len(S.lista_errores):
        print ("Analisis sintactico SATISFACTORIO. Fichero :", filename, "CORRECTO")
    else:
        print ("Analisis sintactico CON ERRORES. Fichero :", filename, "ERRONEO")
        print ("\nLista de errores: (Nºerror, línea, mensaje)\n", S.lista_errores)