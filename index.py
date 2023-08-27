import tkinter as tk, threading
from tkinter import filedialog
import pyautogui
from plyer import notification
from pynput.mouse import Listener, Button


# Cristhianbrh
class NewWindowDialog():
    def __init__(self):
        self.points = tk.StringVar()
        self.points.set("A - B - C")
        self.pixelColor = tk.StringVar()
        self.pixelColor.set("(0,0,0)")

    def setParamsPoints(self, points):
        self.points.set(points)
    
    def setParamsColors(self, pixelColor):
        self.pixelColor.set(pixelColor)

    def new_window(self):
        dialog = tk.Toplevel(app)
        dialog.title("Puntformat")
        
        label = tk.Label(dialog, text=f"Cuadrante {self.points.get()}: {self.pixelColor.get()}")
        label.pack(padx=20, pady=20)
        dialog.lift()
        # dialog.grab_set()



def btn_Clicked():
    # global newWindowDialog
    # newWindowDialog = NewWindowDialog()
    
    archiveSelect = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    archive = ""
    if(archiveSelect):
        # newWindowDialog.new_window()

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
                txt += f"//Polygon "
                pointsDt = ""
                for i in range(countPoints):
                    pointsDt += (' - ' if i != 0 else '') + str(puntos[dta[i]])
                print(pointsDt)

                notification.notify(title= 'PUNTFORMAT', message=pointsDt, timeout=10, ticker=pointsDt)

                # colorDataPolygon = ""
                def saveOnClick(x, y, button, pressed):
                    if pressed and button == Button.right:
                        global colorDataPolygon
                        print("Ingresado")
                        r,g,b = pyautogui.pixel(x,y)
                        colorDataPolygon = f'(({round(r/255, 4)}),({round(g/255, 4)}),({round(b/255, 4)}))'
                        listener.stop()
                        # return f'({r}/255,{g}/255,{b}/255)'

                app.withdraw()
                with Listener(on_click=saveOnClick) as listener:
                    listener.join()

                app.deiconify()
                print(colorDataPolygon)
                # newWindowDialog.setParamsPoints(pointsDt)
                
                # exit_flag = False
                # while not exit_flag: 
                #     pyautogui.sleep(0.3)

                #     with Listener(on_click=saveOnClick) as listener:
                #         listener.join()


                txt += pointsDt
                txt += f"\nglColor3f{colorDataPolygon};\n"
                print( "Cantidad: " , countPoints)
                txt += f"glBegin({textForNum[countPoints-1] if (countPoints) < 5 else textForNum[4]});\n"

                for i in range(countPoints):
                    txt += f"\tglVertex2f{dta[i]};\n"
                txt += f"glEnd();\n\n"
    return txt
            
def tkDraw():
    botonSelect = tk.Button(app, text='Seleccionar archivo', command=btn_Clicked)
    botonSelect.pack()

def __main__():
    global app 
    # global exit_flag
    app = tk.Tk()
    

    app.geometry("400x300")
    app.title("PUNTFORMAT")
    tkDraw()

    app.mainloop()


if __name__ == "__main__":
    __main__()
