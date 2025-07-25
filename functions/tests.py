import unittest
from get_files_info import *


class GetFilesInfoTest(unittest.TestCase):
    def setUp(self):
        self.root = root_dir()

    
    def test_get_root_info(self):
        directory = "."
        contents = get_contents(self.root, directory)
