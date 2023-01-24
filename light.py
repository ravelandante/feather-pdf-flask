# Author: Fynn Young (ravelandante)
# Creation Date: 23/01/2023
# --------------------------------------

from PDFOps import PDFOps

p = PDFOps()

#print('append [in1.pdf,in2.pdf,...] [out.pdf]\ncompress [in1.pdf,in2.pdf,...] [out1.pdf,out2.pdf,...]\nfix_rotation [in1.pdf,in2.pdf,...] [out1.pdf,out2.pdf,...] [type]')
print('q to quit')
while (True):
    cmd = input().split(' ')

    if cmd[0] == 'q':
        break

    elif cmd[0] == 'merge':
        p.append(cmd[1].split(','), cmd[2])

    elif cmd[0] == 'compress':
        p.compress(cmd[1], cmd[2])

    elif cmd[0] == 'fix_rotation':
        type = 0 if cmd[3] == 'p' else 90
        p.fix_rotation(cmd[1], cmd[2], type)

    elif cmd[0] == 'delete':
        pages = cmd[2].split(',') if len(cmd[2]) > 1 else [cmd[2]]
        pages = [int(page) - 1 for page in pages]
        p.delete(cmd[1], pages)

    elif cmd[0] == 'split':
        splits = cmd[2].split(',') if len(cmd[2]) > 1 else [cmd[2]]
        splits = [int(split) - 1 for split in splits]
        p.split(cmd[1], splits)

    elif cmd[0] == 'extract':
        ranges = cmd[2].split(',') if len(cmd[2]) > 1 else [cmd[2]]
        for i, range in enumerate(ranges):
            dash = range.find('-')
            ranges[i] = (int(range[0:dash]), int(range[dash + 1:]))
        p.extract_range(cmd[1], ranges)
    print('DONE')
