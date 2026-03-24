# Ejercicio 1 - Estimación de volúmenes por Monte Carlo

Álvaro Santiso Freire - alvaro.santiso@udc.es
Daniel Quintillán Quintillán - daniel.quintillan@udc.es

## Descripción

Programa que utiliza el método de Monte Carlo para estimar volúmenes de figuras geométricas 3D:

- **Toro** con radio exterior 1.5 y radio interior 0.5.
- **Dos esferas** de radio 0.5 situadas en las posiciones x = -2 y x = 2.

El programa realiza las siguientes tareas:

1. **Estimación del volumen del toro** y comparación con el valor exacto.
2. **Estimación del volumen de las esferas** y verificación de simetría.
3. **Estimación del volumen de las intersecciones** toro-esfera.
4. **Estimación del volumen de la unión** toro-esferas.
5. **Verificación de consistencia** mediante la fórmula de inclusión-exclusión.
6. **Análisis de convergencia**: estudio del error relativo medio en función del número de muestras (N = 1000, 10000, 100000, 1000000) con 50 repeticiones por caso, y comparación con la tasa teórica de convergencia $O(1/\sqrt{N})$.

## Requisitos

- Python 3.10 o superior
- pip

## Configuración del entorno

Situarse en el directorio del ejercicio:

```bash
cd Ejercicio1
```

Crear un entorno virtual e instalar las dependencias:

```bash
python3 -m venv venv
source venv/bin/activate   # En macOS/Linux
# venv\Scripts\activate    # En Windows
pip install -r requirements.txt
```

### Dependencias principales

| Paquete      | Uso                                                        |
|--------------|------------------------------------------------------------|
| `numpy`      | Generación de números aleatorios y cálculo numérico        |
| `matplotlib` | Visualización de la gráfica de convergencia                |
| `scipy`      | Regresión lineal para el análisis de la tasa de convergencia |

## Ejecución

Con el entorno virtual activado, ejecutar el archivo principal:

```bash
python ejercicio1.py
```

El programa imprimirá por consola los resultados de las estimaciones y mostrará una gráfica log-log comparando la convergencia empírica con la teórica.

> **Nota:** La ejecución puede tardar varios minutos debido al alto número de simulaciones (1.000.000 de muestras en el análisis principal y 50 repeticiones × 4 tamaños de muestra en el análisis de convergencia).
