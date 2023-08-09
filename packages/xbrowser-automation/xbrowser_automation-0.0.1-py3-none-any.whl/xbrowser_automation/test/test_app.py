
from importlib.resources import files as resources_files

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def test_notebook():
    folder = resources_files('xbrowser_automation')
    notebook_filename = folder / 'xbrowser_automation.ipynb'
    with open(notebook_filename, encoding='utf8') as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor()
    ep.preprocess(nb, {'metadata': {'path': folder}})
