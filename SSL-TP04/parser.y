%code top{
#include <stdio.h>
#include "tokens.h"
}
%code provides {
void yyerror(const char *s);
extern int nerrlex;
}
%defines "parser.h"
%output "parser.c"
%option  noinput    
%option  nounput
%union {
	int    num;
	char   *str;
}
%tokens <int> NUMERO
%tokens <str> IDENTIFICADOR VARIABLES PROGRAMA DEFINIR LEER ESCRIBIR CODIGO FIN