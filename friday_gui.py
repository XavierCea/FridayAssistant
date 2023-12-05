import friday_logic as friday
from tkinter import *
from PIL import Image, ImageTk

#GUI configuration
commands = """
    COMANDOS HABILITADOS:
    - Reproduce... [canción]
    - Busca... [algo]
    - Alarma... [hora en formato 24H]
    - Archivo... [nombre archivo]
    - Abre... [web/programa]
    - Escribe
    - Tiempo [Ubicación]
"""

root = Tk()
root.title("FRIDAY ASSISTANT")
root.iconbitmap('./assets/images/icon.ico')

root.geometry("800x200")
root.resizable(0,0)
root.configure(bg='#5300AB')

title = Label(root, text = "FRIDAY ASSISTANT", bg='#5300AB', fg="white", font=('Arial', 30, 'bold'))

title.pack(pady=10)
title.place(x=305, y=10)

canva_commands = Canvas(bg = '#410185', height=190, width=300)
canva_commands.place(x=0, y=0)

photo = PhotoImage(file = "./assets/images/audio_icon.png") 
photo = photo.subsample(10, 10)

listenBT = Button(root, text="Escuchar", image=photo, width=400, fg="white", bg="#00B4A2", font=("Arial", 15, "bold"), command=friday.run_friday)
listenBT.pack(pady=10)
listenBT.place(x=350, y=80)

canva_commands.create_text(140, 90, text=commands, fill="white", font='Arial 11')

root.mainloop()
