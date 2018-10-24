%top{
#include  <stdio.h>
#include "parser.h"
}
%{


%}
%option outfile="scanner.c"
%option header-file="scanner.h"
%option  noinput    
%option  nounput
%option yylineno
dignumero [0-9]
letra [a-zA-Z]
caracter  [[:alnum:]]
espacio [[:space:]]
error [^a-zA-Z0-9/),(.+*<[:space:]-]

%%
{dignumero}{dignumero}*     {yylval = strdup(yytext);return NUMERO;}
"variables"                                         {return VARIABLES;}
"programa"                                      {return PROGRAMA;}
"definir"                                              {return DEFINIR;}
"leer"                                                     {return LEER;}
"escribir"                                             {return ESCRIBIR;}
"codigo"                                               {return CODIGO;}
"fin"                                                        {return FIN;}
{letra}{caracter}*                          {yylval = strdup(yytext);return IDENTIFICADOR;}
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
{dignumero}({dignumero}|{letra})+      {yyerrorLexico++;yyerror("Error léxico: constante invalida\n");}
{letra}({caracter}|{error})+      {yyerrorLexico++;yyerror("Error léxico:  identificador invalido \n");}
{espacio}+	;
{error}+ | 
.                                                 {yyerrorLexico++;yyerror("Error léxico: cadena desconocida: %s \n");}
%%


