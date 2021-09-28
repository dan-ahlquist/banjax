import argparse
import logging

from host_config import ConfigLoader
from lex_loader import LexLoader

logging.basicConfig(filename='loader.log', level=logging.DEBUG)


def load():
    parser = argparse.ArgumentParser(description='Load phrases into the banjax-lex database.')
    parser.add_argument('dict_file_name',
                        metavar='Input file',
                        type=str,
                        help='Newline-delimited file with phrases to be loaded.')

    args = parser.parse_args()
    dict_file_name = args.dict_file_name

    host_config = ConfigLoader().host_config
    if host_config is None:
        logging.error('No host config found. It should be in /lex/neo4j/config.ini')
        return

    uri = host_config.uri
    user = host_config.user
    password = host_config.password

    with open(dict_file_name, 'r') as file:
        lex = [line.strip() for line in file.readlines()]

    logging.info(f'Read in {len(lex)} phrases from {dict_file_name}.')

    loader = LexLoader(uri, user, password)
    loader.setup_db()
    loader.create_alphabet_nodes()
    loader.create_phrases(lex)
    loader.close()


if __name__ == '__main__':
    load()
