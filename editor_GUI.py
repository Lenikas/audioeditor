from tkinter import filedialog, Entry, Button, Label, IntVar
from tkinter import messagebox
from editor_console import *


class FunctionForGUI:

    @staticmethod
    def create_result(result, list_data):
        for i in range(len(list_data)):
            result += list_data[i]
        return result

    @staticmethod
    def explorer():
        """Открывает диалоговое окно с выбором файла"""
        return filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("wav files", "*.wav"), ("all files", "*.*")))

    @staticmethod
    def destroy_elements(label, entry, button):
        """Удаляет ненужные графические элементы"""
        label.destroy()
        entry.destroy()
        button.destroy()

    @staticmethod
    def save_file(file):
        """Возвращает прочитанные из файла данные"""
        with open(file, "rb") as file:
            data = file.read()
        return data

    @staticmethod
    def reverse_audio():
        """
        Разворачивает аудио
            Разворачивает данные,отвечающие за звук,возвращает перевенутое аудио
        """
        file = FunctionForGUI.explorer()
        data = FunctionForGUI.save_file(file)
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

    @staticmethod
    def make_copy_audio():
        """
        Создает копию аудиофайла
            Записывает данные входящего аудио в новый файл
        """
        file = FunctionForGUI.explorer()
        data = FunctionForGUI.save_file(file)
        messagebox.showinfo(message="Будет создана копия")
        with open("copy.wav", "wb") as file:
            file.write(data)

    @staticmethod
    def prepare_cut():
        """Создает графические элементы для взаимодействия с пользователем и последующей обработки """
        how_much = IntVar()
        label = Label(text="На сколько вы хотите поделить аудио")
        label.place(relx=.4, rely=.5, anchor="c")
        entry = Entry(bg="#B0E0E6", textvariable=how_much)
        entry.place(relx=.5, rely=.5, anchor="c")
        btn = Button(text="Ok", bg="#B0E0E6", fg="#000000", padx="10", width=8, command=lambda: FunctionForGUI.cut_audio(how_much.get(), label, entry, btn))
        btn.place(relx=.6, rely=.5, anchor="c")

    @staticmethod
    def cut_audio(how_much, label, entry, button):
        """
        Записывает в новый файл часть входящего файла
            Отрезает от входящего аудио какую-то часть(работает пока только с целыми числами).
            На выходе получаем новое аудио, являющееся отрезком входящего
        """
        list_data = []
        result = b''
        FunctionForGUI.destroy_elements(label, entry, button)
        file = FunctionForGUI.explorer()
        data = FunctionForWav(FunctionForGUI.save_file(file))
        size = data.extract_size()
        new_size = size // how_much
        #   result = b'RIFF'
        list_data.append(b'RIFF')
        #   result += struct.pack('>L', new_size)
        list_data.append(struct.pack('>L', new_size))
        #   result += data[8:40]
        list_data.append(data[8:40])
        bytes_region = data.extract_how_much_in_dataregion()
        new_bytes_region = bytes_region // how_much
        #   result += struct.pack('>L', new_bytes_region)
        list_data.append(struct.pack('>L', new_bytes_region))
        data_wav = data[44:]
        #   result += data_wav[44: len(data_wav) // how_much]
        list_data.append(data_wav[44: len(data_wav) // how_much])
        result = FunctionForGUI.create_result(result, list_data)
        answer = messagebox.askyesno(message="Сохранить в новый файл?")
        if answer:
            with open("cut.wav", "wb") as file:
                file.write(result)
        else:
            with open(file, "wb") as file:
                file.truncate()
                file.seek(0)
                file.write(result)

    @staticmethod
    def prepare_speed():
        """Создает графические элементы для взаимодействия с пользователем и последующей обработки """
        sampling_frequency = IntVar()
        label = Label(text="Задайте частоту дискретизации для изменения скорости")
        label.place(relx=.35, rely=.5, anchor="c")
        entry = Entry(bg="#B0E0E6", textvariable=sampling_frequency)
        entry.place(relx=.5, rely=.5, anchor="c")
        btn = Button(text="Ok", bg="#B0E0E6", fg="#000000", padx="10", width=8, command=lambda: FunctionForGUI.change_speed(sampling_frequency.get(), label, entry, btn))
        btn.place(relx=.6, rely=.5, anchor="c")

    @staticmethod
    def change_speed(sampling_frequency, label, entry, button):
        """
        Меняет скорость аудио
            Меняет частоту дискретизации аудио, в результате скорость либо
            увеличивается,либо уменьшается
        """
        list_data = []
        result = b''
        FunctionForGUI.destroy_elements(label, entry, button)
        file = FunctionForGUI.explorer()
        data = FunctionForWav(FunctionForGUI.save_file(file))
        #   result = data[:24]
        list_data.append(data[:24])
        speed = struct.pack('l', int(sampling_frequency))
        #   result += speed
        list_data.append(speed)
        #   result += data[28:]
        list_data.append(data[28:])
        result = FunctionForGUI.create_result(result, list_data)
        answer = messagebox.askyesno(message="Сохранить в новый файл?")
        if answer:
            with open("speed.wav", "wb") as file:
                file.write(result)
        else:
            with open(file, "wb") as file:
                file.truncate()
                file.seek(0)
                file.write(result)

    @staticmethod
    def splice_audio():
        """
        Склеивает два аудио подряд
            Создает новый файл, являющийся склейкой двух входящих файлов,и записывает в него
            последовательно wav данные первого и второго аудио
        """
        list_data = []
        result = b''
        file_one = FunctionForGUI.explorer()
        file_two = FunctionForGUI.explorer()
        data_one = FunctionForWav(FunctionForGUI.save_file(file_one))
        data_two = FunctionForWav(FunctionForGUI.save_file(file_two))
        size_one = data_one.extract_size()
        size_two = data_two.extract_size()
        new_size = size_one + size_two
        #   result = b'RIFF'
        list_data.append(b'RIFF')
        #   result += struct.pack('>L', new_size)
        list_data.append(struct.pack('>L', new_size))
        #   result += data_one[8:40]
        list_data.append(data_one[8:40])
        bytes_region_one = data_one.extract_how_much_in_dataregion()
        bytes_region_two = data_two.extract_how_much_in_dataregion()
        new_bytes_region = bytes_region_one + bytes_region_two
        #   result += struct.pack('>L', new_bytes_region)
        list_data.append(struct.pack('>L', new_bytes_region))
        #   result += data_one[44:]
        list_data.append(data_one[44:])
        #   result += data_two[44:]
        list_data.append(data_two[44:])
        result = FunctionForGUI.create_result(result, list_data)
        messagebox.showinfo(message="Аудио будут склеены, будет создан новый файл")
        with open("splice.wav", "wb") as file:
            file.write(result)
