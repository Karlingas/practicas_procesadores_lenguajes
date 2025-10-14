letra         [a-zA-Z]
digito        [0-9]
digitoNoCero  [1-9]
letraDigito   [a-zA-Z0-9]
operador      [-+*/]
espacio       [ ]

%%
{espacio}                                   { }
fin                                         { return 0; }
{letra}{letraDigito}*                       { printf("identificador %s\n", yytext); }
-?(0|{digitoNoCero}{digito}*)               { printf("Entero %s\n", yytext); }
-?(0|{digitoNoCero}{digito}*)\.{digito}+    { printf("Real %s\n", yytext); }
{operador}                                  { printf("Operador %s\n", yytext); }
.                                           { printf("Caracter no esperado: %s\n", yytext); }

%%

int main()
{
    yylex();
    exit(0);
}
