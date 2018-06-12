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
   if(Archivo=fopen("textoTP.txt","w"))
    {printf("ingrese el valor: ");
    while((caracter = getchar()) != '\n')
 	{
 		printf("%c", fputc(caracter, Archivo));
 	}
 	printf("\n");
 	fclose(Archivo);
    }
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

