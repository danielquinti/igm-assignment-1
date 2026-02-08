from svgpathtools import svg2paths
from svgpathtools.path import Line, CubicBezier, QuadraticBezier

FILE_NAME = "nick.svg"
PATH = f"figuras/{FILE_NAME}"

def print_svg_absolute(svg_file):
    paths, attributes = svg2paths(svg_file)
    csv = ""
    final = None
    inicio = None
    for path_index, path in enumerate(paths):
        for seg_index, segment in enumerate(path):
            final = segment.end
            if inicio == None:
                inicio = segment.start
                
            if isinstance(segment, Line):
                csv+=f"l,{segment.start.real}\n"
                csv+=f",{segment.start.imag}\n"

            elif isinstance(segment, QuadraticBezier):
                csv+=f"q,{segment.start.real},{segment.control.real}\n"
                csv+=f",{segment.start.imag},{segment.control.imag}\n"

            elif isinstance(segment, CubicBezier):
                csv+=f"c,{segment.start.real},{segment.control1.real},{segment.control2.real}\n"
                csv+=f",{segment.start.imag},{segment.control1.imag},{segment.control2.imag}\n"
            else:
                csv+=f"OTHER: {segment}\n" 
        
    if final:
        if final == inicio:
            csv+="f, close\n"
            csv+=", \n"
        else:
            csv+=f"f,{final.real}\n"
            csv+=f",{final.imag}\n"
    else:
        csv+="f, close\n"
        csv+=", \n"

    print(csv)

    csvFileName = PATH.split(".")[0] + ".csv"
    with open(csvFileName, "w", encoding="utf-8") as f:
        f.write(csv)

if __name__ == "__main__":
    print_svg_absolute(PATH)