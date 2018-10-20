
# TREERINGS
Convert dendrochonology data files between flat and decadal formats.
Functions to convert files between decadal and flat formats.

* Version 1.0

> Decadal, raw data, format:  
> 
>     Core ID  Decade  Measurement(s)  [Site ID]  
>     col 1-6   9-12      13-72            74-78
> source:  
>    [NOAA Treering info](ftp://ftp.ncdc.noaa.gov/pub/data/paleo/treering/treeinfo.txt)  
>
>    [MeasureJ2X User Guide, Appendix 1](http://www.voortech.com/projectj2x/docs/userGuide.htm#Appendix 1.)  
- - - 
> Flat, column, format:  
>
>     Core ID   Year  Measurement  [Site ID]  
>     col 1-6   9-12      13-18      20-24  

### Description ###

* treerings.py and treerings.pyw contain the working code.
* convert2raw.py and convert2flat.py are one-way conversion scripts for easy command-line interaction.
* Dependencies:
    Tkinter


### Who do I talk to? ###

* Paul Sowers  
    sowerspa@gmail.com
