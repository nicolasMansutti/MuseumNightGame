#aca ponemos bonito el codigo y la ventana
import customtkinter
from tkinter import *

import time
import random
import simpleaudio as sa
import chardet
#import filtro_md
from typing import Final

#variables globales-->
ANCHO: Final = 800
LARGO: Final = 400
FILE1: Final = "archivo.txt"
FILE2: Final = "arch_lvl2.txt"
FILE3: Final = "arch_lvl3.txt"
VELOCIDAD: Final = 800 
LIMITE_DERECHO: Final = ANCHO 
ULTIMO_TIEMPO: Final= time.perf_counter()
#---------------------------------------------------------------------------
#datos del archivo
def open_file(file_to_open):
    try:
        with open(file_to_open, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]
        file= open(file_to_open, "r", encoding=encoding)
        return file
    except Exception as e:
        print("File Not Found")
        return None

def read_from_file(current_lvl):
    file = None
    match(current_lvl):
        case 1:
            file = open_file(FILE1)
        case 2:
            file = open_file(FILE2)
        case 3:
            file = open_file(FILE3)
        case _:
            pass
    
    if file is None: return -1 
    
    file_data= file.readlines()
    file.close()

    total_Q=int(file_data[0])
    del file_data[0]

    q= random.randint(1, total_Q) 
    q= str(q)

    global questions
    questions= file_data[file_data.index(q+"\n")+1: file_data.index("*"+q+"*\n")]
    if current_lvl == 2 and len(questions) < 5: return -1

    global botones
    botones=[1,2,3]
    random.shuffle(botones)
    return 0

#---------------------------------------------------------------------------
#funciones de movimiento y cambio de color
def anim_on_x_or_y(character, x=False, y=False, nest_func=None):
    
        global ULTIMO_TIEMPO
        ahora = time.perf_counter()
        delta = 0.01
        ULTIMO_TIEMPO = ahora

        # Movimiento basado en tiempo real
        mov_x = VELOCIDAD * delta if x else 0
        mov_y = VELOCIDAD * delta if y else 0
        canvas.move(character, mov_x, mov_y) 

        # Verificar límite
        _, x2 = canvas.coords(character)
        if x2 < LIMITE_DERECHO:
            # Volver a llamar (no bloqueante)
            canvas.after(16, lambda: anim_on_x_or_y( character, x= x, y= y, nest_func= nest_func))
        elif nest_func:
            canvas.after(16, nest_func)
            # Ajustar posición final exacta
            
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
def botones_accion(lvl):
    global boton
    global boton2
    global boton3

    if(lvl>1):
        boton.pack_forget()
        boton2.pack_forget()
        boton3.pack_forget()

    boton= customtkinter.CTkButton(window, text= questions[botones[0]],
                               corner_radius=20, font=("Helvetica", 24),
                               width=10000,
                               command= lambda: nex_lvl(lvl, botones[0]==3))

    boton.pack(side= "bottom", pady=10, padx=40)
     
    boton2= customtkinter.CTkButton(window, text= questions[botones[1]],
                               corner_radius=20, font=("Helvetica", 24),
                               width=10000,
                               command= lambda: nex_lvl(lvl, botones[1]==3))
    boton2.pack(side= "bottom", pady=0, padx=40)
     
    boton3= customtkinter.CTkButton(window, text= questions[botones[2]],
                               corner_radius=20, font=("Helvetica", 24),
                               width=10000,
                               command= lambda: nex_lvl(lvl, botones[2]==3))
    boton3.pack(side= "bottom", pady=10, padx=40)
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
def music(sound, nest_func=None):
    musica = sa.WaveObject.from_wave_file(sound)
    play = musica.play()
    if nest_func:
        canvas.after(2000, nest_func)
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
def lose_anim(offset=0):
    anim_on_x_or_y(snd_pers, x=True)
    window.after(300+offset, lambda: music("knife.wav"))
    window.after(510+offset, lambda: anim_on_x_or_y(main_c_img, y=True))
    win_msg= canvas.create_text(470,70,
                            text= "YOU LOSE",
                            font=("Helvetica", 25),
                            fill="black")
    window.update()
    window.after(1500+offset, lambda: music("Generic.wav"))
    boton.pack_forget()
    boton2.pack_forget()
    boton3.pack_forget()
    window.after(4000+offset, window.destroy)

