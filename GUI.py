from tkinter import *
from tkinter import filedialog, constants
from editor import FunctionForWav
import struct


def explorer():
    return filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("wav files","*.wav"),("all files","*.*")))


def save_file():
    file = explorer()
    with open(file, "rb") as file:
        data = file.read()
    return data


def cut_audio(how_much):
    """Записывает в новый файл часть входящего файла
    Отрезает от входящего аудио какую-то часть(работает пока только с целыми числами)
    и записывает в новый файл.На выходе получаем новое аудио, являющееся отрезком входящего
    """
    data = FunctionForWav(save_file())
    how_much = int(how_much)
    size = data.extract_size()
    new_size = size // 2
    result = b'RIFF'
    result += struct.pack('>L', new_size)
    result += data[8:40]
    bytes_region = data.extract_how_much_in_dataregion()
    new_bytes_region = bytes_region // 2
    result += struct.pack('>L', new_bytes_region)
    data_wav = data[44:]
    result += data_wav[44: len(data_wav) // 2]
    with open("Cut", "wb") as file:
        file.write(result)
    return result


root = Tk()
root["bg"] = "#FFFFFF"
root.title("Audio Editor")
root.wm_state("zoomed")

btn_expl = Button(text="Обзор", bg="#B0E0E6", fg="#000000", padx="10", width = 8,  command=save_file)
btn_expl.place(relx=.488, rely=.99, anchor="c", bordermode=OUTSIDE)

btn_cut = Button(text="Резка", bg="#B0E0E6", fg="#000000", padx="10", width = 8, command=cut_audio)
btn_cut.place(relx=.54, rely=.99, anchor="c", bordermode=OUTSIDE)

btn_splice = Button(text="Склейка", bg="#B0E0E6", fg="#000000", padx="10", width = 8)
btn_splice.place(relx=.59, rely=.99, anchor="c", bordermode=OUTSIDE)
root.mainloop()




