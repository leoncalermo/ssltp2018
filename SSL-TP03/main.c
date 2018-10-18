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




char  *tokenNames [] = {"FINDEARCHIVO","IDENTIFICADOR"," NUMERO","VARIABLES","PROGRAMA","DEFINIR","LEER","ESCRIBIR","CODIGO","FIN","ASIGN"};

int main(void){
   enum tokens t;
                    while( (t = yylex() ) ){
     if(t == '+'|| t == '-'|| t == '*'|| t == '/'|| t == '.'|| t == ','|| t == '(' || t == ')'){
       printf("Token: %s\n",yytext);
     }  else{
       printf("Token: %s\tLexema: %s\n", tokenNames[t],yytext);                     
     }
   printf("\n -------------------------------------------------------------- \n");
}
printf("Token: %s\n",tokenNames[t]);

                     

return 0;
}