// TP00 - 2018
//
// Un escaner elemental
//
// Grupo 07
//
// Calermo, Leon - 153.566-3
// Diaz Argentino, Sebastian - 159.504-0
// Grimberg, Axel - 159.378-0
// Pollola, Mariano - 160.555-0

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "scanner.h"



int main (){
    int cantCons = 0;
    int cantId =0;
    int cantErrores =0;
    int token;
    char caracter;
    FILE *Archivo;

    Archivo=fopen("textoTP.txt","r");
    token = scanner(Archivo);
    while(token != FDT){
        switch(token) {
            case ID:
                printf("Identificador\n");
                cantId++;
                break;
            case CONS:
                printf("Constante Entera\n");
                cantCons++;
                break;
            case ERROR:
                printf("Error\n");
                cantErrores++;
                break;
            default:
                break;
        }
        token = scanner(Archivo);
    }

    printf("\nTotales: \nIdentificadores: %d \nConstantes Enteras: %d \nErrores: %d\n", cantId, cantCons, cantErrores);
    fclose(Archivo);
    return 0;
}
