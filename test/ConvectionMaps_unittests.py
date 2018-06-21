from DARNprocessing import ConvectionMaps
from glob import glob
import unittest
import os
import shutil

"""
Unit test suite for testing the ConvectionMaps class
"""

class TestFitData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data_path = os.getcwd() + "/test_data/"
        self.omni_path = os.getcwd() + "/omni/"
        self.plot_path = os.getcwd() + "/plots/"
        self.map_path = os.getcwd() + "/maps/"

        self.convec_map = ConvectionMaps(None,{'date': "20060301",
                                               'datapath': self.data_path,
                                               'plotpath': self.plot_path,
                                               'omnipath': self.omni_path,
                                               'mappath': self.map_path})
        self.convec_map.generate_grid_files()
        self.convec_map.generate_map_files()
        self.convec_map.generate_RST_convection_maps()

    @classmethod
    def tearDownClass(self):
        self.convec_map.cleanup()
        shutil.rmtree(self.map_path)
        shutil.rmtree(self.plot_path)

    def test_unzips_fitacf(self):
        assert(os.path.exists(self.plot_path+'20060301.C0.wal.fitacf'))

    def test_convert_fit_to_fitacf(self):
        assert(os.path.exists(self.plot_path+'20060301.C0.kod.fitacf'))
        assert(os.path.exists(self.plot_path+'20060301.C0.kap.fitacf'))
        assert(os.path.exists(self.plot_path+'20060301.C0.sto.fitacf'))

    def test_generate_grid_files(self):
        assert(os.path.exists(self.plot_path+'20060301.kod.grid'))
        assert(os.path.exists(self.plot_path+'20060301.kap.grid'))
        assert(os.path.exists(self.plot_path+'20060301.sto.grid'))
        assert(os.path.exists(self.plot_path+'20060301.wal.grid'))
        assert(os.path.exists(self.plot_path+'20060301.grd'))

    def test_map_file(self):
        assert(os.path.exists(self.plot_path+'20060301.empty.map'))
        assert(os.path.exists(self.plot_path+'20060301.hmb.map'))
        assert(os.path.exists(self.plot_path+'20060301.imf.map'))
        assert(os.path.exists(self.plot_path+'20060301.model.map'))
        assert(os.path.exists(self.map_path+'20060301.map'))

    def test_convection_plot_files(self):
        self.assertNotEqual(len(glob(self.plot_path+'20060301.*.ps')),0)
        self.assertNotEqual(len(glob(self.plot_path+'20060301.*.pdf')),0)

