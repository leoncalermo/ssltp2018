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

char * generarInfijo(char *operandoIzquierda, char *operandoDerecha, char *operando) {

	infijo = strdup(generarVariableInfijo());
			printf("%s %s, %s, %s\n",operando, operandoIzquierda, operandoDerecha, infijo);

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