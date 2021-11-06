import argparse
import logging

from lex.neo4j.phrase_dao import PhraseDao

logging.basicConfig(filename='find_match.log', level=logging.DEBUG)


def find_match():
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern',
                        metavar='Pattern to search for',
                        type=str,
                        help='e.g. P_TT__N')

    pattern = parser.parse_args().pattern
    matches = PhraseDao().match(pattern)
    for phrase in matches:
        print(phrase)


if __name__ == '__main__':
    find_match()
