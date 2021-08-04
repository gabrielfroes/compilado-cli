import sys, os
sys.path.insert(0, './src')
import unittest
from photoshopy import Photoshopy

class TestPhotoshopy(unittest.TestCase):

    def setUp(self):
        self.psd_origin = os.path.abspath("./tests/resources/miniatura-podcast.psd")
        self.jpeg_path = os.path.abspath("./tests/resources/tmp")
        self.jpeg_name = "miniatura-podcast.jpg"
        self.jpeg_full_path = os.path.join(self.jpeg_path, self.jpeg_name)

        if not os.path.exists(self.jpeg_path):
                    os.mkdir(self.jpeg_path)

        self.app = Photoshopy()

    def tearDown(self):
        self.app.closePhotoshop()

        if os.path.exists(self.jpeg_full_path):
             os.remove(self.jpeg_full_path)
             
        if os.path.exists(self.jpeg_path):
            os.rmdir(self.jpeg_path)

    def test_openPSD(self):
        opened = self.app.openPSD(self.psd_origin)
        if opened:
            self.app.closePSD()
        self.assertTrue(opened)

    def test_updateLayerText(self):
        updated1 = False
        updated2 = False

        opened = self.app.openPSD(self.psd_origin)
        if opened:
            updated1 = self.app.updateLayerText("PERIODO", "TESTE")
            updated2 = self.app.updateLayerText("NUMERO_EPISODIO", "TESTE")
            self.app.closePSD()

        self.assertTrue(updated1)
        self.assertTrue(updated2)

    def test_exportJPEG(self):
        exported = False

        opened = self.app.openPSD(self.psd_origin)
        if opened:
            updated1 = self.app.updateLayerText("PERIODO", "TESTE")
            updated2 = self.app.updateLayerText("NUMERO_EPISODIO", "TESTE")

            if updated1 & updated2:
                exported = self.app.exportJPEG(self.jpeg_name, self.jpeg_path)

            self.app.closePSD()

        self.assertTrue(exported)


if __name__ == '__main__':
    unittest.main()   