import configparser
from dataclasses import dataclass


@dataclass
class HostConfig:
    uri: str
    user: str
    password: str


class ConfigLoader:

    host_config: HostConfig

    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read('lex/neo4j/config.ini')

        uri = parser.get('Neo4jHost', 'uri')
        user = parser.get('Neo4jHost', 'user')
        password = parser.get('Neo4jHost', 'password')

        self.host_config = HostConfig(uri, user, password)
