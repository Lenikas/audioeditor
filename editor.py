#!/usr/bin/env python3
# coding=utf-8
import sys
import struct


def extract_headers(data):
    """Возвращает информацию из заголовка
    Возвращает список из tuple, содержащий информацию об основных блоках
    заголовка, позиции(номера байта), с которой начинается блок, размера блока
    """
    position = 12
    inf_chunks = []
    while position + 8 < len(data):
        chunk_id = data[position:position + 4]
        chunk_size = struct.unpack_from('<I', data[position + 4:position + 8])[0]
        inf_chunks.append((chunk_id, position, chunk_size))
        position += chunk_size + 8
        if chunk_id == b'data':
            break
    print(inf_chunks)
    return inf_chunks
#proverka

def extract_size(data):
    """Возвращает размер файла в байтах"""
    return struct.unpack_from('<I', data[4: 8])[0] + 8


def extract_format(data):
    """Возвращает параметр сжатия wav файла"""
    return struct.unpack_from('<H', data[20: 22])[0]


def extract_channels(data):
    """Вовзращает количество каналов wav файла"""
    return struct.unpack_from('<H', data[22: 24])[0]


def extract_sample_rate(data):
    """Возвращает частоту дискретизации wav файла в Гц"""
    return struct.unpack_from('<I', data[24: 28])[0]


def extract_bytes_in_second(data):
    """Возвращает количество байт, проигранных за секунду времени"""
    return struct.unpack_from('<I', data[28: 32])[0]


def extract_bytes_in_sample(data):
    """Возвращает количество байт, содержащихся в одном семпле"""
    return struct.unpack_from('<H', data[32: 34])[0]


def extract_bits_in_sample(data):
    """Возращает количество бит в семле, характеризующх глубину звучания"""
    return struct.unpack_from('<H', data[34: 36])[0]


def extract_how_much_in_dataregion(data):
    """Возвращает количество байт, отвечающих непосредственно за wav данные"""
    return struct.unpack_from('<I', data[40: 44])[0]


def extract_wavdata(data):
    """Возвращает блок wav данных в виде последовательности байт"""
    return data[44:]


def extract_information(data):
    """Возвращает основную информацию заголовка в виде списка"""
    size = struct.unpack_from('<I', data[4: 8])[0] + 8
    audio_format = struct.unpack_from('<H', data[20: 22])[0]
    channels = struct.unpack_from('<H', data[22: 24])[0]
    sample_rate = struct.unpack_from('<I', data[24: 28])[0]
    byte_second = struct.unpack_from('<I', data[28: 32])[0]
    bytes_sample = struct.unpack_from('<H', data[32: 34])[0]
    bits_per_sample = struct.unpack_from('<H', data[34: 36])[0]
    bytes_data_region = struct.unpack_from('<I', data[40: 44])[0]
    audio_data = data[44:]
    #   print(size, audio_format, channels, sample_rate, byte_second, bytes_sample, bits_per_sample, bytes_data_region)
    return [size, audio_format, channels, sample_rate, byte_second, bytes_sample, bits_per_sample, bytes_data_region, audio_data]


def read_file(file):
    """Возвращает данные, прочитанные из поступившего файла"""
    opened_file = open(file, 'rb')
    data = opened_file.read()
    opened_file.close()
    return data


def read_two_files(file_one, file_two):
    """Возвращает данные из двух прочитанных файлов в виде tuple """
    opened_one = open(file_one, 'rb')
    opened_two = open(file_two, 'rb')
    data_one = opened_one.read()
    data_two = opened_two.read()
    opened_one.close()
    opened_two.close()
    return data_one,data_two


def reverse_audio(data):
    """не работает,в результате шум"""
    result = data[:44]
    rev = bytes(reversed(data[44:]))
    result += rev
    with open('reverse.wav', 'wb') as file:
        file.write(result)


def create_any_channels(data, count_channels):
    result = data[:22]
    new_channels = count_channels
    result += struct.pack('>H', new_channels)
    result += data[24:]
    with open('in_any_channels.wav', 'wb') as file:
        file.write(result)



def make_copy_audio(data):
    """Создает копию аудиофайла
    Записывает данные входящего аудио в новый файл
    """
    with open('сopy.wav', 'wb') as file:
        file.write(data)



def cut_audio(data, how_much):
    """Записывает в новый файл часть входящего файла
    Отрезает от входящего аудио какую-то часть(работает пока только с целыми числами)
    и записывает в новый файл.На выходе получаем новое аудио, являющееся отрезком входящего
    """
    size = extract_size(data)
    new_size = size // how_much
    result = b'RIFF'
    result += struct.pack('>L', new_size)
    result += data[8:40]
    bytes_region= extract_how_much_in_dataregion(data)
    new_bytes_region = bytes_region // how_much
    result += struct.pack('>L', new_bytes_region)
    data_wav = data[44:]
    new_data_wav = data_wav[44: len(data_wav) // how_much]
    result += new_data_wav
    with open('сut.wav', 'wb') as file:
        file.write(result)


def splice_audio(data_one, data_two):
    """Склеивает два аудио подряд
    Создает новый файл, являющийся склейкой двух входящих файлов,и записывает в него
    последовательно wav данные первого и второго аудио
    """
    size_one = extract_size(data_one)
    size_two = extract_size(data_two)
    new_size = size_one + size_two
    result = b'RIFF'
    result += struct.pack('>L',new_size)
    result += data_one[8:40]
    bytes_region_one = extract_how_much_in_dataregion(data_one)
    bytes_region_two = extract_how_much_in_dataregion(data_two)
    new_bytes_region = bytes_region_one + bytes_region_two
    result += struct.pack('>L', new_bytes_region)
    result += data_one[44:]
    result += data_two[44:]
    with open('splice.wav', 'wb') as file:
        file.write(result)


def main():
    if sys.argv[1] == 'cut':
        data = read_file(sys.argv[3])
        len_cut = int(sys.argv[2])
        cut_audio(data, len_cut)
    if sys.argv[1] == 'splice':
        data = read_two_files(sys.argv[2], sys.argv[3])
        splice_audio(data[0], data[1])




if __name__ == "__main__":
    main()