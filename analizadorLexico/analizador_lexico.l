
%%
[ ] {}
fin {return 0;}
[a-zA-Z][a-zA-Z0-9]* {printf("identificador %s\n",yytext);}
-?(0|[1-9][0-9]*) {printf("Entero %s\n",yytext);}
-?(0|[1-9][0-9]*)\.[0-9]+ {printf("Real %s\n",yytext);}
[-+*/] {printf("Operador %s\n", yytext);}
. {printf("Caracter no esperado");}
%%

int main()
{
    yylex();
    exit(0);
}
