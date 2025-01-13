import unittest
from dotenv import load_dotenv
import os

from filehandler.fh import Filehandler

class Testing(unittest.TestCase):
  def setup(self):
    load_dotenv()
    self.fh = Filehandler()
    self.download_directory = os.getenv("DOWNLOAD_DIRECTORY")

  def test_filehandler(self):
    self.setup()
    self.assertEqual(self.fh.download_directory, os.getenv("DOWNLOAD_DIRECTORY"))
    self.assertEqual(self.fh.data, None)
    self.assertEqual(self.fh.links, None)

if __name__ == '__main__':
    unittest.main()
