#include <stdio.h>
#include "semantic.h"
#include "symbol.h"
#include <string.h>
int temporal = 0;
char nombreDelTemporal[100];
char * infijo;

char * generarVariableInfijo() {
	temporal++;
	sprintf(nombreDelTemporal, "Temp#%d", temporal);
	definirIdentificador(strdup(nombreDelTemporal));	
	return nombreDelTemporal;
}

char * generarInfijo(char *operandoIzquierda, char *operandoDerecha,char operando) {

	infijo = strdup(generarVariableInfijo());
         switch(operando){
               case '+': printf("ADD %s, %s, %s\n", operandoIzquierda, operandoDerecha, infijo);
                         break;
	       case '-': printf("SUBS %s, %s, %s\n", operandoIzquierda, operandoDerecha, infijo);
                         break;
               case '*': printf("MULT %s, %s, %s\n", operandoIzquierda, operandoDerecha, infijo);
                         break;
               case '/': printf("DIV %s, %s, %s\n", operandoIzquierda, operandoDerecha, infijo);
                         break;
                default: puts("ERROR");
      }
	return infijo;
}

char * negar(char * x) {
	infijo = strdup(generarVariableInfijo());
	printf("INV %s,,%s\n", x, infijo);

	return infijo;
}


void leer(char * x) {
	printf("Read %s, Integer\n", x);
}



void asignar(char * var1, char * var2){
	printf("Store %s,%s\n", var2, var1);
}

void escribir(char * x) {
	printf("Write %s, Integer\n", x);
}