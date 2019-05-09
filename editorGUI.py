from tkinter import filedialog, Entry, Button, Label, IntVar
from tkinter import messagebox
from editor_console import *


def explorer():
    return filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("wav files", "*.wav"), ("all files", "*.*")))


def save_file(file):
    with open(file, "rb") as file:
        data = file.read()
    return data


def reverse_audio():
    """Разворачивает аудио
    Разворачивает данные,отвечающие за звук,возвращает перевенутое аудио
    """
    file = explorer()
    data = save_file(file)
    result = data[:44]
    array = bytearray(data[44:])
    list_chunks = []
    k = 44
    j = 48
    while j <= len(array):
        chunk = bytes(array[k:j])
        k = j
        j += 4
        list_chunks.append(chunk)
    list_chunks.reverse()
    for i in range(len(list_chunks)):
        result += list_chunks[i]
    answer = messagebox.askyesno(message="Сохранить в новый файл?")
    if answer:
        with open("reverse.wav", "wb") as file:
            file.write(result)
    else:
        with open(file, "wb") as file:
            file.truncate()
            file.seek(0)
            file.write(result)


def make_copy_audio():
    """Создает копию аудиофайла
    Записывает данные входящего аудио в новый файл
    """
    file = explorer()
    data = save_file(file)
    messagebox.showinfo(message="Будет создана копия")
    with open("copy.wav", "wb") as file:
        file.write(data)


def prepare_cut():
    how_much = IntVar()
    label = Label(text="На сколько вы хотите поделить аудио")
    label.place(relx=.4, rely=.5, anchor="c")
    entry = Entry(bg="#B0E0E6", textvariable=how_much)
    entry.place(relx=.5, rely=.5, anchor="c")
    btn = Button(text="Ok", bg="#B0E0E6", fg="#000000", padx="10", width=8, command=lambda: cut_audio(how_much.get(), label, entry, btn))
    btn.place(relx=.6, rely=.5, anchor="c")


def cut_audio(how_much, label, entry, button):
    """Записывает в новый файл часть входящего файла
    Отрезает от входящего аудио какую-то часть(работает пока только с целыми числами)
    и записывает в новый файл.На выходе получаем новое аудио, являющееся отрезком входящего
    """
    label.destroy()
    entry.destroy()
    button.destroy()
    file = explorer()
    data = FunctionForWav(save_file(file))
    size = data.extract_size()
    new_size = size // how_much
    result = b'RIFF'
    result += struct.pack('>L', new_size)
    result += data[8:40]
    bytes_region = data.extract_how_much_in_dataregion()
    new_bytes_region = bytes_region // how_much
    result += struct.pack('>L', new_bytes_region)
    data_wav = data[44:]
    result += data_wav[44: len(data_wav) // how_much]
    answer = messagebox.askyesno(message="Сохранить в новый файл?")
    if answer:
        with open("cut.wav", "wb") as file:
            file.write(result)
    else:
        with open(file, "wb") as file:
            file.truncate()
            file.seek(0)
            file.write(result)


def prepare_speed():
    sampling_frequency = IntVar()
    label = Label(text="Задайте частоту дискретизации для изменения скорости")
    label.place(relx=.4, rely=.5, anchor="c")
    entry = Entry(bg="#B0E0E6", textvariable=sampling_frequency)
    entry.place(relx=.5, rely=.5, anchor="c")
    btn = Button(text="Ok", bg="#B0E0E6", fg="#000000", padx="10", width=8, command=lambda: change_speed(sampling_frequency.get(), label, entry, btn))
    btn.place(relx=.6, rely=.5, anchor="c")


def change_speed(sampling_frequency, label, entry, button):
    """Меняет скорость аудио
    Меняет частоту дискретизации аудио, в результате скорость либо
    увеличивается,либо уменьшается
    """
    label.destroy()
    entry.destroy()
    button.destroy()
    file = explorer()
    data = FunctionForWav(save_file(file))
    result = data[:24]
    speed = struct.pack('l', int(sampling_frequency))
    result += speed
    result += data[28:]
    answer = messagebox.askyesno(message="Сохранить в новый файл?")
    if answer:
        with open("speed.wav", "wb") as file:
            file.write(result)
    else:
        with open(file, "wb") as file:
            file.truncate()
            file.seek(0)
            file.write(result)