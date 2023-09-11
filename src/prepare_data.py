"""Prepara data to train the model"""
import argparse
from utils import CustomLogging, notebook_wrapper


if __name__ == '__main__':
    logging = CustomLogging()
    logger = logging.get_logger()

    logger.info('Fetching data...')

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('-f', '--filename', metavar='<filename>', type=str, required=True,
                            default='', help='Filename', dest='filename')

    args = arg_parser.parse_args()
    filename = args.filename
    # Run script
    exec(notebook_wrapper(file_name=filename, logger=logger).replace('../', './'))
    logger.info('Data Fetched and prepared...')
