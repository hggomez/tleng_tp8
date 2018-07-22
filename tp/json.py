import ply
import ply.lex
import ply.yacc
import sys

JSON_TOKENS = [
  # Initial state tokens
  'BEGIN_ARRAY',
  'BEGIN_OBJECT',
  'END_ARRAY',
  'END_OBJECT',
  'NAME_SEPARATOR',
  'VALUE_SEPARATOR',
  'QUOTATION_MARK',
  'FALSE',
  'TRUE',
  'NULL',
  'DECIMAL_POINT',
  'DIGITS',
  'E',
  'MINUS',
  'PLUS',
  'ZERO',
  'UNESCAPED',
  'ESCAPE',
  # Escaped state tokens
  'REVERSE_SOLIDUS',
  'SOLIDUS',
  'BACKSPACE_CHAR',
  'FORM_FEED_CHAR',
  'LINE_FEED_CHAR',
  'CARRIAGE_RETURN_CHAR',
  'TAB_CHAR',
  'UNICODE_HEX'
]


class JsonLexer(object):
  def __init__(self, **kwargs):
    self.lexer = ply.lex.lex(module=self, **kwargs)
  tokens = JSON_TOKENS
  states = (
    ('string', 'exclusive'),
    ('escaped', 'exclusive')
  )

  def t_ANY_error(self, t): 
    last_cr = self.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_cr < 0:
      last_cr = 0
    column = (t.lexpos - last_cr) + 1
    print("Illegal character '%s' at line %d pos %d" % (
      t.value[0], t.lineno, column))
    t.lexer.skip(1) 

  t_ignore = '\x20\x09\x0A\x0D'

  # Default state tokens
  t_BEGIN_ARRAY          = r'\x5B'                  # '['
  t_BEGIN_OBJECT         = r'\x7B'                  # '{'
  t_END_ARRAY            = r'\x5D'                  # ']'
  t_END_OBJECT           = r'\x7D'                  # '}'
  t_NAME_SEPARATOR       = r'\x3A'                  # ':'
  t_VALUE_SEPARATOR      = r'\x2C'                  # ','
  t_FALSE                = r'\x66\x61\x6c\x73\x65'  # 'false'
  t_TRUE                 = r'\x74\x72\x75\x65'      # 'true'
  t_NULL                 = r'\x6e\x75\x6c\x6c'      # 'null'
  t_DECIMAL_POINT        = r'\x2E'                  # '.'
  t_DIGITS               = r'[\x30-\x39]+'          # '0'..'9'
  t_E                    = r'[\x45\x65]'            # 'e' or 'E'
  t_MINUS                = r'\x2D'                  # '-'
  t_PLUS                 = r'\x2B'                  # '+'
  t_ZERO                 = r'\x30'                  # '0'

  def t_QUOTATION_MARK(self, t):
    r'\x22'   # '"'
    t.lexer.push_state('string') 
    return t

  t_string_ignore = ''

  def t_string_UNESCAPED(self, t):
    r'[\x20-\x21,\x23-\x5B,\x5D-\xFF]+'
    t.value = str(t.value)
    return t

  # Exits the string state on an unescaped closing quotation mark
  def t_string_QUOTATION_MARK(self, t):
    r'\x22'  # '"'
    t.lexer.pop_state()
    return t

  def t_string_ESCAPE(self, t):
    r'\x5C'  # '\'
    t.lexer.push_state('escaped')
    return t
  
  # Don't skip over any tokens inside the escaped state
  t_escaped_ignore = ''

  def t_escaped_QUOTATION_MARK(self, t):
    r'\x22'  # '"'
    t.lexer.pop_state()
    return t

  def t_escaped_REVERSE_SOLIDUS(self, t):
    r'\x5C'  # '\'
    t.lexer.pop_state()
    return t

  def t_escaped_SOLIDUS(self, t):
    r'\x2F'  # '/'
    t.lexer.pop_state()
    return t

  def t_escaped_BACKSPACE_CHAR(self, t):
    r'\x62'  # 'b'
    t.lexer.pop_state()
    t.value = '\\b'
    return t

  def t_escaped_FORM_FEED_CHAR(self, t):
    r'\x66'  # 'f'
    t.lexer.pop_state()
    t.value = '\\f'
    return t

  def t_escaped_CARRIAGE_RETURN_CHAR(self, t):
    r'\x72'  # 'r'
    t.lexer.pop_state()
    t.value = '\\r'
    return t

  def t_escaped_LINE_FEED_CHAR(self, t):
    r'\x6E'  # 'n'
    t.lexer.pop_state()
    t.value = '\\n'
    return t

  def t_escaped_TAB_CHAR(self, t):
    r'\x74'  # 't'
    t.lexer.pop_state()
    t.value = '\\t'
    return t

  def t_escaped_UNICODE_HEX(self, t):
    r'\x75[\x30-\x39,\x41-\x46,\x61-\x66]{4}'  # 'uXXXX'
    t.lexer.pop_state()
    return t

  def tokenize(self, data, *args, **kwargs):
    self.lexer.input(data)
    tokens = list()
    while True:
      token = self.lexer.token()
      if not token: 
        break
      tokens.append(token)
    return tokens


