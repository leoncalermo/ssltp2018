#include <stdio.h>
#include <string.h> 
#include "symbol.h" 
#include "parser.h"

char *tabla[400];
int siguiente = 0;
char errores[200];
int definirIdentificador(char* id){
	if(noExiste(id) && hayEspacio()){
		agregar(id);
	return 1; 
	}
return 0;
}

int noExiste(char* x) {
	if(buscarIdentificador(x)){
	sprintf(errores,"identificador %s ya declarado\n", x);
	yyerror(errores);
	yysemerrs++;	
	return 0;	
	}else{return 1;}	
}

void agregar(char* x) {
	printf("Declare %s,Integer\n", x);
	tabla[siguiente] = x;
	siguiente++;
}

int hayEspacio(){
	if(siguiente>=400){
	sprintf(errores,"hay espacio insuficiente");
	yyerror(errores);
	yysemerrs++;	
	return 0;
	}
return 1;
}
int buscarIdentificador(char* id){
	int i = 0;
	int existe = 0;
	while (i < siguiente && !existe) {
		if (strcmp(id, tabla[i])==0) {
			existe = 1;
		}
		
		i++;
	}	
	
	return existe;
}
int validarIdentificador(char* id){
	if(!buscarIdentificador(id)){
	sprintf(errores,"identificador %s no declarado\n", id);
	yyerror(errores);
	yysemerrs++;	
	return 0;
}
	return 1;
}