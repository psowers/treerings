#!/usr/bin/env python
"""
Input file:
    Core ID   Year  Measurement  [Site ID]
    col 1-6   9-12      13-18      20-24

Output file:
    Core ID  Decade  Measurement(s)  [Site ID]
    col 1-6   9-12      13-72            74-78
    source: ftp://ftp.ncdc.noaa.gov/pub/data/paleo/treering/treeinfo.txt
    http://www.voortech.com/projectj2x/docs/userGuide.htm#Appendix 1.
"""

from treerings import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        FilesIn = [os.path.abspath(arg) for arg in sys.argv[1:] if os.path.isfile(arg)]
        for arg in sys.argv[1:]:
            if not os.path.abspath(arg) in FilesIn:
                print('Argument not vaild: "%s"' % arg)
    else:
        FilesIn = [promptfile()]

    for Fin in FilesIn:
        if is_readable(Fin):
            Fout_nm = unique_nm(os.path.splitext(Fin)[0] + '.rwl')
            flat2raw(Fin, Fout_nm)
