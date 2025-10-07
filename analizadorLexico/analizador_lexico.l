
%%
[ ] {printf("Esto es un espacio");}
fin {printf("Final");}
[a-zA-Z][a-zA-Z0-9]* {printf("Esto es un identificador");}
-?(0|[1-9][0-9]*) {printf("Esto es un numero entero");}
-?(0|[1-9][0-9]*)\.[0-9]*[1-9] {printf("Esto es un numero real");}
[-+*/] {printf("Esto es un operador");}
%%

int main()
{
    yylex();
    exit(0);
}
