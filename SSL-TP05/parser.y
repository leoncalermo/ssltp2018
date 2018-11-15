%code top{
#include <stdio.h>
#include "scanner.h"
#include "symbol.h"
#include "semantic.h"
}
%code provides{
void yyerror(const char *s);
extern int yyerrorLexico;
extern int yynerrs;
extern int yysemerrs;
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

programa :    PROGRAMA {printf("Load rtlib,\n");} listaDeSentencias {printf("Stop,\n");} FIN 

listaDeSentencias : VARIABLES declaraciones CODIGO sentencias  

declaraciones : declaraciones declaracion
              | declaracion        

declaracion   : DEFINIR IDENTIFICADOR '.' {if(!definirIdentificador($2)){YYERROR;};} 
              | error '.';


sentencias : 		sentencia
			| sentencias sentencia
			;

sentencia     : IDENTIFICADOR ASIGN expresion '.'         {asignar($1 , $3);} 
              | LEER '('identificadores')' '.'             
              | ESCRIBIR '('expresion')' '.'              {escribir($3);} 
              | error '.'
               
                       ;

expresion     : expresion  '+'  expresion                {$$=(generarInfijo($1, $3, "ADD"));}
              |expresion  '/'  expresion                 {$$=(generarInfijo($1, $3, "DIV"));}
              |expresion  '*'  expresion                 {$$=(generarInfijo($1, $3, "MULT"));}
              |expresion  '-'  expresion                 {$$=(generarInfijo($1, $3, "SUBS"));}
              | '(' expresion ')'                        {$$=($2);}
              |  '-'  expresion    %prec  NEG            {$$=(negar($2));}
              |IDENTIFICADOR
              |NUMERO
              ;

identificadores : identificadores ',' IDENTIFICADOR           {leer($3);}
                | IDENTIFICADOR                              {leer($1);} ;


%%
int yyerrorLexico=0;
int yysemerrs=0;

/* Informa la ocurrencia de un error. */
void yyerror(const char *s){
	printf("línea #%d: %s\n", yylineno, s);
	return;
}
