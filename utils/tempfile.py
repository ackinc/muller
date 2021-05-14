import os


def get_tempfile_name(tmpfile):
    tmpfilenameparts = os.path.split(tmpfile.name)
    return tmpfilenameparts[1].split('.')[0]  # handle extension if exists
