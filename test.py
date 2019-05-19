import os
import unittest
from editor_console import FunctionForWav
import pydub
import struct

path = os.path.join(os.path.dirname(__file__), 'coincidence.wav')
with open(path, "rb") as file:
    data_for_test = file.read()
audio_pydub = pydub.AudioSegment(data_for_test)


class TestInformationMethods(unittest.TestCase):

    def test_size(self):
        size_expected = os.path.getsize(path)
        size_actual = FunctionForWav(data_for_test).extract_size()
        self.assertEqual(size_actual, size_expected)

    def test_count_channels(self):
        channels_expected = audio_pydub.channels
        channels_actual = FunctionForWav(data_for_test).extract_channels()
        self.assertEqual(channels_actual, channels_expected)

    def test_sample_rate(self):
        sample_rate_expected = audio_pydub.frame_rate
        sample_rate_actual = FunctionForWav(data_for_test).extract_sample_rate()
        self.assertEqual(sample_rate_actual, sample_rate_expected)

    def test_format(self):
        format_expected = struct.unpack_from('<H', data_for_test[20: 22])[0]
        format_actual = FunctionForWav(data_for_test).extract_format()
        self.assertEqual(format_actual, format_expected)

    def test_bytes_sample(self):
        byte_expected = audio_pydub.sample_width
        byte_actual = FunctionForWav(data_for_test).extract_bytes_in_sample()
        self.assertEqual(byte_actual, byte_expected)



if __name__ == '__main__':
    unittest.main()
