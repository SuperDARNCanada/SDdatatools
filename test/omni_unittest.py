import os
import unittest

from DARNprocessing import Omni
"""
Unit test suit for testing the Omni class
"""
TestOmniClass(unittest.TestCase):

    def setUp(self):
        self.date = "20170601"
        self.omni_path = os.getcwd() + '/omni/'
        self.omni_obj = Omni(self.date,self.omni_path)

    def tearDown(self):
        os.remove(self.omni_path+'20170301_omni.txt')

    def test_no_omni_file_exception(self):
        assertRaises(OmniFileNotFoundWarning,self.omni_obj.check_for_updates())

    def test_get_omni_file(self):
        self.omni_obj.get_omni_file()
        assert(os.path.isfile(self.omni_path+'20170601_omni.txt'))

    def test_no_omni_data_found(self):
        assertRaises(self.omnifile_to_IMFfile)

    def test_omni_to_imf_file(self):
        self.omni_obj.get_omni_file()
        self.omnifile_to_IMFfile()
        assert(os.path.isfile(self.omni_path+'20170601_imf.txt'))

