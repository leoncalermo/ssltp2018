// TP004 - 2018
//
// Bison
//
// Grupo 07
//
// Pollola, Mariano - 160.555-0
// Calermo, Leon - 153.566-3
// Diaz Argentino, Sebastian - 159.504-0
// Grimberg, Axel - 159.378-0
#include <stdio.h>
#include "parser.h"


int main() {
int x=yyparse() ;
	switch( x ){
	case 0:
		puts("Compilacion terminada con exito"); 
		break;
	case 1:
		puts("Errores de compilacion"); 
		break;
	case 2:
		puts("Memoria insuficiente"); 
		break;
	}
	printf("Errores Lexicos: %d \n", yyerrorLexico);
	printf("Errores Sintacticos: %d \n", yynerrs);

	return x;
	
}