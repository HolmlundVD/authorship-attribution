from Book import BookGraph
from DefaultStemmer import DefaultStemmer
import traceback
import pdf_analyzer
import compression
def main():
    try:
        
        text=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        book=BookGraph(text,DefaultStemmer)
        print(book.getFrequency("fox","dog"))#2
        print(book.getFrequency("foxy","dog"))#1
        print(book.getFrequency("fox","lazy"))#2
        print(book.getFrequency("fox","horse"))#0
        print(book.getFrequency("foxy","jumps"))#0
        print(book.getFrequency("dog","lazy"))#3
        print(book.getFrequency("lazy","dog"))#3
        print(book.getAdjacencyMatrix())
        print(compression.compression.get_word_frequencies(text))
    except:
        traceback.print_exc()
    

if __name__ == '__main__':
    main()