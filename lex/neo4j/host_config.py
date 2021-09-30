import configparser
import logging
from dataclasses import dataclass

logging.basicConfig(filename='host_config.log', level=logging.DEBUG)


@dataclass
class HostConfig:
    uri: str
    user: str
    password: str


class ConfigLoader:

    host_config: HostConfig

    def __init__(self):
        parser = configparser.ConfigParser()
        read = parser.read('lex/neo4j/config.ini')
        logging.debug(f'Config files read: {read}')

        uri = parser.get('Neo4jHost', 'uri')
        user = parser.get('Neo4jHost', 'user')
        password = parser.get('Neo4jHost', 'password')

        self.host_config = HostConfig(uri, user, password)
