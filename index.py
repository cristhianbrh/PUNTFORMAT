import tkinter as tk
from tkinter import filedialog

# Cristhianbrh
def btn_Clicked():
    archiveSelect = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    archive = ""
    if(archiveSelect):
        archive = initArchive(archiveSelect)
    
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
                txt += f"//Triangle "
                for i in range(countPoints):
                    txt += ' - ' + str(puntos[dta[1]])

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


app = tk.Tk()
app.geometry("400x300")
app.title("PUNTFORMAT")
tkDraw()
app.mainloop()

