import sqlite3, base64, sys

isEncoded = False

# Decode only if encoded
def decode(str):
	if (isEncoded == True):
		return base64.b64decode(str)
	else:
		return str

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
	
	#return 'Total Compiles: %s \nSuccessful: %s\tUnsuccessful: %s' % (total, success, fail)
	return total, success, fail
	
def error_data(path, name):
	global isEncoded
	
	# Connect to the database and initialize cursor.
	conn = sqlite3.connect(path)
	cur = conn.cursor()
	
	# First query: find the total number of errors.
	if (isEncoded == True):		  
		error_count = 'select count(MSG_TYPE) from ' + name + ' where MSG_TYPE = "RVJST1I="'
	else:
		error_count = 'select count(MSG_TYPE) from ' + name + ' where MSG_TYPE = "ERROR"'
	cur.execute(error_count)
	count = cur.fetchone()[0]

	# Second query: list all error messages.
	error_message = 'select MSG_MESSAGE from ' + name + ' where MSG_MESSAGE != ""'
	cur.execute(error_message)
	messages = []
	
	for i in range(0, count):
		messages.append(decode(cur.fetchone()[0]))
			
	# Third query: get a visual summary of compiles	
	error_freq = 'select MSG_TYPE from ' + name
	cur.execute(error_freq)
	error_map = []
	
	for i in range(0, 24):
		if (decode(cur.fetchone()[0]) == 'ERROR'):
			error_map.append('X')
		else:
			error_map.append('O')	
		
	return 'Total Errors: %s\nError Messages:\n%s\nCompilation Summary:\n%s' \
	  % (count, messages, ''.join(error_map))
	
	
#total, success, fail = compile_data(sys.argv[1], sys.argv[2])
#print 'Total Compiles: %s \nSuccessful: %s\tUnsuccessful: %s' % (total, success, fail)
#print compile_data(sys.argv[1], sys.argv[2])
print error_data(sys.argv[1], sys.argv[2])
