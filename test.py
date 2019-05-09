import unittest
import os
from editor_console import *

class TestDataMethods(unittest.TestCase):
    #r"C:\Users\Леня\Desktop\audioeditor\coincidence.wav"
    def test_size(self):
        with open(r"C:\Users\1\Desktop\editor\audioeditor\arguing.wav", "rb") as file:
            data1 = file.read()
        size_os = os.path.getsize(r"C:\Users\1\Desktop\editor\audioeditor\arguing.wav")
        self.assertEqual(FunctionForWav(data1).extract_size(), size_os)

if __name__ == '__main__':
    unittest.main()