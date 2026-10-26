"""Finds the newest ConfTool export (adminPapersBrowse_YYYY-MM-DD_HH-MM-SS.doc) in this folder."""
import glob
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))


def latest_doc():
    files = glob.glob(os.path.join(_HERE, 'adminPapersBrowse_*.doc'))
    files = [f for f in files if re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', f)]
    if not files:
        raise FileNotFoundError('No adminPapersBrowse_*.doc file found')
    return os.path.basename(max(files, key=lambda f: re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', f).group(0)))


SOURCE_DOC = latest_doc()
