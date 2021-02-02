from cx_Oracle import ProgrammingError
from util.logger import logger
from util.readconfig import db_url
from util.readconfig import db_type
import cx_Oracle


class Oracle(object):
    def __init__(self,db_url):
        """db_url: connection path format
            db_url  eg: PROMOTION/PROMOTION@172.31.6.234:1521/TESTDB
        """
        try:
            self._conn = cx_Oracle.connect(db_url)
            self._cursor = self._conn.cursor()
        except Exception as e:
            logger.exception(e)

    def dict_fetchall(self, sql):
        """Return all rows from a cursor as a dict"""
        try:
            self._cursor.execute(sql)
            logger.debug("DBSQLSTATEMENT - %s" % sql)
            columns = [col[0] for col in self._cursor.description]
            result = [dict(zip(columns, row)) for row in self._cursor.fetchall()]
            logger.debug("DBRESULTS - %s" % result)
            return result
        except ProgrammingError as e:
            logger.exception(e)

    def select(self,sql):
        try:
            self._cursor.execute(sql)
            logger.debug("DBSQLSTATEMENT - %s" % sql)
            result = self._cursor.fetchall()
            logger.debug("DBRESULTS - %s" % result)
            return result
        except ProgrammingError as e:
            logger.exception(e)

    def insert(self):
        pass

    def update(self):
        pass

    def close(self):
        self._cursor.close()
        self._conn.close()



oracle = None
if db_type == 'Oracle':
    oracle = Oracle(db_url)
else:
    oracle = Oracle(db_url)