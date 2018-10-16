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
otro [[:^alnum:]]{-}[[:space :]]
todos [a-zA-Z0-9!@#$%^&_?<>]
diferencia[!@#$%^&_?<>]

%%
{dignumero}{dignumero}*     {return NUMERO;}
"variables"                                         {return 'variables';}
"programa"                                      {return 'programa';}
"definir"                                              {return 'definir';}
"leer"                                                     {return 'leer';}
"escribir"                                             {return 'escribir';}
"codigo"                                               {return 'codigo';}
"fin"                                                        {return 'fin';}
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
"//"{todos}*
{dignumero}{dignumero}*{todos}+      {printf("Error léxico: constante invalida: %s \n",yytext);}
{letra}{letra}*{diferencia}{todos}+      {printf("Error léxico:  identificador invalido: %s \n",yytext);}
{diferencia}+                                                  {printf("Error léxico: cadena desconocida: %s \n",yytext);}
{espacio}+
<<EOF>>                                        {return 'EOF';}

.|\n                                                       ;
%%


