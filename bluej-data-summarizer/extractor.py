import sqlite3, base64, sys

# Connect to the database, get everything, and decode it
def dump(path, name):
	conn = sqlite3.connect(path)
	cur = conn.cursor()
	
	s = 'select * from ' + name
	
	cur.execute(s)
	result = cur.fetchall()
	for i in range(0, len(result)):
		for j in range(26, 27):
			return base64.b64decode(result[i][j])

def compile_data(path, name):
	# Connect to the database and initialize cursor.
	conn = sqlite3.connect(path)
	cur = conn.cursor()
	
	# First query: find the total number of compiles.
	compile_count = 'select count(TOTAL_COMPILES) from ' + name
	cur.execute(compile_count)
	total = cur.fetchone()[0]
	
	# Second query: find all successful compiles.
	success_count = 'select count(COMPILE_SUCCESSFUL) from ' + name + ' where COMPILE_SUCCESSFUL = 1'
	cur.execute(success_count)
	success = cur.fetchone()[0]
	
	# Third query: find all failed compiles.
	failure_count = 'select count(COMPILE_SUCCESSFUL) from ' + name + ' where COMPILE_SUCCESSFUL = 0'
	cur.execute(failure_count)
	fail = cur.fetchone()[0]
	
	return 'Total Compiles: %s \nSuccessful: %s\tUnsuccessful: %s' % (total, success, fail)
	
def error_data(path, name):
	# Connect to the database and initialize cursor.
	conn = sqlite3.connect(path)
	cur = conn.cursor()
	
	# First query: find the total number of errors.		  
	error_count = 'select count(MSG_TYPE) from ' + name + ' where MSG_TYPE = "RVJST1I="'
	cur.execute(error_count)
	count = cur.fetchone()[0]

	# Second query: list all error messages.
	error_message = 'select MSG_MESSAGE from ' + name + ' where MSG_MESSAGE != ""'
	cur.execute(error_message)
	messages = []
	
	for i in range(0, count):
		messages.append(base64.b64decode(cur.fetchone()[0]))
		
	return 'Total Errors: %s\nError Messages:\n%s' % (count, messages)
	
		
print error_data(sys.argv[1], sys.argv[2])	
print compile_data(sys.argv[1], sys.argv[2])
# print dump('/Users/ZMAN/researchs2011/pyserver/Calculator-Data/bluej/Allegheny_CompileData-068e2c36173a3b1aaf893605be2f85a8.sqlite', 'Allegheny_CompileData')	