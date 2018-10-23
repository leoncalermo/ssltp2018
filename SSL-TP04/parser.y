%code top{
#include <stdio.h>
#include "scanner.h"
}
%code provides{
void yyerror(const char *s);
extern int errorLexico;
}
%defines "parser.h"
%output "parser.c"
%define api.value.type {char *}
%left  '-'  '+'
%left  '*'  '/'
%precedence NEG
%token FINDEARCHIVO IDENTIFICADOR NUMERO VARIABLES PROGRAMA DEFINIR LEER ESCRIBIR CODIGO FIN ASIGN


%%
todo  :  PROGRAMA listaDeSentencias FIN  ;

listaDeSentencias : VARIABLES declaraciones CODIGO sentencias  

declaraciones : declaraciones declaracion
              | declaracion        

declaracion   : DEFINIR IDENTIFICADOR '.' {printf("definir %s \n", $2);} ;


sentencias : 		sentencia
			| sentencias sentencia
			;

sentencia     : IDENTIFICADOR ASIGN expresion '.'         {printf("asignacion \n");} 
              | LEER '('identificadores')' '.'          {printf("leer \n");} 
              | ESCRIBIR '('expresion')' '.'          {printf("escribir \n");}
               
                       ;

expresion     : expresion  '+'  expresion                {printf("suma\n");}
              |expresion  '/'  expresion                 {printf("division\n");}
              |expresion  '*'  expresion                 {printf("multiplicacion\n");}
              |expresion  '-'  expresion                 {printf("resta\n");}
              | '(' expresion ')'                        {printf("parentesis\n");}
              |  '-'  expresion    %prec  NEG            {printf("inversion\n");}
              |IDENTIFICADOR
              |NUMERO

identificadores : identificadores ',' IDENTIFICADOR 
                | IDENTIFICADOR ;


%%
int errorLexico=0;

/* Informa la ocurrencia de un error. */
void yyerror(const char *s){
	printf("línea #%d: %s\n", yylineno, s);
	return;
}
