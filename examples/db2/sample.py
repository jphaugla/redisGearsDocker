from rgsync.Connectors.sql_connectors import BaseSqlConnection
from rgsync.Connectors import OracleSqlConnector
from rgsync import RGWriteBehind, RGWriteThrough

class DB2Connection(BaseSqlConnection):
    def __init__(self, user, passwd, db):
        BaseSqlConnection.__init__(self, user, passwd, db)
    def _getConnectionStr(self):
        return 'db2://{user}:{password}@{db}'.format(user=self.user, password=self.passwd, db=self.db)
class DB2Connector(OracleSqlConnector):
    def __init__(self, connection, tableName, pk, exactlyOnceTableName=None):
        OracleSqlConnector.__init__(self, connection, tableName, pk, exactlyOnceTableName)    
    def PrepereQueries(self, mappings):
        values = [val for kk, val in mappings.items() if not kk.startswith('_')]
        values_with_pkey = [self.pk] + values
    def GetUpdateQuery(table, pkey, values_with_pkey, values):
        merge_into = "MERGE INTO %s d USING (VALUES 1) ON (d.%s = :%s)" % (table, pkey, pkey)
        not_matched = "WHEN NOT MATCHED THEN INSERT (%s) VALUES (%s)" % (','.join(values_with_pkey), ','.join([':%s' % a for a in values_with_pkey]))
        matched = "WHEN MATCHED THEN UPDATE SET %s" % (','.join(['%s=:%s' % (a,a) for a in values]))
        query = "%s %s %s" % (merge_into, not_matched, matched)
        return query

        self.addQuery = GetUpdateQuery(self.tableName, self.pk, values_with_pkey, values)
        self.delQuery = 'delete from %s where %s=:%s' % (self.tableName, self.pk, self.pk)
        if self.exactlyOnceTableName is not None:
            self.exactlyOnceQuery = GetUpdateQuery(self.exactlyOnceTableName, 'id', ['id', 'val'], ['val'])
            connection = DB2Connection('db2inst1', 'jasonrocks', '127.0.0.1:50000/SAMPLE')

            empConnector = DB2Connector(connection, 'EMPLOYEE', 'EMPNO')
            empMappings = {
                'FIRSTNME': 'first',
                'LASTNAME': 'last',
                'MIDINIT': 'middle'
            }
            RGWriteBehind(GB, keysPrefix='emp', mappings=empMappings, connector=empConnector, name='empWriteBehind',
              version='99.99.99')
