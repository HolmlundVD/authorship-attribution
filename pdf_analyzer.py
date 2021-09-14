import urllib, PyPDF2
from io import StringIO
from io import BytesIO

class pdf_analyzer(object):
   @staticmethod
   #the method takes a url for a pdf and parses and returns the text in the form of a string from the 
   #start page denoted by the parameter the the last page parameter inclusive
   def analyze_pdf(url_to_analyze:str,start_page:int,last_page)->str:
       remoteFile = urllib.request.urlopen(url_to_analyze).read()
       memoryFile = BytesIO(remoteFile)
       pdfFile = PyPDF2.PdfFileReader(memoryFile)
       initial=str()
       for i in range(start_page,last_page):
           initial+=pdfFile.getPage(i).extractText()
       
       return initial