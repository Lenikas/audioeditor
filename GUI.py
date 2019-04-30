from tkinter import *
from tkinter import filedialog, constants
from editor import FunctionForWav



root = Tk()
root.title("Audio Editor")
root.wm_state("zoomed")
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("wav files","*.wav"),("all files","*.*")))
#root.filename1 = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("wav files","*.wav"),("all files","*.*")))
with open(root.filename, 'rb') as file:
    data= FunctionForWav(file.read())
btn_cut = Button(text="Резка", bg="#FF4500", fg="#000000", padx="10", command=data.cut_audio(2))
btn_cut.place(relx=.5, rely=.99, anchor="c", bordermode=OUTSIDE)


root.mainloop()
