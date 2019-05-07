import unittest
import os
from editor import *

class TestDataMethods(unittest.TestCase):


    def test_size(self):
        with open(r"C:\Users\Леня\Desktop\audioeditor\coincidence.wav", "rb") as file:
            data1 = file.read()
        size_os = os.path.getsize(r"C:\Users\Леня\Desktop\audioeditor\coincidence.wav")
        self.assertEqual(FunctionForWav(data1).extract_size(), size_os)

if __name__ == '__main__':
    unittest.main()