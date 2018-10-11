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




char  *tokenNames [] = {" ", "IDENTIFICADOR" , "PALABRARESERVADA" , "NUMERO",  " ASIGN",  "PUNT"  };

int main(void){
   enum tokens t;
                    while( (t = yylex() ) ){
      printf("\n -------------------------------------------------------------- \n");
     if(t=='+' || t=='-'){
                   printf("Token: Operador aditivo\tValor: %s\n", yytext);  
                                                  }
else{
      if(t=='*' || t=='/'){
                   printf("Token: Operador multiplicativo\tValor: %s\n", yytext);  
                                                    }
    else{ if(t==ERROR){
    	//nada}
    }
    else{   
    	printf("Token: %s\tValor: %s\n", tokenNames[t],yytext);
    }
                                               }
                                  }
}

                     

return 0;
}