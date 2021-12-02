import unittest
import traceback
import compression
from arithmetic_coding import arithmetic_coding as ac

class Test_arithmetic_coding(unittest.TestCase):
    #
    #a basic test of my arithmetic coding algorithm
    #
    def test_arithmetic_coding():
        text="abbc"
        
        map=compression.compression.get_word_frequencies(text)
        print(ac.arithmetic_coding_algorithm(map))
        

if __name__ == '__main__':
   try:
       Test_arithmetic_coding.test_arithmetic_coding()

   except:
       traceback.print_exc()