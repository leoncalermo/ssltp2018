#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>


extern typedef enum TOKEN;
extern int id;
extern int constEnteras;
extern int errores;

TOKEN scaner(void){

   int tabla  [6] [4] = {1,2,5,6,7},
                        {1,1,3,3,3},
                        {99,99,99,99,99},
                        {99,99,99,99,99},
                        {99,99,99,99,99},
                        {99,99,99,99,99},
                        {99,99,99,99,99};
   int columna=0;
   int estado = 0;
   char caracter;
   while(estado != '99'){
    caracter = getchar();
    switch(1){
       case isdigit(caracter): return columna=1;
       case isalpha(caracter): return columna=2;
       case caracter=='\0': return columna=3;
       case caracter=='\n':return columna=4;
       default: return columna=6;
    }
    estado = tabla [estado] [columna];
    if (estado==3) id++;
    if (estado==4) constEnteras++;
    if (estado==7) errores;
    ultimoEstado = estado;
   }
   if (ultimoEstado==3) return IDENTIFICADOR;
   if (ultimoEstado==4) return CONSTANTE; else return ERROR;
}
