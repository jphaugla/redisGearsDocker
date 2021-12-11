from rgsync import RGWriteBehind, RGWriteThrough
from rgsync.Connectors import MySqlConnector, MySqlConnection

'''
Create MySQL connection object
'''
connection = MySqlConnection('demouser', 'jasonrocks', 'mysql:3306/test')

'''
Create MySQL persons connector
'''
personsConnector = MySqlConnector(connection, 'persons', 'person_id')

personsMappings = {
	'first_name':'first',
	'last_name':'last',
	'age':'age'
}

RGWriteBehind(GB,  keysPrefix='person', mappings=personsMappings, connector=personsConnector, name='PersonsWriteBehind',  version='99.99.99')

RGWriteThrough(GB, keysPrefix='__',     mappings=personsMappings, connector=personsConnector, name='PersonsWriteThrough', version='99.99.99')
