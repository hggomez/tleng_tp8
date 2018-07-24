
import ply.lex as lex

tokens = (
	'STRING','NUM','BOOL','NULL','LLLAVE','RLLAVE','LCORCH','RCORCH','COMA','DOSPUNT'
	)

#TOKENS

t_NULL = r'null'
t_LLLAVE = r'\{'
t_RLLAVE = r'\}'
t_LCORCH = r'\['
t_RCORCH = r'\]'
t_COMA = r','
t_DOSPUNT = r':'
#t_STRING = r'/^("(((?=\\)\\(["\\\/bfnrt]|u[0-9a-fA-F]{4}))|[^"\\\0-\x1F\x7F]+)*")$/'
t_STRING = r'\"((?=\\)\\(\"|\/|\\|b|f|n|r|t|u[0-9a-zA-Z]{4})|[^\\"]*)*\"'
t_BOOL =r'true|false' 
t_ignore = ' \n\t'


def t_NUM(t):
	r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?'	
	return t

def t_error(t):
	print("caracter invalido " + repr(t)+"\n")
	t.lexer.skip(len(t.value))