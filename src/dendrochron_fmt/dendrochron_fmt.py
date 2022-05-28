#!/usr/bin/env python3
"""
Convert tree ring data files between decadal and flat formats.

Decadal, raw data, format:
    Core ID  Decade  Measurement(s)  [Site ID]
    col 1-6   9-12      13-72            74-78
    source: ftp://ftp.ncdc.noaa.gov/pub/data/paleo/treering/treeinfo.txt
    http://www.voortech.com/projectj2x/docs/userGuide.htm#Appendix 1.

Flat, column, format:
    Core ID   Year  Measurement  [Site ID]
    col 1-6   9-12      13-18      20-24
"""
import os
import sys
import tempfile 
from datetime import datetime


def unique_file(file_name):
    """Opens a new file for writing."""
    try:
        fd = open(file_name, 'x')
    except FileExistsError:
        dirname, filename = os.path.split(file_name)
        prefix, suffix = os.path.splitext(filename)
        fd, file_name = tempfile.mkstemp(suffix, prefix+"_", dirname, text=True)
    finally:
        return fd, file_name


def raw2flat(file_in, file_out):
    """Reads the decadal input file and writes it to the system in a flat format text file."""
    print(f'Output:\t"{file_out}"')
    output_file = open(file_out, 'a')
    for line in open(file_in, 'r'):
        if not len(line) >= 18:
            continue
        core_id = line[:8]
        year = int(line[8:12])
        if len(line[12:].rstrip()) <= 60:
            site_id = ''
            data = line[12:].rstrip()
        else:
            site_id = line[73:]
            data = line[12:72]
        if not (len(data) % 6) == 0:
            data = '  #Err'.rjust(6)
        s, e = 0, 0
        while e <= (len(data) - 6):
            e += 6
            element = data[s:e].lstrip()
            new_line = core_id.ljust(8) + str(year).rjust(4) + element.rjust(6) + site_id + '\n'
            output_file.write(new_line)
            year += 1
            s = e
    output_file.close()


def flat2raw(file_in, file_out):
    """Reads the flat tree ring file and writes it to the system in raw data format (decadal) file."""
    print('Output:\t"%s"' % file_out)
    output_file = open(file_out, 'a')
    _dec, _cID, _sID = 0, '', ''
    data = ''
    for line in open(file_in, 'r'):
        if not len(line) >= 18:
            continue
        core_id = line[:8]
        year = int(line[8:12])
        decade = (year // 10) * 10
        element = line[12:].rstrip()
        if len(element) == 6:
            site_id = ''
        elif len(element) >= 12 or len(element) <= 13:
            site_id = element[18:]
            element = element[12:18].rstrip().rjust(6)
        else:
            if not (len(element) % 6) == 0:
                element = ''
            site_id = '  #Err'
        if data:
            if not decade == ((_dec // 10) * 10) or not core_id == _cID or not site_id == _sID:
                new_line = _cID.ljust(8) + str(_dec).rjust(4) + data + _sID + '\n'
                if new_line.strip():
                    output_file.write(new_line)
                _dec, _cID, _sID = year, core_id, site_id
                data = ''
        else:
            _dec, _cID, _sID = year, core_id, site_id
        if data:
            data += element
        else:
            data = element
    new_line = _cID.ljust(8) + str(_dec).rjust(4) + data + _sID + '\n'
    output_file.write(new_line)
    output_file.close()


if __name__ == '__main__':

    if sys.argv[1] in ['-h', '--help', '-help']:
        print('treerings.py -convert2flat file1 [file2...]')
        print('treerings.py -convert2raw file1 [file2...]')
        print('treerings.py (with no arguments, launches dialog)')
        sys.exit(__doc__)

    elif sys.argv[1] == '-convert2flat':
        FilesIn = [os.path.abspath(arg) for arg in sys.argv[2:] if os.path.isfile(arg)]
        for arg in sys.argv[2:]:
            if not os.path.abspath(arg) in FilesIn:
                print('Argument not vaild: "%s"' % arg)
        for Fin in FilesIn:
            Fout_nm = unique_nm(os.path.splitext(Fin)[0] + '.txt')
            raw2flat(Fin, Fout_nm)

    elif sys.argv[1] == '-convert2raw':
        FilesIn = [os.path.abspath(arg) for arg in sys.argv[2:] if os.path.isfile(arg)]
        for arg in sys.argv[2:]:
            if not os.path.abspath(arg) in FilesIn:
                print('Argument not vaild: "%s"' % arg)
        for Fin in FilesIn:
            Fout_nm = unique_nm(os.path.splitext(Fin)[0] + '.rwl')
            flat2raw(Fin, Fout_nm)

