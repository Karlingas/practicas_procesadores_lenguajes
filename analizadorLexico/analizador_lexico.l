
%{
    int caracteres = 0, palabras = 0, lineas = 0;
%}
letra         [a-zA-Z]
digito        [0-9]
digitoNoCero  [1-9]
letraDigito   [a-zA-Z0-9]
operador      [-+*/]
espacio       [ ]
salto         [\n]

%%
{salto}                                     {lineas++;}
{espacio}                                   { }
fin                                         { return 0; }
{letra}{letraDigito}*                       { printf("Identificador %s\n", yytext); caracteres= caracteres + yyleng; palabras++;}
-?(0|{digitoNoCero}{digito}*)               { printf("Entero %s\n", yytext);  caracteres= caracteres + yyleng; palabras++;}
-?(0|{digitoNoCero}{digito}*)\.{digito}+    { printf("Real %s\n", yytext); caracteres= caracteres + yyleng; palabras++; }
{operador}                                  { printf("Operador %s\n", yytext); caracteres++;}
.                                           { printf("Caracter no esperado: %s\n", yytext); }

%%

int main()
{
    yylex();
    printf("Lineas: %d, Palabras: %d, Caracteres: %d\n", lineas, palabras, caracteres);
    exit(0);
}
