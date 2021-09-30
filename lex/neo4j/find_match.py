import argparse
import logging

from lex.neo4j.host_config import ConfigLoader
from lex.neo4j.phrase_dao import PhraseDao

logging.basicConfig(filename='find_match.log', level=logging.DEBUG)


def find_match():
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern',
                        metavar='Pattern to search for',
                        type=str,
                        help='e.g. P_TT__N')

    pattern = parser.parse_args().pattern
    host_config = ConfigLoader().host_config
    if host_config is None:
        logging.error('No host config found. It should be in /lex/neo4j/config.ini')
        return

    uri = host_config.uri
    user = host_config.user
    password = host_config.password

    matches = PhraseDao(uri, user, password).match(pattern)
    for phrase in matches:
        print(phrase)


if __name__ == '__main__':
    find_match()
