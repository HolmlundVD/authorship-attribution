import unittest
from googleapiclient.discovery import build

class Test_test_youtube_api_connect(unittest.TestCase):
    def test_A(self):
        service=build('youtube','v3')
        print(service)
        

if __name__ == '__main__':
    unittest.main()
