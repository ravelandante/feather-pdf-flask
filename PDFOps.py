#from pypdf import *
from pypdf import PdfReader, PdfWriter

class PDFOps:

    def __init__(self, pdf_name):
        pass
        
    def simple_merge(self, paths, out_name):
        merger = PdfWriter()
        for pdf in paths:
            merger.append(pdf)
        merger.write(out_name)
        merger.close()

    def complex_merge(self, paths, out_name):
        merger = PdfWriter()
        open_pdfs = []
        for pdf in paths:
            open_pdfs.append(open(pdf, 'rb'))
        merger.write(out_name)
        merger.close()

    def compress(self, paths, out_names):
        writer = PdfWriter()

        for i, path in enumerate(paths):
            reader = PdfReader(path)
            for page in reader.pages:
                page.compress_content_streams() # CPU intensive
                writer.add_page(page)
        
            with open(out_names[i], 'wb') as f:
                writer.write(f)
        writer.close()

    def fix_rotation(self, paths, out_names, type):
        writer = PdfWriter()
        for i, path in enumerate(paths):
            reader = PdfReader(path)
            for page in reader.pages:
                while (page.rotation != type):
                    page.rotate(90)
                writer.add_page(page)
        
            with open(out_names[i], 'wb') as f:
                writer.write(f)
        writer.close()
