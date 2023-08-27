import tkinter as tk, time
from tkinter import filedialog

# Cristhianbrh
class NewWindowDialog():
    def __init__(self):
        self.points = tk.StringVar()
        self.points.set("A - B - C")
        self.pixelColor = tk.StringVar()
        self.pixelColor.set("(0,0,0)")

    # def setParams(self, points):
    #     self.points.set(points)
    
    # def setParams(self, pixelColor):
    #     self.pixelColor.set(pixelColor)

    def new_window(self):
        dialog = tk.Toplevel(app)
        dialog.title("Puntformat")
        label = tk.Label(dialog, text=f"Cuadrante {self.points.get()}: {self.pixelColor.get()}")
        label.pack(padx=20, pady=20)
        dialog.grab_set()

def btn_Clicked():
    archiveSelect = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    archive = ""
    if(archiveSelect):
        archive = initArchive(archiveSelect)

        newWindowDialog.new_window()

        saveArchive = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if(saveArchive):
            with open(saveArchive, 'w') as archiveSave:
                archiveSave.write(archive)

def initArchive(archivePath):
    dictLetter = 'ABCDEFGHIJKLMNOPQRSTUVWZ'
    letterNum = 0

    puntos = {}
    with open(archivePath, 'r') as arch:
        isBegin= False
        dataPnt = ''

        letterAct = 0
        for line in arch:
            lineNew = line.strip()
            if lineNew == r'\begin{scriptsize}':
                isBegin = True

            if isBegin:
                if lineNew[0:5] == r'\draw':
                    if 'circle' in lineNew:
                        data = lineNew.split(' ')[-3]
                        dataPnt = data
                        puntos[dataPnt] = dictLetter[letterAct] + ('' if letterNum == 0 else str(letterNum))
                                
                        letterAct += 1
                        if len(dictLetter) == letterAct:
                            letterAct = 0
                            letterNum += 1
    textForNum = [
        'GL_POINTS',
        'GL_LINES',
        'GL_TRIANGLES',
        'GL_QUADS',
        'GL_POLYGON'
    ]
    txt = ""
    with open(archivePath, 'r') as arch:
        for line in arch:
            line = line.strip()
            if line[0:5] == r'\fill':
                # print(line)
                dta = line.split('] ')[1].split(' -- ')[:-1]

                countPoints = len(dta)
                txt += f"//Polygon "
                pointsDt = ""
                for i in range(countPoints):
                    pointsDt += (' - ' if i == 0 else '') + str(puntos[dta[1]])

                newWindowDialog.points.set(pointsDt)

                txt += pointsDt
                txt += f"\nglColor3ub(0 , 0, 0);\n"
                print( "Cantidad: " , countPoints)
                txt += f"glBegin({textForNum[countPoints-1] if (countPoints) < 5 else textForNum[4]});\n"

                # print(txt)
                # print(dta)
                # print('LengData: ' + str(countPoints))

                for i in range(countPoints):
                    txt += f"\tglVertex2f{dta[i]};\n"
                txt += f"glEnd();\n\n"
                
                # print(line.split(' ')[3])
    
    return txt
            
def tkDraw():
    botonSelect = tk.Button(app, text='Seleccionar archivo', command=btn_Clicked)
    botonSelect.pack()

    

    # tk.Text("Este es un programa generado y creado por Cristhian Alexander Bautista Ruiz").pack()
    # tk.Text("Indicaciónes: ").pack()
    # tk.Text("Paso 1: Dibujar en geogebra clasico").pack()
    # tk.Text("Paso 2: Exportar archivo en formato PGF/TikZ(.txt) ").pack()

# def windowTofront():
#     app.lift()
#     app.after(100, windowTofront)

def __main__():
    global app 
    global newWindowDialog
    app = tk.Tk()
    newWindowDialog = NewWindowDialog()

    app.geometry("400x300")
    app.title("PUNTFORMAT")
    tkDraw()
    # windowTofront()
    app.mainloop()


if __name__ == "__main__":
    __main__()
