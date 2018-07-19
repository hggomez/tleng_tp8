import sys
from lexer import tokens

class val:
	def __init__(self,tab,list_str):
		self.tab = tab
		self.list_str = list_str


class dicc:
	def __init__(self, empty, list_str):
		self.list_str = list_str
		self.empty = empty
class pair:
	def __init__(self, cadenas, clave):
		self.list_str = [cadenas] #cadenas es un string
		self.clave = clave

class memb:
	def __init__(self,list_string, claves):
		self.list_str =  list_string
		self.claves = claves


class arr:
	def __init__(self, empty):
		self.empty = empty
		self.list_str = []

class elem:
	def __init__(self, elementos):
		self.list_str = elementos #elementos seria una lista de strings

#aux b|f|n|r|t|u
scaped_symbols = {"\\b", "\\t", "\\n", "\\f", "\\r", "true", "false"}
def no_scape_symbols(string):
	for symbol in scaped_symbols:
		if symbol in string:
			return False
	return True
#producciones

def p_incial(t):
	'inicial : val'
	res = "".join(t[1].list_str)
	t[0] = res


def p_val(t):
	'''val : STRING
	       | BOOL
	       | NULL
	       | NUM
	       | dicc
	       | arr'''
	if type(t[1]) is dicc or type(t[1]) is arr:
	     t[0] = val(not(t[1].empty),t[1].list_str)
	else:
		aux = t[1]
		if aux[0] == '"' and no_scape_symbols(aux):
			aux = aux[1:-1]
		elif aux == 'null':
			aux = ''
		aux  += '\n'
		t[0] = val(False, [aux])

def p_dicc(t):
	'''dicc : LLLAVE RLLAVE
		  | LLLAVE memb RLLAVE'''
	if type(t[2]) is memb:
		t[0] = dicc(False, t[2].list_str)
	else:
		t[0] = dicc(True, ['{}'])



def p_memb(t):
	'''memb : pair
			| pair COMA memb '''
	t[0] = memb(t[1].list_str, [t[1].clave])
	if len(t)> 2:
		t[0].list_str  += t[3].list_str
		t[0].claves += t[3].claves
		if len(t[0].claves) != len(set(t[0].claves)):
			#hay repetidos
			print("Claves repetidas." + "\n", file=sys.stderr)
			raise SyntaxError


def p_pair(t):
	'pair : STRING DOSPUNT val'
	aux = t[1]
	if no_scape_symbols(aux) and aux[1] != '-':
		aux = aux[1:-1]
	aux = aux + ":"
	if t[3].tab:
		aux = aux + "\n"
		t[0] = pair(aux, t[1])
		valores = ["  " +  val for val in t[3].list_str]
		t[0].list_str += valores
	else:
		aux += " " + t[3].list_str[0] #abusamos de que sabemos que es un valor
		t[0] = pair(aux, t[1])

def p_arr(t):
	''' arr : LCORCH RCORCH
			| LCORCH elem RCORCH '''
	if type(t[2]) is elem:
		t[0] = arr(False)
		t[0].list_str = t[2].list_str
	else:
		t[0] = arr(True)
		t[0].list_str = ['[]']
def p_elem(t):
		''' elem : val
				 | val COMA elem '''
		elementos = t[1].list_str
		if t[1].tab :
			elementos = ["  "+elem for elem in elementos]
			elementos = ["- \n"]+elementos
		else :
			elementos = ["- "+  elem for elem in elementos]

		t[0] = elem(elementos)
		if len(t) > 2:
			t[0].list_str += t[3].list_str


def p_error(t):
	print("Produccion invalida " + repr(t) + "\n", file=sys.stderr)
