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

* true, false, ...

* enumerar más!

* poner todos pls

##Parser


