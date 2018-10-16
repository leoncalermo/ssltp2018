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




char  *tokenNames [] = {" ", "IDENTIFICADOR" , "CONSTANTE",  " ASIGNACION" };

int main(void){
   enum tokens t;
                    while( (t = yylex() ) ){
     if(t>0 && t<4){
                            printf("Token: %s\tLexema: %s\n", tokenNames[t],yytext);
          }  else{
                      printf("Token: %s\n",yytext);
                     if(t=='EOF'){printf("fin del archivo!!!!!!!!!!!!!!!!!!\n");return  0;} 
                  }
               printf("\n -------------------------------------------------------------- \n");
}

                     

return 0;
}