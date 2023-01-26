# Author: Fynn Young (ravelandante)
# Creation Date: 23/01/2023
# --------------------------------------

from pypdf import PdfReader, PdfWriter
import os


class PdfOps:

    def __init__(self, path, default_out='outputs/'):
        self.path = path
        self.default_out = default_out
        # create default output dir if it doesn't exist
        if not os.path.exists(self.default_out):
            os.makedirs(self.default_out)
        self.default_name = self.default_out + (self.path.split('/')[-1])[:-4]

        self.reader = PdfReader(self.path)
        self.writer = PdfWriter()

    def reset(self):
        """Reset (clear) PDF writer & reader for the next action"""
        self.writer.close()
        self.writer = PdfWriter()
        self.reader = PdfReader(self.path)

    def write(self):
        """Writes pages to PDF"""
        pass

    def append(self, paths):
        """Append multiple PDFs in order of paths"""
        self.writer.append(self.path)
        for pdf in paths:
            self.writer.append(pdf)
        with open('{}_appended.pdf'.format(self.default_name), 'wb') as f:
            self.writer.write(f)

    def merge(self, paths):
        """Complex merging of PDFs"""
        open_pdfs = []
        for pdf in paths:
            open_pdfs.append(open(pdf, 'rb'))
        with open('{}_merged.pdf'.format(self.default_name), 'wb') as f:
            self.writer.write(f)

    def compress(self):
        """Compress a PDF"""
        for page in self.reader.pages:
            page.compress_content_streams()  # CPU intensive
            self.writer.add_page(page)

        self.writer.add_metadata(self.reader.metadata)
        with open('{}_compressed.pdf'.format(self.default_name), 'wb') as f:
            self.writer.write(f)

    def rotate(self, type):
        """Change all pages in the PDF to the specified orientation"""
        for page in self.reader.pages:
            while (page.rotation != type):
                page.rotate(90)
            self.writer.add_page(page)

        self.writer.add_metadata(self.reader.metadata)
        with open('{}_rotated.pdf'.format(self.default_name), 'wb') as f:
            self.writer.write(f)

    def delete(self, pages, save_new=True):
        """Delete given pages in the PDF"""
        select_pages = [i for i in range(0, len(self.reader.pages)) if i not in pages]

        with open(self.path, 'rb') as f:
            self.writer.append(f, select_pages)
            self.writer.add_metadata(self.reader.metadata)
            with open(self.path if not save_new else '{}_deleted.pdf'.format(self.default_name), 'wb') as f:
                self.writer.write(f)

    def split(self, splits):
        """Split the PDF at given pages and output 2 new PDFs for each split"""
        l_split = 0

        for i, split in enumerate(splits):
            with open(self.path, 'rb') as f:
                self.writer.append(f, (l_split, split))
                self.writer.add_metadata(self.reader.metadata)
                with open('{}_split_{}.pdf'.format(self.default_name, i), 'wb') as f:
                    self.writer.write(f)
            l_split = split
            self.reset()

            if i == len(splits) - 1:
                
                with open(self.path, 'rb') as f:
                    self.writer.append(f, (l_split, len(self.reader.pages)))
                    self.writer.add_metadata(self.reader.metadata)
                    with open('{}_split_{}.pdf'.format(self.default_name, i), 'wb') as f:
                        self.writer.write(f)
                self.reset()

    def extract_range(self, ranges):
        """Extract ranges of pages from the PDF and write them to distinct output PDFs"""
        for range in ranges:
            with open(self.path, 'rb') as f:
                self.writer.append(f, (range[0] - 1, range[1]))
                self.writer.add_metadata(self.reader.metadata)
                with open('{}_split_{}-{}.pdf'.format(self.default_name, range[0], range[1]), 'wb') as f:
                    self.writer.write(f)
            self.reset()

    def edit_metadata(self, metadata):
        for page in self.reader.pages:
            self.writer.add_page(page)
        self.writer.add_metadata(metadata)
        with open('{}_metadata.pdf'.format(self.default_name), 'wb') as f:
            self.writer.write(f)
