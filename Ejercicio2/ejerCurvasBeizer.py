import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
import csv
from pathlib import Path

# Carpeta con los csv de las figuras
FIGURAS_PATH = Path("figuras")

# ====================================== CLASES =========================================

class BezierCurve(ABC):
    def __init__(self, controlPx, controlPy, resolution=20):
        """
        Inicializa la curva con los puntos de control.
        :param px: Lista o array con las coordenadas X de los puntos de control.
        :param py: Lista o array con las coordenadas Y de los puntos de control.
        """
        self.controlPx = np.array(controlPx)
        self.controlPy = np.array(controlPy)
        self.px, self.py = self.calculatePoints(resolution)

    @abstractmethod
    def point(self, t):
        """
        Calcula la posición (x, y) de un punto en la curva para un t dado [0, 1].
        """
        pass

    def calculatePoints(self, resolution=20):
        """
        Calcula todos los px y py de la curva usando el método point.
        """
        t_values = np.linspace(0, 1, resolution)
        points = np.array([self.point(t) for t in t_values])
        return points[:, 0], points[:, 1]
    
    def getPoints(self):
        return self.px, self.py
    
    
class LinearBezierCurve(BezierCurve):
    def __init__(self, controlPx, controlPy, resolution=20):
        if len(controlPx) != 2 or len(controlPy) != 2:
            raise ValueError("LinearBezier espera exactamente dos puntos de control.")
        super().__init__(controlPx, controlPy, resolution)

    def point(self, t):
        # Fórmula: P = (1-t)P0 + tP1
        x = (1 - t) * self.controlPx[0] + t * self.controlPx[1]
        y = (1 - t) * self.controlPy[0] + t * self.controlPy[1]
        return x, y


class QuadraticBezierCurve(BezierCurve):
    def __init__(self, controlPx, controlPy):
        if len(controlPx) != 3 or len(controlPy) != 3:
            raise ValueError("QuadraticBezierCurve espera exactamente tres puntos de control.")
        super().__init__(controlPx, controlPy)

    def point(self, t):
        # Algoritmo de De Casteljau o fórmula polinómica
        x = (1-t)**2 * self.controlPx[0] + 2*(1-t)*t * self.controlPx[1] + t**2 * self.controlPx[2]
        y = (1-t)**2 * self.controlPy[0] + 2*(1-t)*t * self.controlPy[1] + t**2 * self.controlPy[2]
        return x, y
    

class CubicBezierCurve(BezierCurve):
    def __init__(self, controlPx, controlPy):
        if len(controlPx) != 4 or len(controlPy) != 4:
            raise ValueError("CubicBezierCurve espera exactamente cuatro puntos de control.")
        super().__init__(controlPx, controlPy)

    def point(self, t):
        # Algoritmo de De Casteljau o fórmula polinómica
        x = (1-t)**3 * self.controlPx[0] + 3*(1-t)**2*t * self.controlPx[1] + 3*(1-t)*t**2 * self.controlPx[2] + t**3 * self.controlPx[3]
        y = (1-t)**3 * self.controlPy[0] + 3*(1-t)**2*t * self.controlPy[1] + 3*(1-t)*t**2 * self.controlPy[2] + t**3 * self.controlPy[3]
        return x, y
    
