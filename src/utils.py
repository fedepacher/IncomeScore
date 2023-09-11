"""Utils custom function"""
import codecs
import json
import sys
import logging


def notebook_wrapper(logger, file_name=''):
    """Create a py file from ipynb notebook file

    Args:
        logger (CustomLogging): Logging.
        file_mane (str, optional): File name.

    Returns:
        (str): Return python code as string. 
    """
    ipynb_ext = 'ipynb'
    py_ext = 'py'
    try:
        notebook_file = codecs.open(fr'notebooks/{file_name}.{ipynb_ext}', 'r')
        source = notebook_file.read()
        logger.info(f'File {file_name} opened correctly.')
    except FileNotFoundError as err:
        logger.error(f'File {file_name} could not be opened: {err}.')

    notebook_data = json.loads(source)
    py_code = '##Python .py code from .jpynb:\n'
    comment = '#'
    for element in notebook_data['cells']:
        if element['cell_type'] == "markdown":
            comment = '#'
        else:
            comment = ''
        for code in element['source']:
            py_code += comment
            py_code += code
            if code[-1] != '\n':
                py_code = py_code + '\n'

    logger.info(f'File {file_name}.{py_ext} created.')

    return py_code


class CustomLogging:
    """Implement a logging class"""
    def __init__(self, level=logging.INFO) -> None:
        """Constructor"""
        logging.basicConfig(
            format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
            level=level,
            datefmt='%H:%M:%S',
            stream=sys.stderr
        )


    def get_logger(self):
        """Create the logging

        Returns:
            Logger: Return the logger
        """
        return logging.getLogger(__name__)
