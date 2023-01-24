# Author: Fynn Young (ravelandante)
# Creation Date: 23/01/2023
# --------------------------------------

from pypdf import PdfReader, PdfWriter
import os


class PDFOps:

    def __init__(self, path):
        self.default_out = 'outputs/'
        # create default output dir if it doesn't exist
        if not os.path.exists(self.default_out):
            os.makedirs(self.default_out)
        self.path = path
        self.reader = PdfReader(self.path)
        self.writer = PdfWriter()

    def reset(self):
        """Reset (clear) PDF writer & reader for the next action"""
        self.writer.close()
        self.writer = PdfWriter()
        self.reader = PdfReader(self.path)

    def append(self, paths, out_name):
        """Append multiple PDFs in order of paths"""
        self.writer.append(self.path)
        for pdf in paths:
            self.writer.append(pdf)
        with open(self.default_out + out_name, 'wb') as f:
            self.writer.write(f)
        self.reset()

    def merge(self, paths, out_name):
        """Complex merging of PDFs"""
        open_pdfs = []
        for pdf in paths:
            open_pdfs.append(open(pdf, 'rb'))
        with open(self.default_out + out_name, 'wb') as f:
            self.writer.write(f)
        self.reset()

    def compress(self, out_name):
        """Compress a PDF"""
        for page in self.reader.pages:
            page.compress_content_streams()  # CPU intensive
            self.writer.add_page(page)

        with open(self.default_out + out_name, 'wb') as f:
            self.writer.write(f)
        self.reset()

    def fix_rotation(self, out_name, type):
        """Change all pages in the PDF to the specified orientation"""
        for page in self.reader.pages:
            while (page.rotation != type):
                page.rotate(90)
            self.writer.add_page(page)

            with open(self.default_out + out_name, 'wb') as f:
                self.writer.write(f)
        self.reset()

    def delete(self, pages, save_new=True):
        """Delete given pages in the PDF"""
        select_pages = [i for i in range(0, len(self.reader.pages)) if i not in pages]

        with open(self.path, 'rb') as f:
            self.writer.append(f, select_pages)
            out_name = self.path if not save_new else self.default_out + (self.path.split('/')[-1])[:-4] + '_deleted.pdf'
            with open(out_name, 'wb') as f:
                self.writer.write(f)
        self.reset()

    def split(self, splits):
        """Split the PDF at given pages and output 2 new PDFs for each split"""
        l_split = 0

        for i, split in enumerate(splits):
            with open(self.path, 'rb') as f:
                self.writer.append(f, (l_split, split))
                out_name = self.default_out + (self.path.split('/')[-1])[:-4] + '_split_' + str(i) + '.pdf'
                with open(out_name, 'wb') as f:
                    self.writer.write(f)
            l_split = split
            self.reset()

            if i == len(splits) - 1:
                
                with open(self.path, 'rb') as f:
                    self.writer.append(f, (l_split, len(self.reader.pages)))
                    out_name = self.default_out + (self.path.split('/')[-1])[:-4] + '_split_' + str(i + 1) + '.pdf'
                    with open(out_name, 'wb') as f:
                        self.writer.write(f)
                self.reset()

    def extract_range(self, ranges):
        """Extract ranges of pages from the PDF and write them to distinct output PDFs"""
        for range in ranges:
            with open(self.path, 'rb') as f:
                self.writer.append(f, (range[0] - 1, range[1]))
                out_name = self.default_out + (self.path.split('/')[-1])[:-4] + '_range_' + str(range[0]) + '-' + str(range[1]) + '.pdf'
                with open(out_name, 'wb') as f:
                    self.writer.write(f)
            self.reset()
