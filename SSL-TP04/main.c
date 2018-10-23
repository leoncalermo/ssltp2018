// TP003 - 2018
//
// Flex
//
// Grupo 07
//
// Pollola, Mariano - 160.555-0
// Calermo, Leon - 153.566-3
// Diaz Argentino, Sebastian - 159.504-0
// Grimberg, Axel - 159.378-0
#include <stdio.h>
#include "scanner.h"
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
	

	return x;
	
}