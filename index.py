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
    textComplete = ""

    with open(archivePath, 'r') as arch:
        for line in arch:
            lineNew = line.strip()
            if lineNew[0:5] == r'\fill':
                txt = lineNew[5:].split(' ')
                
                p1 = txt[3]
                p2 = txt[5]
                p3 = txt[7]
                print(p1 + " / " + p2 + ' /' + p3)
                textComplete+=(f'''
//Triangle {puntos[p1]} - {puntos[p2]} - {puntos[p3]}
glColor3ub(0 , 0, 0);
glBegin(GL_TRIANGLES);
    glVertex2f{p1};
    glVertex2f{p2};
    glVertex2f{p3};
glEnd();\n''')
    
    return textComplete
            
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

