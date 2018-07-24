import sys
import lexer
import parser

# -- with ply installed --
from ply.lex import lex
from ply.yacc import yacc
# -- with lex and yacc files on project --
#import lex
#import yacc

# -- with ply installed --
lexer = lex(module=lexer)
parser = yacc(module=parser)
# -- with lex and yacc files on project --
#lexer = lex.lex(module=lexer_rules)
#parser = yacc.yacc(module=parser_rules)

entrada = sys.stdin.read()

resultado = parser.parse(entrada, lexer)
print(resultado)
