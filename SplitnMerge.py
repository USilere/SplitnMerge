import argparse
import getopt
import logging as log
import sys

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

pars = argparse.ArgumentParser(description='Test run')
pars.add_argument('-A', '--action', type=str, choices=['merge', 'split'], required=True,
                  metavar='', help='Please specify which option to perform')
pars.add_argument('-F', '--file', nargs='+', type=str, required=True,
                  metavar='', help='Choose files to use for this action')
pars.add_argument('--range', nargs=2, type=int,
                  metavar='', help="Please choose range to use. NB: No range"
                  " means split will be done per page")
args = pars.parse_args()

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
log.basicConfig(format=FORMAT, filename="SplitnMerge.log", level=log.DEBUG)
log.debug("Start...")


def merge(pdfs):
    merger = PdfFileMerger()
    log.info("Merging: {}".format(pdfs))
    for pdf in pdfs:
        merger.append(pdf)
    merger.write('MergedDocuments.pdf')
    log.info("Merged: {} to 'MergedDocuments.pdf'")


def split_range(doc, start, end):
    inputpdf = PdfFileReader(open(doc, 'rb'))
    # Taking the first 5 pages of a document
    if start != 0 and end != 0:
        start_page = start
        end_page = end
        try:
            # PyPDF2 starts counting pages from 0
            log.info("Splitting: {} document in ranges".format(doc))
            output = PdfFileWriter()
            for i in range(start_page-1, end_page):
                output.addPage(inputpdf.getPage(i))
            with open('SplitFile1.pdf', 'wb') as outputStream:
                output.write(outputStream)
            outputStream.close()
            log.info(
                "'SplitFile1.pdf' document from range: {} - {} of {}".format(
                    start, end, doc))

        except (IndexError, TypeError):
            log.exception('Please specify correct range')


def split_individual(doc):
    inputpdf = PdfFileReader(open(doc, 'rb'))
    log.info("Splitting: {} document to individual pages".format(doc))
    for l in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(l))
        with open('document %d_pdf.pdf' % (l+1), 'wb') as outputStream:
            output.write(outputStream)
        outputStream.close()
        log.info('Making document %d_pdf.pdf' % (l+1))


if __name__ == '__main__':
    try:
        if args.action == "merge" and len(args.file) > 1:
            log.info("You want to merge: {}" .format(args.file))
            merge(args.file)
        elif args.action == 'split' and len(args.file) == 1 and args.range:
            log.info('You want to split {} using ranges:' .format(args.file))
            split_range(args.file[0], args.range[0], args.range[1])
        elif args.action == 'split' and len(args.file) == 1:
            log.info('You want to split individually: {}' .format(args.file))
            split_individual(args.file[0],)
        else:
            log.error("Wrong action specified, Please specify correct "
                      "required information")
    except (IndexError, TypeError) as e:
        log.exception(
            'Please specify correct required information: ()'.format(e))
