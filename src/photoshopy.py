import win32com.client
import os
from pathvalidate import sanitize_filename

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

    def closePhotoshop(self):
        self.app.Quit()

    def openPSD(self, filename):
        if os.path.isfile(filename) == False:
            self.closePhotoshop()
            return False

        self.app.Open(filename)
        self.psd_file = self.app.Application.ActiveDocument
        return True

    def closePSD(self):
        if self.psd_file is None:
            raise Exception(FileNotFoundError)

        self.app.Application.ActiveDocument.Close(DO_NOT_SAVE_CHANGES)

    def updateLayerText(self, layer_name, text):
        if self.psd_file is None:
            raise Exception(FileNotFoundError)
        
        layer = self.psd_file.ArtLayers[layer_name]
        layer_text = layer.TextItem
        layer_text.contents = text
        return True

    def exportJPEG(self, filename, folder='', quality=DEFAULT_JPEG_QUALITY):
        if self.psd_file is None:
            raise Exception(FileNotFoundError)

        filename = sanitize_filename(filename)
        full_path = os.path.join(folder, filename)

        options = win32com.client.Dispatch("Photoshop.ExportOptionsSaveForWeb")
        options.Format = DOCUMENT_TYPE_JPEG
        options.Quality = quality

        self.psd_file.Export(ExportIn=full_path, ExportAs=SAVE_FOR_WEB, Options=options)

        return os.path.isfile(full_path)