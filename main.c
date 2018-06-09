#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "scanner.h"

int main (){
    FILE *Archivo = fopen("textoTP.txt","r");
    int cantCons = 0;
    int cantId =0;
    int cantErrores =0;
    int token;

    token = scanner(Archivo);
    while(token != FDT){
        switch(token) {
            case ID:
                printf("Identificador\n");
                cantIdentificadores++;
                break;
            case CONS:
                printf("Constante Entera\n");
                cantConstantes++;
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