indentation = 0
first_object = True

def print_indentation():
  global indentation
  sys.stdout.write(' '*2*indentation)

def increment_indentation():
  global indentation
  indentation = indentation + 1

def decrement_indentation():
  global indentation
  indentation = indentation - 1

def end_line():
  sys.stdout.write('\n')

class JsonParser(object):

  def __init__(self, lexer=None, **kwargs):
    if lexer is not None:
      if isinstance(lexer, JsonLexer):
        self.lexer = lexer.lexer
      else:
        self.lexer = lexer
    else:
      self.lexer = JsonLexer().lexer
    self.parser = ply.yacc.yacc(module=self, **kwargs)

  tokens = JSON_TOKENS
  
  def p_value_string(self, p):
    '''value : string'''
    p[0] = p[1]
  
  def p_value_number(self, p):
    '''value : number'''
    sys.stdout.write(str(p[1]))

  def p_value_empty_object(self, p):
    '''value : object'''

  def p_value_array(self, p):
    '''value : array'''
  
  def p_value_true(self, p):
    '''value : TRUE'''
    sys.stdout.write('true')
    
  def p_value_false(self, p):
    '''value : FALSE'''
    sys.stdout.write('false')

  def p_value_null(self, p):
    '''value : NULL'''

  def p_empty_object(self, p):
    '''object : BEGIN_OBJECT END_OBJECT'''
    global first_object
    first_object = False
    sys.stdout.write("{}\n")
    
  def p_not_empty_object(self, p):
    '''object : object_begin members object_end'''
    aux = p[2]
    to_set = set(aux)
    if len(to_set) != len(aux):
      raise "dos claves iguales en el mismo nivel"   
    first_object = False
  
  def p_object_begin(self, p):
    '''object_begin : BEGIN_OBJECT'''
    #increment_indentation()
    global first_object
    end_line()
    increment_indentation() 
    print_indentation()

  def p_object_end(self, p):
    '''object_end : END_OBJECT'''
    decrement_indentation()

  def p_members_final(self, p):
    '''members : pair'''
    p[0] = p[1]
    
  def p_members_not_final(self, p):
    '''members : pair_and_separator members'''
    p[0] =  p[1] + p[2]

  def p_pair_and_separator(self, p):
    '''pair_and_separator : pair VALUE_SEPARATOR'''
    p[0] = p[1]
    end_line()
    print_indentation()
  
  def p_pair(self, p):
    '''pair : key value_abst'''
    p[0] = p[1]

  def p_value_abst(self, p):
    '''value_abst : value'''
    p[0] = p[1]
    decrement_indentation()


  def p_key(self, p):
    '''key : string NAME_SEPARATOR'''
    sys.stdout.write(':')
    #end_line()
    increment_indentation()
    p[0] = p[1]
  
  def p_elements(self, p):
    '''elements : 
                | elements_not_final
                | elements_final'''
   
  def p_elements_not_final(self, p):
    '''elements_not_final : elements value_abst_elements VALUE_SEPARATOR'''
    print_indentation()
    sys.stdout.write('- ')

  def p_value_abst_elements(self, p):
    '''value_abst_elements : value'''
    end_line()

  def p_elements_final(self, p):
    '''elements_final : elements value'''
  
  def p_array(self, p):
    '''array : array_begin elements array_end'''

  def p_empty_array(self, p):
    '''array :  BEGIN_ARRAY END_ARRAY'''
    sys.stdout.write('[]')

  def p_array_begin(self, p):
    '''array_begin :  BEGIN_ARRAY'''
    end_line()
    increment_indentation()
    print_indentation()
    sys.stdout.write('- ')

  def p_array_end(self, p):
    '''array_end : END_ARRAY'''
    decrement_indentation()
    
  def p_number_positive(self, p):
    '''number : integer
              | float'''
    p[0] = p[1]
    
  def p_number_negative(self, p):
    '''number : MINUS integer
              | MINUS float'''
    p[0] = -p[2]
    
  def p_integer(self, p):
    '''integer : int'''
    p[0] = p[1]
    
  def p_integer_exp(self, p):
    '''integer : int exp'''
    p[0] = p[1] * (10 ** p[2])
    
  def p_number_float(self, p):
    '''float : int frac'''
    p[0] = p[1] + p[2]
    
  def p_number_float_exp(self, p):
    '''float : int frac exp'''
    p[0] = (p[1] + p[2]) * (10 ** p[3])
    
  def p_exp_negative(self, p):
    '''exp : E MINUS DIGITS'''
    p[0] = -p[3]

  def p_exp(self, p):
    '''exp : E DIGITS'''
    p[0] = int(p[2])
    
  def p_exp_positive(self, p):
    '''exp : E PLUS DIGITS'''
    p[0] = int(p[3])
    
  def p_frac(self, p):
    '''frac : DECIMAL_POINT DIGITS'''
    p[0] = float('0.'+str(p[2]))
    
  def p_int_zero(self, p):
    '''int : ZERO'''
    p[0] = int(0)

  def p_int_non_zero(self, p):
    '''int : DIGITS'''
    if p[1].startswith('0'):
      raise SyntaxError('Leading zeroes are not allowed.')
    p[0] = int(p[1])

  def p_string(self, p):
    '''string : QUOTATION_MARK chars QUOTATION_MARK'''
    sys.stdout.write(p[2])
    p[0] = [p[2]]

  def p_final_chars(self, p):
    '''chars : '''
    p[0] = ""
    
  def p_not_final_chars(self, p):
    '''chars : chars char'''
    p[0] = p[1]  + p[2].decode('utf-8') 
    
  def p_char(self, p):
    '''char : UNESCAPED
           | ESCAPE QUOTATION_MARK
           | ESCAPE REVERSE_SOLIDUS
           | ESCAPE SOLIDUS
           | ESCAPE BACKSPACE_CHAR
           | ESCAPE FORM_FEED_CHAR
             | ESCAPE LINE_FEED_CHAR
            | ESCAPE CARRIAGE_RETURN_CHAR
            | ESCAPE TAB_CHAR'''
    p[0] = bytearray(p[len(p) - 1], 'utf8')

  def p_error(self, p): 
    print( "Syntax error at '%s'" % p)

  # Invoke the parser
  def parse(self, data, lexer=None, *args, **kwargs):
    if lexer is None:
      lexer = self.lexer
    return self.parser.parse(data, lexer=lexer, *args, **kwargs)

parser = None

def parse(s):
  global parser
  if parser is None:
    parser = JsonParser()
  return parser.parse(s)


def parse_file(f):
  return parse(f.read())


def main(argv):
  if len(argv) > 1:
    for filename in argv[1:]:
      parse_file(open(filename))
  else:
    parse_file(sys.stdin)


if __name__ == '__main__':
  main(sys.argv)
