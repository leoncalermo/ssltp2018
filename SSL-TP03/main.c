#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tokens.h"
#include "scanner.c"


char  *tokenNames [] = {" ", "IDENTIFICADOR" , "PALABRARESERVADA" , "NUMERO", "OPERADORAD", "OPERADORMULT", " ASIGN",  "PUNT"  };

int main(void){
   enum tokens t;
    
                    while( (t = yylex() ) ){     
                               printf("papu \n");
}

                     

return 0;
}