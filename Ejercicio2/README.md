# Practica Curvas de Bezier

Álvaro Santiso Freire - alvaro.santiso@udc.es
Daniel Quintillán Quintillán - daniel.quintillan@udc.es

## Archivos

- Carpeta ```figuras```
    Contiene archivos csv con las subfiguras (Curvas de Bezier cerradas) que componen la figura.
    Cada archivo contiene las Curvas de Bezier (coordenadas de los puntos de control) de una subfigura y metadatos.
    La estructura del archivo es la siguiente:
        Cada curva se representa mediante dos filas. En la primera fila se indica el tipo de curva (l, q, c) y las coordenadas X de los puntos de control. En la segunda fila se indican las coordenadas Y de los puntos de control.
        El punto final de una curva no se indica, se corresponde con el primero de la siguiente curva.
        Las dos filas siguientes a la última curva se marcan con el tipo 'f' para indicar las coordenadas del punto final (o "close" si la curva es cerrada, correspondiendose el punto final con el primer punto de la primera curva).
        En la última fila se indican metadatos de la subfigura (color y capa de dibujado).

- Carpeta ```Ferrari```
    Contiene la imagen modelo que se va a dibujar (ferrari.svg) y archivos de apoyo para generar los archivos csv junto con el parser.

- parserSVG.py
    Traduce un archivo svg que contenga una única curva cerrada a un archivo csv (con la sintaxis explicada en el apartado anterior).

- ejerCuvasBezier.py
    Código principal.
    Modificar el valor de las variables al principio del archivo (MOSTRAR_PUNTOS_CONTROL, MOSTRAR_CONTORNO, MOSTRAR_PIEZA) según lo que se desee visualizar.
    BezierCurve: clase que representa una curva de Bezier de grado n. Contiene:
        - Puntos de control
        - Grado de la curva
        - Puntos de la curva calculados a partir de los puntos de control y el grado de la curva
        - Métodos para calcular los puntos de la curva
        - Transformaciones (traslación, rotación, escalado y reflexión).
    Figura: Clase que representa una figura compuesta por varias curvas de Bezier. Contiene:
        - Lista de curvas de Bezier
        - Color de relleno de la figura
        - Nombre de la figura
        - Número de capa para el Algoritmo del Pintor
        - Métodos para dibujar la figura y para aplicar transformaciones a todas las curvas de la figura (traslación, rotación, escalado y reflexión).  
        
## Requisitos

- Python 3.10 o superior
- pip

## Configuración del entorno

Situarse en el directorio raíz del proyecto:

```bash
cd Ejercicio2
```

Crear un entorno virtual e instalar las dependencias:

```bash
python3 -m venv venv
source venv/bin/activate   # En macOS/Linux
# venv\Scripts\activate    # En Windows
pip install -r requirements.txt
```

### Dependencias principales

| Paquete | Uso |
|---------|-----|
| `matplotlib` | Visualización y dibujo de las curvas |
| `numpy` | Cálculo numérico (puntos de Bezier, transformaciones) |
| `svgpathtools` | Parseo de archivos SVG (usado por `parserSVG.py`) |

## Ejecución

Con el entorno virtual activado, ejecutar el archivo principal:

```bash
python ejerCurvasBezier.py
```

Se pueden modificar las variables al inicio de `ejerCurvasBezier.py` para controlar la visualización:

```python
MOSTRAR_PUNTOS_CONTROL = True   # Muestra los puntos de control de cada curva
MOSTRAR_CONTORNO = True         # Muestra el contorno interpolado de cada figura
MOSTRAR_PIEZA = True            # Muestra cada pieza rellena individualmente
```

Para generar un archivo CSV a partir de un SVG con una curva cerrada:

```bash
python parserSVG.py
```
