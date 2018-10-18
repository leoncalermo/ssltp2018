%top{
#include  <stdio.h>
#include  "tokens.h"

}
%{


%}
%option outfile="scanner.c"
%option header-file="scanner.h"
%option  noinput    
%option  nounput
dignumero [0-9]
letra [a-zA-Z]
caracter  [[:alnum:]]
espacio [[:space:]]
error [^a-zA-Z0-9/),(.+*<[:space:]-]

%%
{dignumero}{dignumero}*     {return NUMERO;}
"variables"                                         {return VARIABLES;}
"programa"                                      {return PROGRAMA;}
"definir"                                              {return DEFINIR;}
"leer"                                                     {return LEER;}
"escribir"                                             {return ESCRIBIR;}
"codigo"                                               {return CODIGO;}
"fin"                                                        {return FIN;}
{letra}{caracter}*                          {return IDENTIFICADOR;}
"+"                                                          {return '+';}
"-"                                                           {return '-';}
"*"                                                          {return '*';}
"/"                                                          {return '/';}
"<-"                                                        {return ASIGN;}
"."                                                          {return '.';}
"("                                                          {return '(';}
")"                                                          {return ')';}
","                                                          {return ',';}
"//".*	;
{dignumero}({dignumero}|{letra})+      {printf("Error léxico: constante invalida: %s \n",yytext);}
{letra}({caracter}|{error})+      {printf("Error léxico:  identificador invalido: %s \n",yytext);}
{espacio}+	;
{error}+ | 
.                                                 {printf("Error léxico: cadena desconocida: %s \n",yytext);}
%%


