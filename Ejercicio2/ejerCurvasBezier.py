import matplotlib.pyplot as plt
import numpy as np
import csv
from pathlib import Path

MOSTRAR_PUNTOS_CONTROL = True
MOSTRAR_CONTORNO = True 
MOSTRAR_PIEZA = True

# Carpeta con los csv de las figuras
FIGURAS_PATH = Path("figuras")

COLOR_FONDO = "#f0f0f0"  # Gris claro para el fondo

# ====================================== CLASES =========================================

class BezierCurve():
    """
    Clase que representa una curva de Bezier de grado n. Contiene:
        - Puntos de control
        - Grado de la curva
        - Puntos de la curva calculados a partir de los puntos de control y el grado de la curva
        - Métodos para calcular los puntos de la curva
        - Transformaciones (traslación, rotación, escalado y reflexión).
    """
    def __init__(self, grado, controlPx, controlPy, resolution=20):
        """
        Inicializa la curva de Bezier a partir del grado, los puntos de control y la resolución (número de puntos a calcular en la curva).
        Calcula los puntos de la curva usando el método calculatePoints y los almacena en self.px y self.py.
        """
        if len(controlPx) != len(controlPy) != grado + 1:
            raise ValueError(f"El número de puntos de control debe ser {grado + 1} para una curva de grado {grado}.")
        self.grado = grado
        self.controlPx = np.array(controlPx)
        self.controlPy = np.array(controlPy)
        self.px, self.py = self.calculatePoints(resolution)

    def point(self, coorArr, i, j, t):
        """
        Calcula la posición de un punto en la curva para un t dado [0, 1], mediante el algoritmo de Casteljau.
        """
        if j == 0:
            return coorArr[i]
        else:             
            return (1 - t) * self.point(coorArr, i, j - 1, t) + t * self.point(coorArr, i + 1, j - 1, t)

    def calculatePoints(self, resolution=20):
        """
        Calcula todos los px y py de la curva usando el método point.
        """
        t_values = np.linspace(0, 1, resolution)
        px = np.array([self.point(self.controlPx, 0, self.grado, t) for t in t_values])
        py = np.array([self.point(self.controlPy, 0, self.grado, t) for t in t_values])
        return px, py
    
    def getPoints(self):
        return self.px, self.py
    
    def getControlPoints(self):
        return self.controlPx, self.controlPy

    def getGrado(self):
        return self.grado
    
    def translate(self, dx, dy):
        self.controlPx += dx
        self.controlPy += dy
        self.px += dx
        self.py += dy
        
    def rotate(self, angle_degrees):
        angle_radians = np.radians(angle_degrees)
        cos_angle = np.cos(angle_radians)
        sin_angle = np.sin(angle_radians)

        # Rotar puntos de control
        new_controlPx = self.controlPx * cos_angle - self.controlPy * sin_angle
        new_controlPy = self.controlPx * sin_angle + self.controlPy * cos_angle
        self.controlPx, self.controlPy = new_controlPx, new_controlPy

        # Rotar puntos de la curva
        new_px = self.px * cos_angle - self.py * sin_angle
        new_py = self.px * sin_angle + self.py * cos_angle
        self.px, self.py = new_px, new_py
    
    def scale(self, sx, sy):
        self.controlPx *= sx
        self.controlPy *= sy
        self.px *= sx
        self.py *= sy
        
    def reflexion(self, axis='x'):
        if axis == 'x':
            self.controlPy = -self.controlPy
            self.py = -self.py
        elif axis == 'y':
            self.controlPx = -self.controlPx
            self.px = -self.px
        elif axis == 'xy':
            self.controlPx = -self.controlPx
            self.controlPy = -self.controlPy
            self.px = -self.px
            self.py = -self.py
        else:
            raise ValueError("El eje de reflexión debe ser 'x', 'y' o 'xy'.")
    

