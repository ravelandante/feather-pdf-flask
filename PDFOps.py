# Author: Fynn Young (ravelandante)
# Creation Date: 23/01/2023
# --------------------------------------

from pypdf import PdfReader, PdfWriter
import os


class PDFOps:

    def __init__(self):
        self.default_out = 'outputs/'
        # create default output dir if it doesn't exist
        if not os.path.exists(self.default_out):
            os.makedirs(self.default_out)

    def append(self, paths, out_name):
        writer = PdfWriter()

        for pdf in paths:
            writer.append(pdf)
        writer.write(self.default_out + out_name)
        writer.close()

    def merge(self, paths, out_name):
        writer = PdfWriter()

        open_pdfs = []
        for pdf in paths:
            open_pdfs.append(open(pdf, 'rb'))
        writer.write(self.default_out + out_name)
        writer.close()

    def compress(self, path, out_name):
        writer = PdfWriter()

        reader = PdfReader(path)
        for page in reader.pages:
            page.compress_content_streams()  # CPU intensive
            writer.add_page(page)

        with open(self.default_out + out_name, 'wb') as f:
            writer.write(f)
        writer.close()

    def fix_rotation(self, path, out_name, type):
        writer = PdfWriter()

        reader = PdfReader(path)
        for page in reader.pages:
            while (page.rotation != type):
                page.rotate(90)
            writer.add_page(page)

            with open(self.default_out + out_name, 'wb') as f:
                writer.write(f)
        writer.close()

    def delete(self, path, pages, save_new=True):
        writer = PdfWriter()
        reader = PdfReader(path)
        select_pages = [i for i in range(
            0, len(reader.pages)) if i not in pages]

        with open(path, 'rb') as f:
            writer.append(f, select_pages)
            out_name = path if not save_new else self.default_out + (path.split('/')[-1])[:-4] + '_deleted.pdf'
            with open(out_name, 'wb') as f:
                writer.write(f)
        writer.close()

    def split(self, path, splits):
        reader = PdfReader(path)
        l_split = 0

        for i, split in enumerate(splits):
            writer = PdfWriter()
            with open(path, 'rb') as f:
                writer.append(f, (l_split, split))
                out_name = self.default_out + (path.split('/')[-1])[:-4] + '_split_' + str(i) + '.pdf'
                with open(out_name, 'wb') as f:
                    writer.write(f)
            l_split = split
            writer.close()

            if i == len(splits) - 1:
                writer = PdfWriter()
                with open(path, 'rb') as f:
                    writer.append(f, (l_split, len(reader.pages)))
                    out_name = self.default_out + (path.split('/')[-1])[:-4] + '_split_' + str(i + 1) + '.pdf'
                    with open(out_name, 'wb') as f:
                        writer.write(f)
                writer.close()

    def extract_range(self, path, ranges):
        for i, range in enumerate(ranges):
            writer = PdfWriter()
            with open(path, 'rb') as f:
                writer.append(f, (range[0] - 1, range[1]))
                out_name = self.default_out + (path.split('/')[-1])[:-4] + '_range_' + str(range[0]) + '-' + str(range[1]) + '.pdf'
                with open(out_name, 'wb') as f:
                    writer.write(f)
            writer.close()
