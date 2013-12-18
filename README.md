PDFSPAM
=======

A very basic re-implementation of _[pdfsandwich][1]_ in Python, since

- The given implementation didn't work on my system
- All the tool invocations were nicely logged in verbose mode
- Python was the easiest way to reach my goal

From Tobias Elze's [website][1]:

[1]: http://www.tobias-elze.de/pdfsandwich/

> pdfsandwich is a command line tool which is supposed to be useful to
> OCR scanned books or journals. It is able to recognize the page layout
> even for multicolumn text.

> Essentially, pdfsandwich is a wrapper script which calls the following
> binaries: convert, gs, hocr2pdf, and tesseract. It is known to run on
> Unix systems and has been tested on Linux and MacOS X. It supports
> parallel processing on multiprocessor systems.

Feel free to use & modify!

TODO
----
- Check and help for not-installed third party tools
- Core estimation with multiprocessing.cpu_count(), do the whole multiprocessor stuff
