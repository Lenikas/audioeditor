#!/usr/bin/env python3
# coding=utf-8
import sys
import struct


def extract_headers(data):
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
    return struct.unpack_from('<I', data[4: 8])[0] + 8


def extract_format(data):
    return struct.unpack_from('<H', data[20: 22])[0]


def extract_channels(data):
    return struct.unpack_from('<H', data[22: 24])[0]


def extract_sample_rate(data):
    return struct.unpack_from('<I', data[24: 28])[0]


def extract_bytes_in_second(data):
    return struct.unpack_from('<I', data[28: 32])[0]


def extract_bytes_in_sample(data):
    return struct.unpack_from('<H', data[32: 34])[0]


def extract_bits_in_sample(data):
    return struct.unpack_from('<H', data[34: 36])[0]


def extract_how_much_in_dataregion(data):
    return struct.unpack_from('<I', data[40: 44])[0]


def extract_wavdata(data):
    return data[44:]


def extract_information(data):
    size = struct.unpack_from('<I', data[4: 8])[0] + 8
    audio_format = struct.unpack_from('<H', data[20: 22])[0]
    channels = struct.unpack_from('<H', data[22: 24])[0]
    sample_rate = struct.unpack_from('<I', data[24: 28])[0]
    byte_second = struct.unpack_from('<I', data[28: 32])[0]
    bytes_sample = struct.unpack_from('<H', data[32: 34])[0]
    bits_per_sample = struct.unpack_from('<H', data[34: 36])[0]
    bytes_data_region = struct.unpack_from('<I', data[40: 44])[0]
    audio_data = data[44:]
    #  print(size, audio_format, channels, sample_rate, byte_second, bytes_sample, bits_per_sample, bytes_data_region)
    return [size, audio_format, channels, sample_rate, byte_second, bytes_sample, bits_per_sample, bytes_data_region, audio_data]


def make_copy_audio(data):
    with open('сopy.wav', 'wb') as file:
        file.write(data)
    return file


def cut_audio(data):
    size = extract_size(data)
    new_size = size // 2
    result = b'RIFF'
    result += struct.pack('>L', new_size)
    result += data[8:40]
    bytes_region= extract_how_much_in_dataregion(data)
    new_bytes_region = bytes_region // 2
    result += struct.pack('>L', new_bytes_region)
    data_wav = data[44:]
    new_data_wav = data_wav[44: len(data_wav) // 2]
    result += new_data_wav
    return result



def splice_audio(data_one, data_two):
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
    return result


def main():
    file_one = open(sys.argv[1], 'rb')
    data_one = file_one.read()
    result = cut_audio(data_one)
    with open('cut.wav', 'wb') as file:
        file.write(result)
    return file



if __name__ == "__main__":
    main()