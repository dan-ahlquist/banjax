import logging

from neo4j import GraphDatabase

from lex.neo4j.host_config import ConfigLoader

logging.basicConfig(filename='loader.log', level=logging.DEBUG)
ALPHA_EN = 'abcdefghijklmnopqrstuvwxyz'


def create_phrase(tx, phrase):
    query = "MERGE (:Phrase {text:'%s', length:%s})" % (phrase, len(phrase))
    logging.debug(query)
    tx.run(query)


def relate_letters(tx, phrase):
    for idx, c in enumerate(phrase):
        query = ("MATCH (p:Phrase {text:'%s'}) "
                 "MATCH (l:Letter {glyph:'%s'}) "
                 "MERGE (p)-[:HAS_LETTER {at:%s}]->(l)") % (phrase, c, idx+1)
        logging.debug(query)
        tx.run(query)


def create_letter(tx, char):
    query = "MERGE (:Letter {glyph:'%s'})" % char
    logging.debug(query)
    tx.run(query)


class LexLoader:

    def __init__(self):
        host_config = ConfigLoader().host_config
        if host_config is None:
            logging.error('No host config found. It should be in /lex/neo4j/config.ini')
            return

        uri = host_config.uri
        user = host_config.user
        password = host_config.password

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def setup_db(self):
        self.__add_constraints()
        self.__clear_data()

    def __add_constraints(self):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run("CREATE CONSTRAINT IF NOT EXISTS ON (phrase:Phrase) ASSERT (phrase.text) IS NOT NULL;")
                tx.run("CREATE CONSTRAINT IF NOT EXISTS ON (phrase:Phrase) ASSERT (phrase.text) IS UNIQUE;")
                tx.run("CREATE CONSTRAINT IF NOT EXISTS ON (letter:Letter) ASSERT (letter.glyph) IS UNIQUE;")
                tx.run("CREATE CONSTRAINT IF NOT EXISTS ON (letter:Letter) ASSERT (letter.glyph) IS NOT NULL;")
                tx.commit()

    def __clear_data(self):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run("MATCH (n) DETACH DELETE n")
                tx.commit()

    def create_alphabet_nodes(self, alphabet=ALPHA_EN):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                for c in alphabet:
                    create_letter(tx, c)
                tx.commit()

    def create_phrases(self, phrases):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                for phrase in phrases:
                    create_phrase(tx, phrase)
                    relate_letters(tx, phrase)
                tx.commit()
