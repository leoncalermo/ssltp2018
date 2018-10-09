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
int letra=0;
int error=0;
%}
%option outfile="scanner.c"
%option nodefault
dignumero [0-9]
letra [a-zA-Z]
caracter  [[:alnum:]]
espacio [[:space:]]
otro [[:^alnum:]]{-}[[:space :]]
todos [a-zA-Z0-9!@#$%^&_?<>]
invalidos[!@#$%^&_?<>]

%%
{dignumero}{dignumero}*     {numero++;printf("Token: Constante    lexema: %s \n",yytext); return NUMERO;}
"variables"                                         {palabraReservada++;printf("Token: %s \n",yytext);return PALABRARESERVADA;}
"programa"                                      {palabraReservada++;printf("Token: %s \n",yytext);return PALABRARESERVADA;}
"definir"                                              {palabraReservada++;printf("Token: %s \n",yytext);return PALABRARESERVADA;}
"leer"                                                     {palabraReservada++;printf("Token: %s \n",yytext);return PALABRARESERVADA;}
"escribir"                                             {palabraReservada++;printf("Token: %s \n",yytext);return PALABRARESERVADA;}
"codigo"                                               {palabraReservada++;printf("Token: %s \n",yytext);return PALABRARESERVADA;}
"fin"                                                        {palabraReservada++;printf("Token: %s \n",yytext);return PALABRARESERVADA;}
{letra}                                            {letra++;printf("Token: Letra   lexema: %s \n",yytext);return LETRA;}
{letra}{caracter}*                          {id++;printf("Token: Identificador   lexema: %s \n",yytext);return IDENTIFICADOR;}
"+"                                                          {operadorAditivo++;printf("Token: %s \n",yytext);return OPERADORAD;}
"-"                                                           {operadorAditivo++;printf("Token: %s \n",yytext);return OPERADORAD;}
"*"                                                          {operadorMultiplicativo++;printf("Token: %s \n",yytext);return OPERADORMULT;}
"/"                                                          {operadorMultiplicativo++;printf("Token: %s \n",yytext);return OPERADORMULT;}
"<-"                                                        {asignacion++;printf("Token: Asignación \n");return PUNT;}
"."                                                          {puntuacion++;printf("Token: %s \n",yytext);return PUNT;}
"("                                                          {puntuacion++;printf("Token: %s \n",yytext);return PUNT;}
")"                                                          {puntuacion++;printf("Token: %s \n",yytext);return PUNT;}
","                                                          {puntuacion++;printf("Token: %s \n",yytext);return PUNT;}
"//"{letra}{caracter}*
{dignumero}{dignumero}*{todos}+      {error++;printf("Error léxico: constante invalida: %s \n",yytext);return ERROR;}
{letra}{letra}*{invalidos}{todos}+      {error++;printf("Error léxico: cadena desconocida: %s \n",yytext);return ERROR;}
{otro}+                                                  {error++;printf("Error léxico: cadena desconocida: %s \n",yytext);}
{espacio}+


.|\n                                                       ;
%%


