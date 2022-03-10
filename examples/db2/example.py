from rgsync import RGWriteBehind, RGWriteThrough
from rgsync.Connectors import DB2Connector, DB2Connection



'''
Create Postgres connection object
'''
connection = DB2Connection('db2inst1', 'jasonrocks', 'localhost:50000/SAMPLE')

'''
Create Postgres employee connector
'''
employeeConnector = DB2Connector(connection, 'EMPLOYEE', 'EMPNO')

employeeMappings = {
	'FIRSTNME':'first',
	'LASTNAME':'last',
	'MIDINIT':'middle'
}

RGWriteBehind(GB,  keysPrefix='EMPLOYEE', mappings=employeeMappings, connector=employeeConnector, name='EmployeeWriteBehind',  version='99.99.99')

RGWriteThrough(GB, keysPrefix='__',     mappings=employeeMappings, connector=employeeConnector, name='EmployeeWriteBehind', version='99.99.99')
