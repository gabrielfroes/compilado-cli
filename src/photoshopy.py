import win32com.client
import os
from pathvalidate import sanitize_filename
import logging

DO_NOT_SAVE_CHANGES = 2
DEFAULT_JPEG_QUALITY = 10
SAVE_FOR_WEB = 2
DOCUMENT_TYPE_JPEG = 6

class Photoshopy:
    app = None
    psd_file = None

    def __init__(self):
        self.app = win32com.client.Dispatch("Photoshop.Application")
        self.app.Visible = False

        self.log = logging.getLogger(__name__)
        self.log.debug("Photoshop started")

    def closePhotoshop(self):
        self.app.Quit()
        self.log.debug("Photoshop closed")

    def openPSD(self, filename):
        if os.path.isfile(filename) == False:
            self.log.error("File not found: {0}".format(filename))
            self.closePhotoshop()
            return False

        self.app.Open(filename)
        self.psd_file = self.app.Application.ActiveDocument

        self.log.debug("PSD opened: {0}".format(filename))
        return True

    def closePSD(self):
        if self.psd_file is None:
            self.log.error("PSD file is not opened")
            raise Exception(FileNotFoundError)

        self.app.Application.ActiveDocument.Close(DO_NOT_SAVE_CHANGES)
        self.log.debug("PSD file closed")

    def updateLayerText(self, layer_name, text):
        if self.psd_file is None:
            self.log.error("PSD file is not opened")
            raise Exception(FileNotFoundError)
        
        layer = self.psd_file.ArtLayers[layer_name]
        layer_text = layer.TextItem
        layer_text.contents = text
        return True

    def exportJPEG(self, filename, folder='', quality=DEFAULT_JPEG_QUALITY):
        if self.psd_file is None:
            self.log.error("PSD file is not opened")
            raise Exception(FileNotFoundError)

        filename = sanitize_filename(filename)
        full_path = os.path.join(folder, filename)

        options = win32com.client.Dispatch("Photoshop.ExportOptionsSaveForWeb")
        options.Format = DOCUMENT_TYPE_JPEG
        options.Quality = quality

        self.psd_file.Export(ExportIn=full_path, ExportAs=SAVE_FOR_WEB, Options=options)
        self.log.info("JPEG Export: {0}".format(full_path))

        return os.path.isfile(full_path)