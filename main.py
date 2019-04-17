import argparse
from editor import *

def parse_args():
    """Разбор аргументов запуска"""
    parser = argparse.ArgumentParser()
    return parser.parse_args()


def main():


    if sys.argv[1] == 'cut':
        data = read_file(sys.argv[3])
        len_cut = int(sys.argv[2])
        cut_audio(data, len_cut)
    if sys.argv[1] == 'splice':
        data = read_two_files(sys.argv[2], sys.argv[3])
        splice_audio(data[0], data[1])