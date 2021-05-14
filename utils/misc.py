import os
import subprocess


def get_filename(filepath):
    parts = os.path.split(filepath)
    return parts[1].split('.')[0]  # handle extension if exists


def remove_pdf_password(pdfpath, outfilepath):
    subprocess.run([
        'pdftops',
        '-upw',
        os.environ['CREDIT_CARD_STATEMENT_PDF_PASSWORD'],
        pdfpath,
        outfilepath
    ], check=True)

    return outfilepath


def extract_pdf_first_page(
    pdfpath,
    outfilepath,
    try_fix=True,
    remove_original=False
):
    try:
        subprocess.run([
            'pdfseparate',
            '-f',
            '1',
            '-l',
            '1',
            pdfpath,
            outfilepath
        ], check=True)
    except subprocess.CalledProcessError as err:
        if not try_fix:
            raise err

        # try to fix the file with ghostscript, then attempt
        #   to extract the first page again
        pdffilename = get_filename(pdfpath)
        repairedfilepath = pdfpath.replace(
            pdffilename, f"{pdffilename}-repaired")
        subprocess.run([
            'gs',
            '-o',
            repairedfilepath,
            '-sDEVICE=pdfwrite',
            '-dPDFSETTINGS=/prepress',
            pdfpath
        ], check=True)

        return extract_pdf_first_page(
            repairedfilepath, outfilepath, try_fix=False, remove_original=True)

    if remove_original:
        os.remove(pdfpath)

    return outfilepath
