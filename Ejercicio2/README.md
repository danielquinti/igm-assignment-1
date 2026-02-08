Ejercicio de dibujado mediante curvas de Bezier.

- Carpeta ```figuras```

Curvas situadas en carpeta ```figuras```. Se dibujarán todos los archivos csv.
Cada archivo indica las coordenadas de las curvas de una figura, además de metadatos.
Cada dos filas corresponden a una curva (la primera fila para las coordenadas X y la segunda para las Y).
El tipo de curva se indica en la primera columna y puede ser: l, q, c.
El punto final de una curva no se indica, se corresponde con el primero de la siguiente.
Al final del archivo se indica las coordenadas del puntos final o "close" si la curva es cerrada.
En la última fila se indican metadatos de la figura (de momento solo el color).

- parserSVG.py

Traduce un archivo svg a un archivo csv (con la sintaxis explicada en el apartado anterior).
Funciona para una única figura cerrada (si el archivo contiene varias, es necesario dividirlo en varios archivos previamente, teniendo precaución con las coordenadas relativas de los puntos).

- ejerCuvasBeizer.py

Código principal.
BezierCurve: clase abstracta para las curvas de Beizer. Las clases concretas implementarán el método point dependiendo del tipo de curva.
Figure: clase que representa a una figura cerrada mediante una lista de curvas de Bezier.

- Procedimiento
    1. Obtener un archivo svg por cada figura cerrada (mediante un editor como inkscape) y almacenarlos en la carpeta ```figuras```.
    2. Para cada archivo svg, aplicar parserSVG.py, obteniendo los correspondientes csv.
    3. Ejecutar ejerCurvasBeizer.py para mostrar las figuras. (falta mostrar el resultado conjunto de todas)
