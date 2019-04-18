import argparse
import sys
from editor import *


def parse_args():
    """Разбор аргументов запуска"""
    parser = argparse.ArgumentParser(description="Edit wav")
    parser.add_argument('--cut', nargs=2)
    parser.add_argument('--copy', nargs=1)
    parser.add_argument('--splice', nargs=2)
    parser.add_argument('--edit_channels', nargs=2)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.cut:
        cut_audio(sys.argv[2], sys.argv[3])
    if args.copy:
        make_copy_audio(sys.argv[2])
    if args.splice:
        splice_audio(sys.argv[2], sys.argv[3])
    if args.edit_channels:
        create_any_channels(sys.argv[2], sys.argv[3])

