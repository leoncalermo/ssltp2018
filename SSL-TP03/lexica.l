%{
#include  <stdio.h>
int id=0;
int palabraReservada=0;
int letra=0;
int numero=0;
int operadorAditivo=0;
int operadorMultiplicativo=0;
int asignacion=0;
int puntuacion=0;
%}
digdecimal [0-9]
caracter[a-zA-Z]


%%
{digdecimal} {digdecimal}*     {numero++;printf("reconocio el numero %s",yytext);}
{caracter} {caracter} {caracter}* {id++;printf("reconocio el id %s",yytext);}




.|\n                                                       ;
%%