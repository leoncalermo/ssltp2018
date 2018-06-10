#ifndef SCANNER_H_INCLUDED
#define SCANNER_H_INCLUDED
#include <stdbool.h>


bool esEstadoAceptor(int estadoActual);
int tipoCaracter(char caracter);
int scanner(FILE *Archivo);
enum {ESTADO_INICIAL, LEYENDO_CONS,  LEYENDO_ID, LEYENDO_ERROR, LEIDO_CONS, LEIDO_ID, LEIDO_ERROR, FIN_DE_TEXTO};
enum {ES_CONS, ES_CARACTER, ES_ERROR, ES_ESPACIO, ES_FDT};
enum{ID, CONS, ERROR, FDT};


#endif // SCANNER_H_INCLUDED
