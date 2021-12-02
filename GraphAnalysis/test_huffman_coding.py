import unittest
import compression
import traceback
from dahuffman import HuffmanCodec as codec
class Test_huffman_coding(unittest.TestCase):
    #
    #A basic test of the huffman coding algorithm I had written
    #
    def test_compression():
        text=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        map=compression.compression.get_word_frequencies(text)
        tree=compression.compression.compress_from_frequencies(map)
        print(tree.costs)
    #
    #another basic test this time with a longer text
    #
    def test_big_compression():
        text=""
        with open('markTwain\\frog.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        map=compression.compression.get_word_frequencies(text)
        print(map)
        tree=compression.compression.compress_from_frequencies(map)
        print(tree.costs)
    #
    #This takes the mark twain short story and tests compressing the sample text file using the 
    #compression tree from the short story
    #
    def test_compression_comparison():
        text=""
        with open('markTwain\\frog.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        map=compression.compression.get_word_frequencies(text)
        tree=compression.compression.compress_from_frequencies(map)
        text2=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text2=text2+line
        print(tree.get_cost_of_text(text2))
    #
    #This uses huffman coding to try to see if we can differentiate between works by twain and ohenry
    #
    def  compare_twain_henry_press():
        text_frog=""
        with open('markTwain\\frog.txt', 'r') as reader:
            for line in reader.readlines():
                text_frog=text_frog+line
        text_barber=""
        with open('markTwain\\barber.txt', 'r') as reader:
            for line in reader.readlines():
                text_barber=text_barber+line
        text_dup=""
        with open('ohenry\\duplicityohargraves.txt', 'r') as reader:
            for line in reader.readlines():
                text_dup=text_dup+line
        text_gift=""
        with open('ohenry\\giftofthemagi.txt', 'r') as reader:
            for line in reader.readlines():
                text_gift=text_gift+line
        tree_frog=compression.compression.compress_from_frequencies(compression.compression.get_word_frequencies(text_frog))
        tree_barber=compression.compression.compress_from_frequencies(compression.compression.get_word_frequencies(text_barber))
        tree_dup=compression.compression.compress_from_frequencies(compression.compression.get_word_frequencies(text_dup))
        tree_gift=compression.compression.compress_from_frequencies(compression.compression.get_word_frequencies(text_gift))
        print("twain on twain"+str(tree_frog.get_cost_of_text(text_barber)))
        print("henry on twain"+str(tree_dup.get_cost_of_text(text_barber)))
        print("henry on twain"+str(tree_gift.get_cost_of_text(text_barber)))
        print("twain on henry"+str(tree_frog.get_cost_of_text(text_dup)))
        print("twain on henry"+str(tree_barber.get_cost_of_text(text_dup)))
        print("henry on henry"+str(tree_gift.get_cost_of_text(text_dup)))
        print("twain on henry"+str(tree_frog.get_cost_of_text(text_gift)))              
        print("twain on henry"+str(tree_barber.get_cost_of_text(text_gift)))
        print("henry on henry"+str(tree_dup.get_cost_of_text(text_gift)))
        print("henry on twain"+str(tree_dup.get_cost_of_text(text_frog)))        
        print("twain on twain"+str(tree_barber.get_cost_of_text(text_frog)))
        print("henry on twain"+str(tree_gift.get_cost_of_text(text_frog)))
    def test_huffman_library():
        text=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        coded=codec.from_frequencies(compression.compression.get_word_frequencies(text))
        print(coded.get_code_table())
    def test_huffman_mathmatically():
        text="aaabbbc"
        map=compression.compression.get_character_frequencies(text)
        print(map)
        tree=compression.compression.compress_from_frequencies(map)
        print(tree.costs)
        print(tree.get_cost_of_characters(text))
if __name__ == '__main__':
    try:
        #Test_huffman_coding.test_compression()
        #Test_huffman_coding.test_big_compression()
        #Test_huffman_coding.test_compression_comparison()
        #Test_huffman_coding.compare_twain_henry_press()
        #Test_huffman_coding.test_huffman_library()
        Test_huffman_coding.test_huffman_mathmatically()
    except:
        traceback.print_exc()