class TestSouthRadars(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data_path = os.getcwd() + "/test_data/"
        self.omni_path = os.getcwd() + "/omni/"
        self.plot_path = os.getcwd() + "/plots/south/"
        self.map_path = os.getcwd() + "/maps/south/"

        self.convec_map = ConvectionMaps(None,{'date': 20170301,
                                               'hemisphere': 'south',
                                               'datapath': self.data_path,
                                               'plotpath': self.plot_path,
                                               'omnipath': self.omni_path,
                                               'mappath': self.map_path,
                                               'image_extension': 'png'})
        self.convec_map.generate_grid_files()
        self.convec_map.generate_map_files()
        self.convec_map.generate_RST_convection_maps()

    @classmethod
    def tearDownClass(self):
        pass
        #self.convec_map.cleanup()
        #shutil.rmtree(self.map_path)
        #shutil.rmtree(self.plot_path)

    def test_generation_path(self):
        assert(os.path.exists(self.data_path))
        assert(os.path.exists(self.omni_path))
        assert(os.path.exists(self.plot_path))
        assert(os.path.exists(self.map_path))

    def test_unzips_fitacf(self):
        assert(not os.path.exists(self.plot_path+'20170301.C0.han.fitacf'))
        assert(not os.path.exists(self.plot_path+'20170301.C0.inv.fitacf'))
        assert(not os.path.exists(self.plot_path+'20170301.C0.sas.fitacf'))

    def test_generate_grid_files(self):
        assert(os.path.exists(self.plot_path+'20170301.zho.a.grid'))
        assert(os.path.exists(self.plot_path+'20170301.sps.a.grid'))
        assert(os.path.exists(self.plot_path+'20170301.mcm.a.grid'))
        assert(os.path.exists(self.plot_path+'20170301.grd'))

    def test_generate_not_south_radar_file(self):
        assert(not os.path.exists(self.plot_path+'20170301.sas.grid'))
        assert(not os.path.exists(self.plot_path+'20170301.inv.grid'))
        assert(not os.path.exists(self.plot_path+'20170301.ksr.a.grid'))

    def test_map_file(self):
        assert(os.path.exists(self.plot_path+'20170301.empty.map'))
        assert(os.path.exists(self.plot_path+'20170301.hmb.map'))
        assert(os.path.exists(self.plot_path+'20170301.imf.map'))
        assert(os.path.exists(self.plot_path+'20170301.model.map'))
        assert(os.path.exists(self.map_path+'20170301.map'))

    def test_convection_plot_files(self):
        self.assertNotEqual(len(glob(self.plot_path+'20170301.*.ps')),0)
        self.assertEqual(len(glob(self.plot_path+'20170301.*.pdf')),0)
        self.assertNotEqual(len(glob(self.plot_path+'20170301.*.png')),0)

class TestNorthData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data_path = os.getcwd() + "/test_data/"
        self.omni_path = os.getcwd() + "/omni/"
        self.plot_path = os.getcwd() + "/plots/"
        self.map_path = os.getcwd() + "/maps/"

        self.convec_map = ConvectionMaps(None,{'date': "20170301",
                                               'canadian': True,
                                               'datapath': self.data_path,
                                               'plotpath': self.plot_path,
                                               'omnipath': self.omni_path,
                                               'mappath': self.map_path})
        self.convec_map.generate_grid_files()
        self.convec_map.generate_map_files()
        self.convec_map.generate_RST_convection_maps()

    @classmethod
    def tearDownClass(self):
        self.convec_map.cleanup()
        shutil.rmtree(self.map_path)
        shutil.rmtree(self.plot_path)

    def test_generation_path(self):
        assert(os.path.exists(self.data_path))
        assert(os.path.exists(self.omni_path))
        assert(os.path.exists(self.plot_path))
        assert(os.path.exists(self.map_path))

    def test_unzips_fitacf(self):
        assert(os.path.exists(self.plot_path+'20170301.C0.han.fitacf'))
        assert(os.path.exists(self.plot_path+'20170301.C0.inv.fitacf'))
        assert(os.path.exists(self.plot_path+'20170301.C0.sas.fitacf'))

    def test_generate_grid_files(self):
        assert(os.path.exists(self.plot_path+'20170301.rkn.a.grid'))
        assert(os.path.exists(self.plot_path+'20170301.rkn.b.grid'))
        assert(os.path.exists(self.plot_path+'20170301.ksr.b.grid'))
        assert(os.path.exists(self.plot_path+'20170301.ksr.a.grid'))
        assert(os.path.exists(self.plot_path+'20170301.inv.grid'))
        assert(os.path.exists(self.plot_path+'20170301.sas.grid'))
        assert(os.path.exists(self.plot_path+'20170301.grd'))

    def test_generate_not_south_radar_file(self):
        assert(not os.path.exists(self.plot_path+'20170301.mcm.a.grid'))
        assert(not os.path.exists(self.plot_path+'20170301.zho.grid'))
        assert(not os.path.exists(self.plot_path+'20170301.sps.a.grid'))

    def test_empty_files(self):
        assert(not os.path.exists(self.plot_path+'20170301.wal.grid'))

    def test_map_file(self):
        assert(os.path.exists(self.plot_path+'20170301.empty.map'))
        assert(os.path.exists(self.plot_path+'20170301.hmb.map'))
        assert(os.path.exists(self.plot_path+'20170301.imf.map'))
        assert(os.path.exists(self.plot_path+'20170301.model.map'))
        assert(os.path.exists(self.map_path+'20170301.map'))

    def test_convection_plot_files(self):
        self.assertNotEqual(len(glob(self.plot_path+'20170301.*.ps')),0)
        self.assertNotEqual(len(glob(self.plot_path+'20170301.*.pdf')),0)



class TestNorthData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data_path = os.getcwd() + "/test_data/"
        self.omni_path = os.getcwd() + "/omni/"
        self.plot_path = os.getcwd() + "/plots/"
        self.map_path = os.getcwd() + "/maps/"

        self.convec_map = ConvectionMaps(None,{'date': "20170301",
                                               'datapath': self.data_path,
                                               'plotpath': self.plot_path,
                                               'omnipath': self.omni_path,
                                               'mappath': self.map_path})
        self.convec_map.generate_grid_files()
        self.convec_map.generate_map_files()
        self.convec_map.generate_RST_convection_maps()

    @classmethod
    def tearDownClass(self):
        self.convec_map.cleanup()
        shutil.rmtree(self.map_path)
        shutil.rmtree(self.plot_path)

    def test_generation_path(self):
        assert(os.path.exists(self.data_path))
        assert(os.path.exists(self.omni_path))
        assert(os.path.exists(self.plot_path))
        assert(os.path.exists(self.map_path))

    def test_unzips_fitacf(self):
        assert(os.path.exists(self.plot_path+'20170301.C0.han.fitacf'))
        assert(os.path.exists(self.plot_path+'20170301.C0.inv.fitacf'))
        assert(os.path.exists(self.plot_path+'20170301.C0.sas.fitacf'))

    def test_generate_grid_files(self):
        assert(os.path.exists(self.plot_path+'20170301.rkn.a.grid'))
        assert(os.path.exists(self.plot_path+'20170301.rkn.b.grid'))
        assert(os.path.exists(self.plot_path+'20170301.ksr.b.grid'))
        assert(os.path.exists(self.plot_path+'20170301.ksr.a.grid'))
        assert(os.path.exists(self.plot_path+'20170301.inv.grid'))
        assert(os.path.exists(self.plot_path+'20170301.sas.grid'))
        assert(os.path.exists(self.plot_path+'20170301.grd'))

    def test_generate_not_south_radar_file(self):
        assert(not os.path.exists(self.plot_path+'20170301.mcm.a.grid'))
        assert(not os.path.exists(self.plot_path+'20170301.zho.grid'))
        assert(not os.path.exists(self.plot_path+'20170301.sps.a.grid'))

    def test_empty_files(self):
        assert(not os.path.exists(self.plot_path+'20170301.wal.grid'))

    def test_map_file(self):
        assert(os.path.exists(self.plot_path+'20170301.empty.map'))
        assert(os.path.exists(self.plot_path+'20170301.hmb.map'))
        assert(os.path.exists(self.plot_path+'20170301.imf.map'))
        assert(os.path.exists(self.plot_path+'20170301.model.map'))
        assert(os.path.exists(self.map_path+'20170301.map'))

    def test_convection_plot_files(self):
        self.assertNotEqual(len(glob(self.plot_path+'20170301.*.ps')),0)
        self.assertNotEqual(len(glob(self.plot_path+'20170301.*.pdf')),0)


if __name__ == '__main__':
    unittest.main()

