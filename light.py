# Author: Fynn Young (ravelandante)
# Creation Date: 23/01/2023
# --------------------------------------

from PDFOps import PdfOps


print('q to quit')
while (True):
    cmd = input().split(' ')

    if cmd[0] == 'q':
        break

    p = PdfOps(cmd[1])

    if cmd[0] == 'append':
        p.append(cmd[2].split(','))

    elif cmd[0] == 'compress':
        p.compress()

    elif cmd[0] == 'rotate':
        type = 0 if cmd[2] == 'p' else 90
        p.rotate(type)

    elif cmd[0] == 'delete':
        pages = cmd[2].split(',') if len(cmd[2]) > 1 else [cmd[2]]
        pages = [int(page) - 1 for page in pages]
        p.delete(pages)

    elif cmd[0] == 'split':
        splits = cmd[2].split(',') if len(cmd[2]) > 1 else [cmd[2]]
        splits = [int(split) - 1 for split in splits]
        p.split(splits)

    elif cmd[0] == 'extract':
        ranges = cmd[2].split(',') if len(cmd[2]) > 1 else [cmd[2]]
        for i, range in enumerate(ranges):
            dash = range.find('-')
            ranges[i] = (int(range[0:dash]), int(range[dash + 1:]))
        p.extract_range(ranges)
    
    elif cmd[0] == 'metadata':
        metadata = {}
        metadata.update({'/Title': input('Title: ')})
        metadata.update({'/Author': input('Author: ')})
        metadata.update({'/Producer': input('Producer: ')})
        metadata.update({'/Creator': input('Creator: ')})
        metadata.update({'/Subject': input('Subject: ')})
        p.edit_metadata(metadata)
    print('DONE')
