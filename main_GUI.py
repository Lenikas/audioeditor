from tkinter import *
from editor_GUI import FunctionForGUI


root = Tk()
root["bg"] = "#FFFFFF"
root.title("Audio Editor")
root.wm_state("zoomed")

btn_expl = Button(text="Обзор", bg="#B0E0E6", fg="#000000", padx="10", width=8,  command=FunctionForGUI.explorer)
btn_expl.place(relx=.45, rely=.99, anchor="c")

btn_cut = Button(text="Резка", bg="#B0E0E6", fg="#000000", padx="10", width=8, command=FunctionForGUI.prepare_cut)
btn_cut.place(relx=.49, rely=.99, anchor="c")

btn_splice = Button(text="Склейка", bg="#B0E0E6", fg="#000000", padx="10", width=8, command=FunctionForGUI.splice_audio)
btn_splice.place(relx=.53, rely=.99, anchor="c")

btn_rvrs = Button(text="Разворот", bg="#B0E0E6", fg="#000000", padx="10", width=8, command=FunctionForGUI.reverse_audio)
btn_rvrs.place(relx=.57, rely=.99, anchor="c")

btn_spd = Button(text="Скорость", bg="#B0E0E6", fg="#000000", padx="10", width=8, command=FunctionForGUI.prepare_speed)
btn_spd.place(relx=.61, rely=.99, anchor="c")

btn_cp = Button(text="Сделать копию", bg="#B0E0E6", fg="#000000", padx="10", width=10, command=FunctionForGUI.make_copy_audio)
btn_cp.place(relx=.655, rely=.99, anchor="c")
root.mainloop()




