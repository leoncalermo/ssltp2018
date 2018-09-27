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
letra [[:alpha:]]
caracter  [[:alnum:]]
espacio [[:space:]]
constanteInvalida [[:^digit:]]
otro [[:^alnum:]]{-}[[:space :]]
invalidos [a-zA-Z0-9!@#$%^&_.,?]

%%
{dignumero}{dignumero}*     {numero++;printf("reconocio el numero %s \n",yytext); return NUMERO;}
"variables"                                         {palabraReservada++;printf("reconocio la palabraReservada %s \n",yytext);return PALABRARESERVADA;}
"programa"                                      {palabraReservada++;printf("reconocio la palabraReservada %s \n",yytext);return PALABRARESERVADA;}
"definir"                                              {palabraReservada++;printf("reconocio la palabraReservada %s \n",yytext);return PALABRARESERVADA;}
"leer"                                                     {palabraReservada++;printf("reconocio la palabraReservada %s \n",yytext);return PALABRARESERVADA;}
"escribir"                                             {palabraReservada++;printf("reconocio la palabraReservada %s \n",yytext);return PALABRARESERVADA;}
"codigo"                                               {palabraReservada++;printf("reconocio la palabraReservada %s \n",yytext);return PALABRARESERVADA;}
"fin"                                                        {palabraReservada++;printf("reconocio la palabraReservada %s \n",yytext);return PALABRARESERVADA;}
{letra}                                            {letra++;printf("reconocio la letra %s \n",yytext);return LETRA;}
{letra}{caracter}*                          {id++;printf("reconocio el id %s \n",yytext);return IDENTIFICADOR;}
"+"                                                          {operadorAditivo++;printf("reconocio el operador Aditivo %s \n",yytext);return OPERADORAD;}
"-"                                                           {operadorAditivo++;printf("reconocio el operador Aditivo %s \n",yytext);return OPERADORAD;}
"*"                                                          {operadorMultiplicativo++;printf("reconocio el operador Multiplicativo %s \n",yytext);return OPERADORMULT;}
"/"                                                          {operadorMultiplicativo++;printf("reconocio el operadorMultiplicativo %s \n",yytext);return OPERADORMULT;}
"<-"                                                        {asignacion++;printf("reconocio el caracter de asignacion %s \n",yytext);return PUNT;}
"."                                                          {puntuacion++;printf("reconocio el caracter de puntuacion %s \n",yytext);return PUNT;}
"("                                                           {puntuacion++;printf("reconocio el caracter de puntuacion %s \n",yytext);return PUNT;}
")"                                                          {puntuacion++;printf("reconocio el caracter de puntuacion %s \n",yytext);return PUNT;}
","                                                          {puntuacion++;printf("reconocio el caracter de puntuacion %s \n",yytext);return PUNT;}
"//"                                                        {puntuacion++;printf("reconocio el caracter de puntuacion %s \n",yytext);return PUNT;}
{dignumero}{invalidos}*      {error++;printf("reconocio constante invalida %s \n",yytext);return ERROR;}
{otro}+                                                  {error++;printf("reconocio error lexico %s \n",yytext);}
{espacio}+


.|\n                                                       ;
%%


char  *tokenNames [] = {" ", "IDENTIFICADOR" , "PALABRARESERVADA" , "NUMERO", "OPERADORAD", "OPERADORMULT", " ASIGN",  "PUNT","ERROR" };

int main(void){
   enum tokens t;
    
                    while( (t = yylex() ) ){     
                               printf("papu \n");
}

                     

return 0;
}
