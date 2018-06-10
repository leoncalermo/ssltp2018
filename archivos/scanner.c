#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include "scanner.h"

FILE *Archivo;

int tabla_de_estados[4][5]=
{{LEYENDO_CONS, LEYENDO_ID, LEYENDO_ERROR, ESTADO_INICIAL, FIN_DE_TEXTO},
{LEYENDO_CONS, LEIDO_CONS, LEIDO_CONS, LEIDO_CONS, LEIDO_CONS},
{LEYENDO_ID, LEYENDO_ID, LEIDO_ID, LEIDO_ID, LEIDO_ID},
{LEIDO_ERROR, LEIDO_ERROR, LEYENDO_ERROR, LEIDO_ERROR, LEIDO_ERROR}
};

bool esEstadoAceptor(int estadoActual)
{
   if (estadoActual == LEIDO_ERROR || estadoActual == LEIDO_ID || estadoActual == LEIDO_CONS || estadoActual == FIN_DE_TEXTO) {
      return true;
   }
   else {
      return false;
    }
}

int tipoDeToken(int estadoActual){
  int token;
  switch(estadoActual) {
    case LEIDO_ERROR:
        token = ERROR;
            break;

    case LEIDO_CONS:
        token = CONS;
            break;

    case LEIDO_ID:
        token = ID;
            break;

        case FIN_DE_TEXTO:
    token = FDT;
    break;
  }
  return token ;
}


int tipoCaracter(char caracter){
    if(islower(caracter)){
        return ES_CARACTER;
    }else if(isdigit(caracter)){
        return ES_CONS;
    }else if(isspace(caracter)){
        return ES_ESPACIO;
    }else if(caracter == EOF){
      return ES_FDT;
  } else {
        return ES_ERROR;
    }
}


int scanner(FILE *Archivo){
   int estadoActual = ESTADO_INICIAL;
    char caracter;
    while(!esEstadoAceptor (estadoActual)){

        caracter = getc(Archivo);
        int tipodecaracter = tipoCaracter(caracter);
        estadoActual = tabla_de_estados[estadoActual][tipodecaracter];
    }
    if(estadoActual!=FIN_DE_TEXTO){
       ungetc(caracter, Archivo);
    }

        return tipoDeToken(estadoActual);
}
