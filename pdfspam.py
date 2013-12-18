#!/usr/bin/env python
'''
PDFSPAM
=======

A very basic re-implementation of _[pdfsandwich][1]_ in Python.

[1]: http://www.tobias-elze.de/pdfsandwich/
'''


def run(fin, fout=None, v=False, no_cleanup=False):
    import os
    import shutil
    import sys

    if not os.path.isfile(fin):
        print 'Cannot read file "{}". Aborting.'.format(fin)
        return

    if fout is None:
        chunks = fin.rpartition('.')
        chunks = chunks[0]  + '_ocr' + chunks[1] + chunks[2]
        fout = ''.join(chunks)

    fout = os.path.abspath(fout)
    fin = os.path.abspath(fin)

    if os.path.isfile(fout):
        print '"{}" already exists. Aborting.'.format(fout)
        return

    cache = os.path.dirname(fin)
    cache = os.path.join(cache, 'pdfspam_cache')
    try:
        os.mkdir(cache)
    except OSError:
        print 'Cannot create temporary cache directory. Aborting.'
        return

    cmd = {'pdf2png': 'convert -type Bilevel -density 300x300 {fin}[{idx}] png:{cache}/{idx}.png',
           'ocr': 'tesseract {page}.png {page} -l eng hocr',
           'png2bmp': 'convert {page}.png {page}.bmp',
           'hocr2pdf': 'hocr2pdf -i "{page}.bmp" -o "{page}.pdf" < "{page}.html"',
           'join_pdf': 'gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="{fout}" {pages}',
           }

    print 'Splitting up pdf to individual pages...'

    
    idx = 0
    while not _do(cmd['pdf2png'].format(cache=cache, fin=fin, idx=idx),v):
        sys.stdout.write('..')
        sys.stdout.flush()
        idx += 1
    
    print '\n{} pages detected.'.format(idx)

    pages = [cache+'/'+s.rpartition('.')[0] for s in os.listdir(cache)]
    
    for page in pages:
        _do(cmd['ocr'].format(cache=cache, page=page),v)
        sys.stdout.write('.')
        sys.stdout.flush()
        _do(cmd['png2bmp'].format(page=page),v)
        _do(cmd['hocr2pdf'].format(page=page),v)
        sys.stdout.write('.')
        sys.stdout.flush()
    
    pagelist = ' '.join([p+'.pdf' for p in pages])
    _do(cmd['join_pdf'].format(cache=cache, fout=fout, pages=pagelist),v)

    if not no_cleanup:
        shutil.rmtree(cache)
    print '\ndone.'


def _do(cmd, verbose):
    if verbose:
        print '$ '+cmd
    import subprocess
    # dirty way:
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if verbose:
        print output
        print err
    ret = process.wait()
    if verbose:
        print '-> {}'.format(ret)
    return ret

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='creating sandwich-pdfs with searchable text')
    parser.add_argument('input', help='the .pdf-file to do convert')
    parser.add_argument('-o', '--output', help='name of the converted .pdf', default=None)
    parser.add_argument('-v', '--verbose', help='print every tool invocation',
                        default=False, action='store_true')
    parser.add_argument('-nc', '--no-cleanup', help='leave cache directory behind',
                        default=False, action='store_true')
    args = parser.parse_args()
    run(args.input, args.output, args.verbose, args.no_cleanup)
