%top{
#include  <stdio.h>
#include  "tokens.h"
}
%{
int id=0;
int palabraReservada=0;
int numero=0;
int operadorAditivo=0;
int operadorMultiplicativo=0;
int asignacion=0;
int puntuacion=0;
%}
%option outfile="lexica.c"
%option nodefault
dignumero [0-9]
letra [[:alpha::]]
caracter [[:alnum:]]

%%
{dignumero}{dignumero}*     numero++;printf("reconocio el numero %s",yytext); return NUMERO;
{letra}{caracter}*          id++;printf("reconocio el id %s",yytext);return IDENTIFICADOR;
"+"                                                          {operadorAditivo++;printf("reconocio el operador Aditivo %s",yytext);return OPERADORAD;}
"-"                                                           {operadorAditivo++;printf("reconocio el operador Aditivo %s",yytext);return OPERADORAD;}
"*"                                                          {operadorMultiplicativo++;printf("reconocio el operador Multiplicativo %s",yytext);return OPERADORMULT;}
"/"                                                          {operadorMultiplicativo++;printf("reconocio el operadorMultiplicativo %s",yytext);return OPERADORMULT;}
"<-"                                                        {asignacion++;printf("reconocio el caracter de asignacion %s",yytext);return PUNT;}
"."                                                          {puntuacion++;printf("reconocio el caracter de puntuacion %s",yytext);return PUNT;}
"("                                                           {puntuacion++;printf("reconocio el caracter de puntuacion %s",yytext);return PUNT;}
")"                                                          {puntuacion++;printf("reconocio el caracter de puntuacion %s",yytext);return PUNT;}
","                                                          {puntuacion++;printf("reconocio el caracter de puntuacion %s",yytext);return PUNT;}
"//"                                                        {puntuacion++;printf("reconocio el caracter de puntuacion %s",yytext);return PUNT;}
"programa"                                      {palabraReservada++;printf("reconocio la palabraReservada%s",yytext);return PALABRARESERVADA;}
"variables"                                        {palabraReservada++;printf("reconocio la palabraReservada%s",yytext);return PALABRARESERVADA;}
"definir"                                           {palabraReservada++;printf("reconocio la palabraReservada%s",yytext);return PALABRARESERVADA;}
"leer"                                                 {palabraReservada++;printf("reconocio la palabraReservada%s",yytext);return PALABRARESERVADA;}
"escribir"                                         {palabraReservada++;printf("reconocio la palabraReservada%s",yytext);return PALABRARESERVADA;}
"codigo"                                          {palabraReservada++;printf("reconocio la palabraReservada%s",yytext);return PALABRARESERVADA;}
"fin"                                                   {palabraReservada++;printf("reconocio la palabraReservada%s",yytext);return PALABRARESERVADA;}

.|\n                                                       ;
%%

int main(){

yylex();

return 0;
}