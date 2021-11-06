import logging

from neo4j import GraphDatabase

from lex.neo4j.host_config import ConfigLoader

logging.basicConfig(filename='phrase_dao.log', level=logging.DEBUG)


def get_constraints(pattern):
    result = []
    for idx, c in enumerate(pattern):
        if c != '_':
            result.append((c, idx+1))
    return result


def build_condition(constraint):
    glyph, position = constraint
    return "(p)-[:HAS_LETTER {at:%s}]->(:Letter {glyph:'%s'})" % (position, glyph)


def match(tx, pattern):
    length = len(pattern)

    query = "MATCH (p:Phrase {length:%s})" % length

    conditions: list[str] = [build_condition(c) for c in get_constraints(pattern)]

    if conditions:  # not empty
        query += ' WHERE '
        query += ' AND '.join(conditions)

    query += " RETURN p.text"
    logging.debug(query)

    results = tx.run(query)
    return [record["p.text"] for record in results]


# TODO merge LexLoader into this.
class PhraseDao:

    def __init__(self):
        host_config = ConfigLoader().host_config
        if host_config is None:
            logging.error('No host config found. It should be in /lex/neo4j/config.ini')
            return

        uri = host_config.uri
        user = host_config.user
        password = host_config.password

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def match(self, pattern):
        with self.driver.session() as session:
            return session.read_transaction(match, pattern)
