from editor_console import *
import argparse


def parse_args():
    """Разбор аргументов запуска"""
    parser = argparse.ArgumentParser(description="Edit wav")
    parser.add_argument('--cut', nargs=3, help=FunctionForWav.cut_audio.__doc__)
    parser.add_argument('--copy', nargs=1, help=FunctionForWav.make_copy_audio.__doc__)
    parser.add_argument('--splice', nargs=2, help=FunctionForWav.splice_audio.__doc__)
    #   parser.add_argument('--edit_channels', nargs=2, help=FunctionForWav.create_any_channels.__doc__)
    parser.add_argument('--reverse', nargs=2, help=FunctionForWav.reverse_audio.__doc__)
    parser.add_argument('--speed', nargs=3, help=FunctionForWav.change_speed.__doc__)
    return parser.parse_args()


def write_in_this(args, data):
    file_for_write = args[1]
    with open(file_for_write, "rb+") as file:
        file.truncate()
        file.seek(0)
        file.write(data)


def process_cut(args):
    file_for_work = args[1]
    num_for_cut = args[2]
    key_which_file = args[0]
    with open(file_for_work, "rb") as file:
        data = FunctionForWav(file.read())
        # # result = data[:36]
        # # result += data[70:]
        # # result = FunctionForWav(result)
        # print(FunctionForWav(data).extract_headers())
        # print(data[20:22])
    cut_data = data.cut_audio(num_for_cut)
    if key_which_file == 'new':
        with open("cut_audio.wav", 'wb') as file:
            file.write(cut_data)
    elif key_which_file == 'this':
        write_in_this(args, cut_data)


def process_splice(args):
    file_for_work1 = args[0]
    file_for_work2 = args[1]
    with open(file_for_work1, "rb") as file:
        data_one = FunctionForWav(file.read())
    with open(file_for_work2, "rb") as file:
        data_two = FunctionForWav(file.read())
    with open("splice_audio.wav", 'wb') as file:
        file.write(data_one.splice_audio(data_two))


def process_copy(args):
    file_for_work = args[0]
    with open(file_for_work, 'rb') as file:
        data = FunctionForWav(file.read())
    with open("copy_audio.wav", 'wb') as file:
        file.write(data)


def process_reverse(args):
    file_for_work = args[1]
    key_which_file = args[0]
    with open(file_for_work, "rb") as file:
        data = FunctionForWav(file.read())
        # result = data[:36]
        # result += data[70:]
        # result = FunctionForWav(result)
    reverse_data = data.reverse_audio()
    if key_which_file == 'new':
        with open("reverse_audio.wav", 'wb') as file:
            file.write(reverse_data)
    elif key_which_file == 'this':
        write_in_this(args, reverse_data)


def process_speed(args):
    file_for_work = args[1]
    key_which_file = args[0]
    with open(file_for_work, "rb") as file:
        data = FunctionForWav(file.read())
    speed_data = data.change_speed(args[2])
    if key_which_file == 'new':
        with open("speed.wav", 'wb') as file:
            file.write(speed_data)
    elif key_which_file == 'this':
        write_in_this(args, speed_data)


def main():
    args = parse_args()
    if args.cut:
        process_cut(args.cut)
    elif args.copy:
        process_copy(args.copy)
    elif args.splice:
        process_splice(args.splice)
    elif args.reverse:
        process_reverse(args.reverse)
    elif args.speed:
        process_speed(args.speed)
    else:
        print('ERROR')
    # if args.cut:
    #     with open(args.cut[1], "rb") as file:
    #         data = FunctionForWav(file.read())
    #     if args.cut[0] == 'new':
    #         with open("cut_audio.wav", 'wb') as file:
    #             file.write(data.cut_audio(args.cut[2]))
    #     elif args.cut[0] == 'this':
    #         with open(args.cut[1], "rb+") as file:
    #             data = data.cut_audio(args.cut[2])
    #             file.truncate()
    #             file.seek(0)
    #             file.write(data)
    #     else:
    #         print('unknown command')
