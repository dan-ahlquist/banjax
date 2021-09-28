# Banjax: a crossword generator

Generate crossword puzzle grids (clues sold separately).

## Dependencies

* A [Neo4j installation](https://neo4j.com/developer/get-started/) (graph DBMS)
* [Neo4j Python driver](https://neo4j.com/developer/python/)
  * `pip install neo4j` 

## Setup & Usage 

* Copy `lex/neo4j/config_sample.ini` as `lex/neo4j/config.ini` and update the database credentials.
* Load some phrases.
  * A phrase is one or more words together, with no spaces.
  * `python3 lex/neo4j/load.py your_dictionary.dat`
* Coming soon: generate a puzzle!