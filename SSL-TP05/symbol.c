#include "parser.h"
#include "symbol.h"

#include <string.h>
#include <stdio.h>
//#include <stdbool.h>

char buffer[200];
int posicion = 0;
char* diccionario[100];

void agregar(char* id){
	if (posicion<100){
	  diccionario[posicion]=strdup(id);
	  posicion++;
	}
	else {
	  printf("No hay espacio en el diccionario");
	}
}

int declarado(char* id) {
  int indice=0;
  int encontrado=0;
  while(indice < posicion && !encontrado){
  	if (!strcmp(diccionario[indice],id)) {
	  encontrado = 1;
 	} else {
	  indice++;
	}
  }
}

int agregarID(char* id) {
	if(declarado(id)){
		printf("Error semantico: identificador %s ya esta declarado",id);
		nerrsem++;
		return 0;
	} else {
		agregar(id);
		printf("Declare %s,Integer\n",id);
		return 1;
	}
  
}

int comprobarID(char *id) {
	if(!declarado(id)){
	  printf("Error semántico: identificador %s no esta declarado",id);
	  nerrsem++;
	  return 0;
	}

}