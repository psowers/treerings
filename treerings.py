#!/usr/bin/env python
"""
Functions to convert files between decadal and flat formats.

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

import tkinter

__author__ = 'Paul Sowers <sowerspa@gmail.com>'


class TkTreeRingDialog(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)
        root.title('Tree Ring Raw Data Flattner')

        frame_opt = {'expand': tkinter.constants.TRUE, 'fill': tkinter.constants.X}
        self.frmInput = tkinter.Frame(self)
        self.frmOutput = tkinter.Frame(self)
        self.frmExecute = tkinter.Frame(self)
        self.frmInput.pack(**frame_opt)
        self.frmOutput.pack(**frame_opt)
        self.frmExecute.pack(expand=tkinter.constants.TRUE, fill=tkinter.constants.BOTH)

        # define filename variables
        self.filename_in = tkinter.StringVar()
        self.filename_out = tkinter.StringVar()

        # pack options
        button_opt = {'fill': tkinter.constants.BOTH, 'padx': 5, 'pady': 5, 'side': tkinter.constants.LEFT}
        entry_opt = {'expand': tkinter.constants.TRUE, 'fill': tkinter.constants.X,
                     'padx': 5, 'pady': 5, 'side': tkinter.constants.LEFT}

        # define buttons and entry boxes
        self.label_opt = options = {}
        options['width'] = 25
        options['state'] = 'readonly'
        self.lblIn = tkinter.Entry(self.frmInput, text='Input Filename', textvariable=self.filename_in,
                                   **self.label_opt)
        self.lblIn.pack(**entry_opt)
        tkinter.Button(self.frmInput, text='Input', command=self.ask_inputfilename, width=8).pack(**button_opt)
        self.lblOut = tkinter.Entry(self.frmOutput, text='Output Filename', textvariable=self.filename_out,
                                    **self.label_opt)
        self.lblOut.pack(**entry_opt)
        tkinter.Button(self.frmOutput, text='Output', command=self.ask_outputfilename, width=8).pack(**button_opt)
        tkinter.Button(self.frmExecute, text='Convert to Flat', command=self.convert2flat, width=25).pack(**button_opt)
        tkinter.Button(self.frmExecute, text='Convert to Raw Decadal', command=self.convert2raw, width=25).pack(
            **button_opt)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = ''  # couldn't figure out how this works
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('raw files', '.rwl')]
        options['initialdir'] = os.getcwd()
        options['parent'] = root
        options['title'] = 'This is a title'

    def ask_inputfilename(self):
        # get filename
        options = self.file_opt.copy()
        options['title'] = 'Input Filename ...'
        self.filename_in.set(tkinter.filedialog.askopenfilename(**options))
        self.lblIn.config(state=tkinter.constants.NORMAL)
        self.lblIn.delete(0, tkinter.constants.END)
        self.lblIn.insert(tkinter.constants.END, self.filename_in.get())
        self.lblIn.config(state='readonly')
        self.lblIn.xview_moveto(1.0)

    def ask_outputfilename(self):
        # get filename
        options = self.file_opt.copy()
        options['title'] = 'Output Filename ...'
        self.filename_out.set(tkinter.filedialog.asksaveasfilename(**options))
        self.lblOut.config(state=tkinter.constants.NORMAL)
        self.lblOut.delete(0, tkinter.constants.END)
        self.lblOut.insert(tkinter.constants.END, self.filename_out.get())
        self.lblOut.config(state='readonly')
        self.lblOut.xview_moveto(1.0)

    def convert2flat(self):
        filename_in = self.filename_in.get()
        filename_out = self.filename_out.get()
        if filename_in and filename_out:
            # print(filename_in, filename_out)
            raw2flat(filename_in, filename_out)
            self.quit()

    def convert2raw(self):
        filename_in = self.filename_in.get()
        filename_out = self.filename_out.get()
        if filename_in and filename_out:
            # print(filename_in, filename_out)
            flat2raw(filename_in, filename_out)
            self.quit()


def promptfile():
    """Prompts user for input file path, returns when user input mathes a file."""
    f = input('Enter the input file name and path:\n')
    if os.path.isfile(f):
        return f
    else:
        promptfile()


def is_readable(filename):
    """Tries to open the input file, result is a boolean"""
    try:
        f = open(filename)
        f.close()
        print('File "%s" successfully opened.' % filename)
        return True
    except IOError:
        print('File error: "%s"' % filename)
        return False


def unique_nm(filename):
    """returns a unique filename"""
    from time import localtime
    from random import randint
    if os.path.isfile(filename):
        name, ext = os.path.splitext(filename)
        tag = [('%s.%s' % (dyr, yr)) for yr, mo, d, h, mn, s, wd, dyr, sav in [localtime()]][0]
        _filename = name + tag + ext
        if os.path.isfile(_filename):
            i = 0
            while i < 10:
                _filename = name + tag + ('-%s' % i) + ext
                if not os.path.isfile(_filename):
                    return _filename
                i += 1
            tag = tag + '-' + str(randint(0, 99)).rjust(2, '0')
            _filename = name + tag + ext
            if os.path.isfile(_filename):
                unique_nm(filename)
            else:
                return _filename
        else:
            return _filename
    else:
        return filename
        # tag = tag + ('-%s' % randint(0,9))
        # _filename = name + tag + '.txt'


def raw2flat(file_in, file_out):
    """Reads the decadal input file and writes it to the system in a flat format text file."""
    print('Output:\t"%s"' % file_out)
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

    if len(sys.argv) == 1:
        main = tkinter.Tk()
        app = TkTreeRingDialog(main)
        app.pack(expand=tkinter.constants.TRUE, fill=tkinter.constants.BOTH)
        main.mainloop()

    elif sys.argv[1] in ['-h', '--help', '-help']:
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
            if is_readable(Fin):
                Fout_nm = unique_nm(os.path.splitext(Fin)[0] + '.txt')
                raw2flat(Fin, Fout_nm)

    elif sys.argv[1] == '-convert2raw':
        FilesIn = [os.path.abspath(arg) for arg in sys.argv[2:] if os.path.isfile(arg)]
        for arg in sys.argv[2:]:
            if not os.path.abspath(arg) in FilesIn:
                print('Argument not vaild: "%s"' % arg)
        for Fin in FilesIn:
            if is_readable(Fin):
                Fout_nm = unique_nm(os.path.splitext(Fin)[0] + '.rwl')
                flat2raw(Fin, Fout_nm)

    else:
        print('Invalid arguments. Launching dialog.')
        main = tkinter.Tk()
        app = TkTreeRingDialog(main)
        app.pack(expand=tkinter.constants.TRUE, fill=tkinter.constants.BOTH)
        main.mainloop()