#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
def lvl_mensage(current_lvl):
    lvl_msg= canvas.create_text(400,75,
                            text= "level " + str(current_lvl+1),
                            font=("Helvetica", 20),
                            fill="black")
    x=10
    while(x<70):
        canvas.move(lvl_msg,x,25)
        window.update()
        time.sleep(0.45)
        canvas.move(lvl_msg,x+1,25+190)
        x= x + 10
    canvas.delete(lvl_msg)

#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
def pregunta(lvl):
    global preg
    if(lvl>1): preg.pack_forget()
    preg= Label(window, text=questions[0], bg="black", fg="white",
                     bd=5,
                     height=2, width=100, font=("Helvetica",20))
    preg.pack()
    
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
def deadth_moves(lvl):
    if(lvl != 3 ): canvas.move(snd_pers,-300,0)
    else: canvas.move(snd_pers,-200,0)
    window.update()
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
def dialogo(lvl, perdiste= False): 
    global dial 
    if(lvl==2 and not perdiste):
        dial= canvas.create_text(500,80,
              text= questions[4],
              font=("Helvetica", 20, "italic"),
              fill="black",
             )
        #aca es donde esta la magia de lo que va escrito
    elif (perdiste and lvl==2) or lvl>2:
        canvas.delete(dial)
    window.update()
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
def set_lvl(lvl): 
    if read_from_file(lvl) == -1 : 
        window.destroy()
        return -1
    pregunta(lvl)
    #aca prodira ser algo como tirar la moneda de si hacemos timer o no
    # hay que ver que no sea el nivel 2 para el timer
    # en botones_accion hay que pasarle si hubo timer o no, de manera que
    # si  lo muestra
    # si no, no lo hace
    if lvl == 3:
        is_timer= random.randint(0,1)
        #en maun hay un ejemplo de como hacer el temporizador

    botones_accion(lvl)
    if lvl != 1:
        deadth_moves(lvl) 
        dialogo(lvl)
    window.update()
    return 0
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
def end_scene(): #TODO sacar sleep y ver como el de perder
    anim_on_x_or_y(snd_pers, y=True)
    window.after(90, lambda: music("tada.wav"))
    win_msg= canvas.create_text(470,70,
                            text= "YOU WIN",
                            font=("Helvetica", 25),
                            fill="black")

    boton.pack_forget()
    boton2.pack_forget()
    boton3.pack_forget()
    window.after(1510, window.destroy)


#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --     
def nex_lvl(current_lvl, is_correct):
    if(current_lvl==3 and is_correct):
        end_scene()
    elif(is_correct):
        lvl_mensage(current_lvl)
        set_lvl(current_lvl+1)
    else:
        dialogo(current_lvl, perdiste= True)
        offset=0
        if current_lvl > 1: 
            offset=500 if current_lvl==2 else 900
        lose_anim(offset=offset)
#------------------------------------------------------------------------

#main-->       
def main():
    #crear la ventana
    global window
    global canvas
    global preg


    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    
    window= customtkinter.CTk()
    window.title("Primer intento")
    window.geometry("1024x700")
    canvas= Canvas(window, width= ANCHO, height= LARGO, bg="black")
    canvas.pack(fill="both", expand=False, padx=50)
    
    #-----------------------------------------------------------------------
    #poner la imagen en el widget canvas-->

    global main_character
    global main_c_img
    global dead_charcater
    global snd_pers

    fondo= PhotoImage(file="fondo_fondo.png")
    fondo_img= canvas.create_image(0,0, image=fondo, anchor= NW)
    
    main_character= PhotoImage(file="fondo_personaje.png")
    main_c_img= canvas.create_image(796,213, image= main_character)
    
    dead_charcater= PhotoImage(file="fondo_muerte.png")
    snd_pers= canvas.create_image(490,168, image=dead_charcater, anchor= NW)
    #-------------------------------------------------------------------------
    #botones con funciones-->
    
    set_lvl(1)
    window.mainloop()
#---------------------------------------------------------------------------



if __name__=='__main__':
    main()
