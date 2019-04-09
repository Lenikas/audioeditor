#!/usr/bin/env python3
import sys
import wave
import struct



def speedup(audio, speed):
    """Возвращает ускоренное аудио
    Ускоряет указанное аудио в указанное количество раз(больше 1,замедления нет)
    """



def slowdown(audio):
    pass

def rewind():
    pass


def cut():
    """Возвращает кусок аудио
    Отрезает от указанного аудио первые length миллисекунд.
    """
    data_bytes = open(sys.argv[1], 'rb').read()
    print(data_bytes[-1])
    # проверка на работу



def splice(audio_one, audio_two):
    """Возвращает склейку
    Склеивает два аудио в один файл
    """


def helping():
    print("This is a audio editor")


def main():
    cut()


if __name__ == "__main__":
    main()