# TODO: implementar dibujado con relleno, sin puntos de control, función de posición y excalado...
# TODO: si fuese necesario, incorporar traslacion a partir de información en la ultima fila del csv (metadatos) -> permitir encajar las figuras cuando se compongan
class Figure():
    def __init__(self, curves=None, csv_path=None):
        self.curves = []
        self.color = "#000000" #Negro por defecto
        self.nombre = "Figura"
        if curves != None:
            self.curves = curves
        if csv_path != None:
            self.nombre = csv_path.stem # Usar el nombre del archivo sin extensión como nombre de la figura
            self.setCurvesFromCsv(csv_path)

    def setCurves(self, curves):
        self.curves = curves
    
    def setCurvesFromCsv(self, csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as archivo:
            lector_csv = list(csv.reader(archivo))
        
        # Recorremos de 2 en 2 filas (dimensión 2)
        # Ventana deslizante de 4 filas (poder ver curva actual y siguiente curva para obtener punto de unión)
        for i in range(0, len(lector_csv) - 2, 2):
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
                    self.color = lector_csv[i+4][0].strip() #Obtener metadatos de la última linea
            else:
                p_final_x = float(lector_csv[i+2][1])
                p_final_y = float(lector_csv[i+3][1])

            # --- CURVA ACTUAL (Filas i e i+1) ---
            tipo_actual = lector_csv[i][0].strip()
            px_actual = np.array([*(float(x) for x in lector_csv[i][1:] if x.strip()), p_final_x])
            py_actual = np.array([*(float(y) for y in lector_csv[i+1][1:] if y.strip()), p_final_y])
            
            # --- INSTANCIACIÓN Y DIBUJO ---
            if tipo_actual == 'l':
                curva = LinearBezierCurve(px_actual, py_actual)
            elif tipo_actual == 'q':
                curva = QuadraticBezierCurve(px_actual, py_actual)
            elif tipo_actual == 'c':
                print(px_actual, py_actual)
                curva = CubicBezierCurve(px_actual, py_actual)
            
            self.curves.append(curva)

    def drawPoints(self):
        for curve in self.curves:
            px, py = curve.getPoints()
            # 1. Dibuja la curva de Bezier resultante (azul sólido)
            plt.title(self.nombre + " - sin interpolación")
            plt.plot(px, py, 'b.', linewidth=2, label='Curva')
            
            # 2. Dibuja el polígono de control (puntos rojos con línea punteada)
            # 'ro' dibuja los puntos, linestyle='--' hace la unión punteada
            plt.plot(curve.controlPx, curve.controlPy, 'ro', 
                     linestyle='--', 
                     linewidth=1, 
                     alpha=0.6) # Un poco de transparencia para no distraer
        plt.show()
            
    def drawInterpolate(self):
        for curve in self.curves:
            px, py = curve.getPoints()
            # 1. Dibuja la curva de Bezier resultante (azul sólido)
            plt.title(self.nombre + " - con interpolación")
            plt.plot(px, py, 'b-', linewidth=2, label='Curva')
            
            # 2. Dibuja el polígono de control (puntos rojos con línea punteada)
            # 'ro' dibuja los puntos, linestyle='--' hace la unión punteada
            plt.plot(curve.controlPx, curve.controlPy, 'ro', 
                     linestyle='--', 
                     linewidth=1, 
                     alpha=0.6) # Un poco de transparencia para no distraer
        plt.show()
    
    def drawFilled(self):
        todos_px = []
        todos_py = []

        # 1. Recopilamos todos los puntos de todas las curvas en orden
        for curve in self.curves:
            px, py = curve.getPoints()
            # Convertimos a lista y extendemos (evitando duplicar el punto de unión)
            todos_px.extend(px[:-1].tolist()) 
            todos_py.extend(py[:-1].tolist())
            
        # Añadimos el último punto de la última curva para cerrar el camino
        p_final_x, p_final_y = self.curves[-1].getPoints()
        todos_px.append(p_final_x[-1])
        todos_py.append(p_final_y[-1])

        # 2. Dibujamos el relleno
        # 'facecolor' es el color de relleno, 'edgecolor' el borde
        plt.title(f"{self.nombre} - Relleno")
        plt.fill(todos_px, todos_py, facecolor=self.color, edgecolor=self.color, linewidth=1)
        
        plt.show()
        

# ========================================== MAIN ==========================================

def main():
    csv_files = list(FIGURAS_PATH.glob("*.csv"))
    print(csv_files)
    figuras = [Figure(csv_path=csv_file) for csv_file in csv_files]

    for figura in figuras:
        figura.drawPoints()
        figura.drawInterpolate()
        figura.drawFilled()


if __name__ == "__main__":
    main()
