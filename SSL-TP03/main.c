// TP003 - 2018
//
// Flex
//
// Grupo 07
//
// Pollola, Mariano - 160.555-0
// Calermo, Leon - 153.566-3
// Diaz Argentino, Sebastian - 159.504-0
// Grimberg, Axel - 159.378-0

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tokens.h"
#include "scanner.h"




char  *tokenNames [] = {" ", "IDENTIFICADOR" , "PALABRARESERVADA" , "NUMERO", "OPERADORAD", "OPERADORMULT", " ASIGN",  "PUNT"  };

int main(void){
   enum tokens t;
printf("\n ------------------------------------------------------------------------------------------------------------ \n");
                    while( (t = yylex() ) ){
      printf("Token: %s\tValor: %s\n", tokenNames[t],yytext);
}

                     

return 0;
}