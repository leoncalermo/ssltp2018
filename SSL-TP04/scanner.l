%top{
#include  <stdio.h>
#include "parser.h"
}
%{
	char buffer[100];

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
{dignumero}({dignumero}|{letra})+      {yyerrorLexico++;sprintf( buffer, "Error Lexico: constante invalida %s", yytext); yyerror(buffer);}
{letra}({caracter}|{error})+      {yyerrorLexico++;sprintf( buffer, "Error Lexico: identificador invalido %s", yytext); yyerror(buffer);}
{espacio}+	;
{error}+ | 
.                                 {yyerrorLexico++; sprintf( buffer, "Error Lexico: cadena desconocida %s", yytext); yyerror(buffer);}
%%
