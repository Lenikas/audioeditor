#!/usr/bin/env python3
# coding=utf-8
import struct
from main_console import *


class Information(bytes):
    #   вспомогательный класс для понимания структуры wav, в программе особо не задействован
    def extract_headers(self):
        """
        Возвращает информацию из заголовка
            Возвращает список из tuple, содержащий информацию об основных блоках
            заголовка, позиции(номера байта), с которой начинается блок, размера блока(не используется)
        """
        position = 12
        inf_chunks = []
        while position + 8 < len(self):
            chunk_id = self[position:position + 4]
            chunk_size = struct.unpack_from('<I', self[position + 4:position + 8])[0]
            inf_chunks.append((chunk_id, position, chunk_size))
            position += chunk_size + 8
            if chunk_id == b'data':
                break
        return inf_chunks

    def extract_size(self):
        """Возвращает размер файла в байтах"""
        return struct.unpack_from('<I', self[4: 8])[0] + 8

    def extract_format(self):
        """Возвращает параметр сжатия wav файла(не используется)"""
        return struct.unpack_from('<H', self[20: 22])[0]

    def extract_channels(self):
        """Вовзращает количество каналов wav файла(не используется)"""
        return struct.unpack_from('<H', self[22: 24])[0]

    def extract_sample_rate(self):
        """Возвращает частоту дискретизации wav файла в Гц(не используется)"""
        return struct.unpack_from('<I', self[24: 28])[0]

    def extract_bytes_in_second(self):
        """Возвращает количество байт, проигранных за секунду времени(не используется)"""
        return struct.unpack_from('<I', self[28: 32])[0]

    def extract_bytes_in_sample(self):
        """Возвращает количество байт, содержащихся в одном семпле(не используется)"""
        return struct.unpack_from('<H', self[32: 34])[0]

    def extract_bits_in_sample(self):
        """Возращает количество бит в семле, характеризующх глубину звучания(не используется)"""
        return struct.unpack_from('<H', self[34: 36])[0]

    def extract_how_much_in_dataregion(self):
        """Возвращает количество байт, отвечающих непосредственно за wav данные(не используется)"""
        return struct.unpack_from('<I', self[40: 44])[0]

    def extract_wavdata(self):
        """Возвращает блок wav данных в виде последовательности байт(не используется)"""
        return self[44:]

    def extract_information(self):
        """Возвращает основную информацию заголовка в виде списка(не используется)"""
        size = struct.unpack_from('<I', self[4: 8])[0] + 8
        audio_format = struct.unpack_from('<H', self[20: 22])[0]
        channels = struct.unpack_from('<H', self[22: 24])[0]
        sample_rate = struct.unpack_from('<I', self[24: 28])[0]
        byte_second = struct.unpack_from('<I', self[28: 32])[0]
        bytes_sample = struct.unpack_from('<H', self[32: 34])[0]
        bits_per_sample = struct.unpack_from('<H', self[34: 36])[0]
        bytes_data_region = struct.unpack_from('<I', self[40: 44])[0]
        audio_data = self[44:]
        return [size, audio_format, channels, sample_rate, byte_second, bytes_sample,
                bits_per_sample, bytes_data_region, audio_data]


class FunctionForWav(Information):

    @staticmethod
    def create_result(result, list_data):
        for i in range(len(list_data)):
            result += list_data[i]
        return result

    def change_speed(self, sampling_frequency):
        """
        Меняет скорость аудио
            Меняет частоту дискретизации аудио, в результате скорость либо
            увеличивается,либо уменьшается
        """
        list_data = []
        result = b""
        list_data.append(self[:24])
        #   result = self[:24]
        speed = struct.pack('l', int(sampling_frequency))
        list_data.append(speed)
        #   result += speed
        list_data.append(self[28:])
        # result += self[28:]
        result = FunctionForWav.create_result(result, list_data)
        return result

    def reverse_audio(self):
        """
        Разворачивает аудио
            Разворачивает данные,отвечающие за звук,возвращает перевенутое аудио
        """
        result = self[:44]
        array = bytearray(self[44:])
        list_chunks = []
        k = 44
        j = 48
        while j <= len(array):
            chunk = bytes(array[k:j])
            k = j
            j += 4
            list_chunks.append(chunk)
            print(chunk)
        list_chunks.reverse()
        for i in range(len(list_chunks)):
            result += list_chunks[i]
        return result

    def create_any_channels(self, count_channels):
        """
        Изменяет количество каналов
            Возвращает аудио с измененным в количество каналов звучанием
        """
        list_data = []
        result = b''
        #   result = self[:22]
        list_data.append(self[:22])
        new_channels = int(count_channels)
        #   result += struct.pack('>H', new_channels)
        list_data.append(struct.pack('>H', new_channels))
        #   result += self[24:]
        list_data.append(self[24:])
        result = FunctionForWav.create_result(result, list_data)
        return result

    def make_copy_audio(self):
        """
        Создает копию аудиофайла
            Записывает данные входящего аудио в новый файл
        """
        return self

    def cut_audio(self, how_much):
        """
        Записывает в новый файл часть входящего файла
            Отрезает от входящего аудио какую-то часть(работает пока только с целыми числами).
            На выходе получаем новое аудио, являющееся отрезком входящего
        """
        list_data = []
        result = b''
        how_much = int(how_much)
        size = self.extract_size()
        new_size = size // how_much
        list_data.append(b'RIFF')
        #    result = b'RIFF'
        #    result += struct.pack('>L', new_size)
        list_data.append(struct.pack('>L', new_size))
        #   result += self[8:40]
        list_data.append(self[8:40])
        bytes_region = self.extract_how_much_in_dataregion()
        new_bytes_region = bytes_region // how_much
        #   result += struct.pack('>L', new_bytes_region)
        list_data.append(struct.pack('>L', new_bytes_region))
        data_wav = self[44:]
        #   result += data_wav[44: len(data_wav) // how_much]
        list_data.append(data_wav[44: len(data_wav) // how_much])
        result = FunctionForWav.create_result(result, list_data)
        return result

    def splice_audio(self, second):
        """
        Склеивает два аудио подряд
            Создает новый файл, являющийся склейкой двух входящих файлов,и записывает в него
            последовательно wav данные первого и второго аудио
        """
        list_data = []
        result = b''
        size_one = self.extract_size()
        size_two = second.extract_size()
        new_size = size_one + size_two
        #   result = b'RIFF'
        list_data.append(b'RIFF')
        #   result += struct.pack('>L', new_size)
        list_data.append(struct.pack('>L', new_size))
        #   result += self[8:40]
        list_data.append(self[8:40])
        bytes_region_one = self.extract_how_much_in_dataregion()
        bytes_region_two = second.extract_how_much_in_dataregion()
        new_bytes_region = bytes_region_one + bytes_region_two
        #   result += struct.pack('>L', new_bytes_region)
        list_data.append(struct.pack('>L', new_bytes_region))
        #   result += self[44:]
        list_data.append( self[44:])
        #   result += second[44:]
        list_data.append(second[44:])
        result = FunctionForWav.create_result(result, list_data)
        return result


if __name__ == "__main__":
    main()