class Figure():
    """
    Clase que representa una figura compuesta por varias curvas de Bezier. Contiene:
        - Lista de curvas de Bezier
        - Color de relleno de la figura
        - Nombre de la figura
        - Número de capa para el Algoritmo del Pintor
        - Métodos para dibujar la figura y para aplicar transformaciones a todas las curvas de la figura (traslación, rotación, escalado y reflexión).  
    """
    def __init__(self, curves=None, csv_path=None):
        """
        Inicializa la figura a partir de una lista de curvas de Bezier o a partir de un archivo CSV. Si se proporciona un archivo CSV, se llama al método setCurvesFromCsv para cargar las curvas desde el archivo.
        """
        self.curves = []
        self.color = "#000000" #Negro por defecto
        self.nombre = "Figura"
        self.capa = 0
        if curves != None:
            self.curves = curves
        if csv_path != None:
            self.nombre = csv_path.stem # Nombre del archivo sin extensión como nombre de la figura
            self.setCurvesFromCsv(csv_path)

    def setCurves(self, curves):
        self.curves = curves
    
    def setCurvesFromCsv(self, csv_path):
        """
        Carga las curvas de Bezier desde un archivo CSV. El formato del CSV es el siguiente:
            - Cada curva se define por dos filas: la primera fila contiene el tipo de curva ('l' para línea, 'q' para curva cuadrática y 'c' para curva cúbica) seguida de las coordenadas X de los puntos de control, y la segunda fila contiene las coordenadas Y de los puntos de control. El punto final de cada curva es el primer punto de la siguiente curva, excepto para la última curva, cuyo punto final se define en la fila siguiente.
            - Después de la última curva, se incluye un par de filas con el tipo 'f' y el punto final de la última curva (o 'close' para indicar que el punto final es el primer punto de la primera curva).
            - La última fila contiene el color de relleno y el número de capa de la figura.
        """
        with open(csv_path, mode='r', encoding='utf-8') as archivo:
            lector_csv = list(csv.reader(archivo))
        
        # Recorrer de 2 en 2 filas (curvas de 2 dimensiones)
        # Ventana deslizante de 4 filas (poder ver curva actual y siguiente curva para obtener punto de unión)
        i = 0
        fin = False
        while not fin:
            # --- CURVA SIGUIENTE (Filas i+2 e i+3) ---
            # Obtener punto final de curva actual
            tipo_siguiente = lector_csv[i+2][0].strip()
            if tipo_siguiente == 'f': # Final del archivo
                if lector_csv[i+2][1].strip() == "close": # Punto final = primer punto de primera curva
                    puntosPrimeraCurvaX, puntosPrimeraCurvaY = self.curves[0].getPoints()
                    p_final_x = puntosPrimeraCurvaX[0]
                    p_final_y = puntosPrimeraCurvaY[0]
                else:
                    p_final_x = float(lector_csv[i+2][1])
                    p_final_y = float(lector_csv[i+3][1])
                # Obtener metadatos
                self.color = lector_csv[i+4][0].strip()
                self.capa = int(lector_csv[i+4][1].strip())
                fin = True
            else:
                p_final_x = float(lector_csv[i+2][1])
                p_final_y = float(lector_csv[i+3][1])

            # --- CURVA ACTUAL (Filas i e i+1) ---
            tipo_actual = lector_csv[i][0].strip()
            px_actual = np.array([*(float(x) for x in lector_csv[i][1:] if x.strip()), p_final_x])
            py_actual = np.array([*(float(y) for y in lector_csv[i+1][1:] if y.strip()), p_final_y])
            
            # --- INSTANCIACIÓN Y DIBUJO ---
            if tipo_actual == 'l':
                curva = BezierCurve(1, px_actual, py_actual)
            elif tipo_actual == 'q':
                curva = BezierCurve(2, px_actual, py_actual)
            elif tipo_actual == 'c':
                curva = BezierCurve(3, px_actual, py_actual)
            
            self.curves.append(curva)
            i+=2

    def drawPoints(self, ax=None, show=False):
        """
        Dibuja la figura mostrando los puntos de la curva (en azul) y los puntos de control (en rojo con línea punteada).
        Si se proporciona un objeto ax, se dibuja en él.
        Si show es True, se muestra la figura al finalizar el dibujo.
        """
        if ax is None:
            fig, ax = plt.subplots()
            
            ax.set_facecolor(COLOR_FONDO)
            ax.set_aspect('equal', adjustable='datalim')
            ax.set_title(f"{self.nombre} - sin interpolación")

        for curve in self.curves:
            px, py = curve.getPoints()
            
            # Curva Bezier (puntos azules)
            ax.plot(px, py, 'b.', markersize=2, label='Curva')
            
            # Puntos de control (puntos rojos con línea punteada)
            ax.plot(curve.controlPx, curve.controlPy, 'ro--', 
                    linewidth=1, 
                    alpha=0.6)

        if show:
            plt.show()

    def drawInterpolate(self, ax=None, show=False):
        """
        Dibuja la figura mostrando la curva de Bezier interpolada (en azul) y los puntos de control (en rojo con línea punteada).
        Si se proporciona un objeto ax, se dibuja en él.
        Si show es True, se muestra la figura al finalizar el dibujo.
        """
        if ax is None:
            fig, ax = plt.subplots()
            
            ax.set_facecolor(COLOR_FONDO)
            ax.set_aspect('equal', adjustable='datalim') 
            ax.set_title(f"{self.nombre} - con interpolación")

        for curve in self.curves:
            px, py = curve.getPoints()
            
            # Curva Bezier (linea azul)
            ax.plot(px, py, 'b-', markersize=2, label='Curva')
            
            # Puntos de control (puntos rojos con linea punteada)
            ax.plot(curve.controlPx, curve.controlPy, 'ro--', 
                    linewidth=1, 
                    alpha=0.6)

        if show:
            plt.show()
    
    def drawFilled(self, ax=None, show=False):
        """
        Dibuja la figura rellenando el interior de la curva de Bezier con el color especificado en self.color.
        Si se proporciona un objeto ax, se dibuja en él.
        Si show es True, se muestra la figura al finalizar el dibujo.
        """
        if ax is None:
            fig, ax = plt.subplots()
            
            ax.set_facecolor(COLOR_FONDO)
            ax.set_aspect('equal', adjustable='datalim') 
            ax.set_title(f"{self.nombre} - Relleno")

        todos_px = []
        todos_py = []

        # Recopilar puntos de las curvas
        for curve in self.curves:
            px, py = curve.getPoints()
            # Convertir a lista y concatenar (sin duplicar el punto de unión)
            todos_px.extend(px[:-1].tolist()) 
            todos_py.extend(py[:-1].tolist())
            
        # Añadir el último punto de la última curva para cerrar la figura
        p_final_x, p_final_y = self.curves[-1].getPoints()
        todos_px.append(p_final_x[-1])
        todos_py.append(p_final_y[-1])

        # Dibujar
        ax.fill(todos_px, todos_py, facecolor=self.color, edgecolor=self.color, linewidth=1)

        if show:
            plt.show()
    
    def translate(self, dx, dy):
        for curve in self.curves:
            curve.translate(dx, dy)
    
    def rotate(self, angle_degrees):
        for curve in self.curves:
            curve.rotate(angle_degrees)
    
    def scale(self, sx, sy):
        for curve in self.curves:
            curve.scale(sx, sy)
    
    def reflexion(self, axis='x'):
        for curve in self.curves:
            curve.reflexion(axis)
            
    def centroide(self):
        todos_px = []
        todos_py = []

        for curve in self.curves:
            px, py = curve.getPoints()
            todos_px.extend(px[:-1].tolist()) 
            todos_py.extend(py[:-1].tolist())
            
        p_final_x, p_final_y = self.curves[-1].getPoints()
        todos_px.append(p_final_x[-1])
        todos_py.append(p_final_y[-1])

        x = np.array(todos_px)
        y = np.array(todos_py)

        A = 0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])
        Cx = (1/(6*A)) * np.sum((x[:-1] + x[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1]))
        Cy = (1/(6*A)) * np.sum((y[:-1] + y[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1]))

        return Cx, Cy
    
    def toCsv(self):
        csv = ""
        
        for curve in self.curves:
            controlPx, controlPy = curve.getControlPoints()
            tipo = 'l' if curve.getGrado() == 1 else 'q' if curve.getGrado() == 2 else 'c'
            csv += tipo + "," + ",".join(str(px) for px in controlPx[:-1]) + "\n"
            csv += "," + ",".join(str(py) for py in controlPy[:-1]) + "\n"
        csv += "f,close\n"
        csv += ",\n"
        csv += self.color + "," + str(self.capa) + "\n"
        return csv


# ========================================== MAIN ==========================================

def main():
    # Cargar archivos csv
    csv_files = list(FIGURAS_PATH.glob("*.csv"))

    # Crear figuras a partir de los archivos csv
    figuras = [Figure(csv_path=csv_file) for csv_file in csv_files]

    # Dibujar cada figura por separado con diferentes opciones de visualización
    for figura in figuras:
        if MOSTRAR_PUNTOS_CONTROL: figura.drawPoints(show=True)
        if MOSTRAR_CONTORNO: figura.drawInterpolate(show=True)
        if MOSTRAR_PIEZA: figura.drawFilled(show=True)
        
    # Mostrar figura completa
    # Algoritmo del pintor
    fig, ax = plt.subplots()
    
    ax.set_facecolor(COLOR_FONDO)
    ax.set_aspect('equal', adjustable='datalim') 
    ax.set_title("Figura completa")
    figuras.sort(key=lambda f: f.capa) # ordenar por capa (de menor a mayor)
    for figura in figuras:
        figura.drawFilled(ax=ax)
    plt.show()
    
if __name__ == "__main__":
    main()
