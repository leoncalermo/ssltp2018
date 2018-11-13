%code top{
#include <stdio.h>
#include "scanner.h"
}
%code provides{
void yyerror(const char *s);
extern int yyerrorLexico;
extern int yynerrs;
}
%defines "parser.h"
%output "parser.c"
%define api.value.type {char *}
%define parse.error verbose
%left  '-'  '+'
%left  '*'  '/'
%precedence NEG
%token IDENTIFICADOR NUMERO VARIABLES PROGRAMA DEFINIR LEER ESCRIBIR CODIGO FIN ASIGN


%%
todo  :  programa { if (yynerrs || yyerrorLexico) YYABORT; else YYACCEPT; } ;

programa :    PROGRAMA listaDeSentencias FIN 

listaDeSentencias : VARIABLES declaraciones CODIGO sentencias  

declaraciones : declaraciones declaracion
              | declaracion        

declaracion   : DEFINIR IDENTIFICADOR '.' {printf("definir %s \n", $2);} 
              | error '.';


sentencias : 		sentencia
			| sentencias sentencia
			;

sentencia     : IDENTIFICADOR ASIGN expresion '.'         {printf("asignacion \n");} 
              | LEER '('identificadores')' '.'          {printf("leer \n");} 
              | ESCRIBIR '('expresion')' '.'          {printf("escribir \n");}
              | error '.'
               
                       ;

expresion     : expresion  '+'  expresion                {printf("suma\n");}
              |expresion  '/'  expresion                 {printf("division\n");}
              |expresion  '*'  expresion                 {printf("multiplicacion\n");}
              |expresion  '-'  expresion                 {printf("resta\n");}
              | '(' expresion ')'                        {printf("parentesis\n");}
              |  '-'  expresion    %prec  NEG            {printf("inversion\n");}
              |IDENTIFICADOR
              |NUMERO
              ;

identificadores : identificadores ',' IDENTIFICADOR 
                | IDENTIFICADOR ;


%%
int yyerrorLexico=0;
/* Informa la ocurrencia de un error. */
void yyerror(const char *s){
	printf("línea #%d: %s\n", yylineno, s);
	return;
}