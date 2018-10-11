%top{
#include  <stdio.h>
#include  "tokens.h"

}
%{


%}
%option outfile="scanner.c"
%option header-file="scanner.h"
%option nodefault
dignumero [0-9]
letra [a-zA-Z]
caracter  [[:alnum:]]
espacio [[:space:]]
otro [[:^alnum:]]{-}[[:space :]]
todos [a-zA-Z0-9!@#$%^&_?<>]
invalidos[!@#$%^&_?<>]

%%
{dignumero}{dignumero}*     { return NUMERO;}
"variables"                                         {return PALABRARESERVADA;}
"programa"                                      {return PALABRARESERVADA;}
"definir"                                              {return PALABRARESERVADA;}
"leer"                                                     {return PALABRARESERVADA;}
"escribir"                                             {return PALABRARESERVADA;}
"codigo"                                               {return PALABRARESERVADA;}
"fin"                                                        {return PALABRARESERVADA;}
{letra}                                                    {return LETRA;}
{letra}{caracter}*                          {return IDENTIFICADOR;}
"+"                                                          {return '+';}
"-"                                                           {return '-';}
"*"                                                          {return '*';}
"/"                                                          {return '/';}
"<-"                                                        {return ASIGN;}
"."                                                          {return PUNT;}
"("                                                          {return PUNT;}
")"                                                          {return PUNT;}
","                                                          {return PUNT;}
"//"{letra}{caracter}*
{dignumero}{dignumero}*{todos}+      {printf("Error léxico: constante invalida: %s \n",yytext);return ERROR;}
{letra}{letra}*{invalidos}{todos}+      {printf("Error léxico: cadena desconocida: %s \n",yytext);return ERROR;}
{otro}+                                                  {printf("Error léxico: cadena desconocida: %s \n",yytext);}
{espacio}+


.|\n                                                       ;
%%


