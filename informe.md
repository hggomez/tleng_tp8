#Traductor de JSON a YAML



Integrante | Libreta | Correo
--- | --- | --- |
Fachal, Matías | 154/15  | `mfachal@dc.uba.ar`  
Gomez, Horacio | 756/13 | ` horaciogomez.1993@gmail.com` |
Gonzalez, Juan |   | ` `  

##Introducción

El objetivo de este trabajo es crear un traductor que tome cadenas válidas en el lenguaje _JSON_ y las traduzca al lenguaje YAML, teniendo en cuenta que _JSON_ soporta más de unaclave con un mismo nombre y YAML, en cuyo caso la traducción no será posible. Utilizamos la biblioteca _ply_ debido a que utiliza gramáticas _LALR_ y ya teníamos una.

##Gramática:

Tomamos la gramática definida en la [página oficial de JSON](https://www.json.org).

##Lexer

Una vez que terminamos con la gramática implementamos el lexer. Este se encarga de transformar la cadena recibida en terminales de nuestra gramática, para que luego el parser pueda reconstruir el árbol.
Los distintos terminales son asociados a tokens que representan de manera más general a los mismos.

Los tokens que utilizamos son los siguientes:
* BEGIN_ARRAY, representando al [
* BEGIN_OBJECT, representando al {
* END_ARRAY, representa el fin de un array, ]
* END_OBJECT, }
* NAME_SEPARATOR, representa el :
* VALUE_SEPARATOR, `,`
* QUOTATION_MARK, `"`
* FALSE, directamente la string `false`
* TRUE, `true`
* NULL, `null`
* DECIMAL_POINT, `.`
* DIGITS, representando los dígitos del 0 al 9
* E, `e`, como exponente
* MINUS, `-`, como resta o prefijo de un negativo
* PLUS, `+`, similarmente
* ZERO, `0`
* UNESCAPED, representa cualquier caracter no escapado
* ESCAPE, representa al caracter `\`, el lexer entra en el estado en que considera la string como escapada
* REVERSE_SOLIDUS, en un estado escapado, representa al caracter `\`
* SOLIDUS, `/`, similarmente
* BACKSPACE_CHAR, `b`, ídem
* FORM_FEED_CHAR, `f`, ídem
* LINE_FEED_CHAR, `n`, ídem
* CARRIAGE_RETURN_CHAR, `r`, ídem
* TAB_CHAR, `t`, ídem
* UNICODE_HEX, en un estado escapado representa a las strings del tipo `uXXXX`, las cuales actualmente no se interpretan especialmente.

##Parser

Una vez que se obtiene la cadena _tokenizada_, solo resta hacer la traducción al lenguaje _YAML_. Para este fin, mantenemos una variable global que indica el nivel de _anidamiento_, lo cual necesitamos para traducir cada terminal con el nivel de _indentación_ correspondiente. También tuvimos que agregar un atributo sintetizado que permite chequear que no haya claves repetidas dentro de un diccionario de _JSON_, ya que _YAML_ no soporta esto. 
Al encontrarnos con dos claves iguales dentro de un mismo diccionario dejamos de traducir. Gracias a esto es que podemos detectar en qué parte del _JSON_ se produjo el error.


##Requerimientos de software

- Python 3.5+
- Ply 3.11+

La cadena que se desee traducir deberá estar almacenada en un archivo. Para traducirla se deberá ejecutar el siguiente comando: `python3 json.py nombredelarchivo`


