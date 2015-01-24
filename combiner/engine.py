# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

DATABASE = {
        'drivername': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'username': 'vagrant',
        'password': '.',
        'database': 'DP'
}
RAW_DATA_DIR = '../tmp/raw'

DeclarativeBase = declarative_base()

def _db_connect():
    """ Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance """
    if not db_connect.engine:
         db_connect.engine = create_engine(URL(**settings.DATABASE))
    return db_connect.engine

def _create_all_tables(engine):
    DeclarativeBase.metadata.create_all(engine)

def main():
    from argparse import ArgumentParser
    from csv import DictReader
    parser = ArgumentParser(description='Run a combiner')
    parser.add_argument('combiner', type=str, help='the combiner name to be run')
    args = parser.parse_args()
    session = _db_connect()

    try:
        combiner = __import__(args.combiner)
    except ImportError:
        print("combiner '%s' does not exist" % args.combiner)
        raise
    requested_data = combiner.raw_data

    files = []
    try:
        # Accumulator pattern is needed in this case
        for f in requested_data:
            f = RAW_DATA_DIR + '/' + f + '.csv'
            files.append(open(f, 'r', encoding='utf8'))
            data = map(DictReader, files)
            data = namedtuple(args.combiner + '_data', requested_data)(data)
        for item in combiner.combine(data):
            _send_to_db(session, item)
    finally:
        for f in files: f.__exit__()

def _send_to_db(session, item):
    try:
        session.add(item)
        session.commit()
    except:
        session.rollback()
        raise


if __name__ == '__main__':
    main()
