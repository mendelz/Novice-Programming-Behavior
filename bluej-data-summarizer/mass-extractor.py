import sqlite3, os, sys, re

isEncoded = False

##### WRAPPERS #####

def decode(str):
	if (isEncoded == True):
		return base64.b64decode(str)
	else:
		return str

def search(path):
	# Find only databases that contain compile data.
	db_list = []
	for f in os.listdir(path):
		match = re.search('CompileData', f)
		if match:
			fullpath = '%s%s' % (path, f)
			db_list.append(fullpath)
	
	return db_list
	
def get_name(path):
	# Get the name of the database.	
	name = re.search('.*/(.*?_CompileData)', path)
	if name:
		return name.group(1)


##### SQLITE #####	

def compile_data(path, name):
	# Connect to the database and initialize cursor.
	conn = sqlite3.connect(path)
	cur = conn.cursor()

	# Find the total number of compiles.
	compile_count = 'select count(TOTAL_COMPILES) from ' + name
	cur.execute(compile_count)
	total = cur.fetchone()[0]

	# Find the number of successful compiles.
	success_count = 'select count(COMPILE_SUCCESSFUL) from ' + name + ' where COMPILE_SUCCESSFUL = 1'
	cur.execute(success_count)
	success = cur.fetchone()[0]

	# Find the number of unsuccessful compiles.
	failure_count = 'select count(COMPILE_SUCCESSFUL) from ' + name + ' where COMPILE_SUCCESSFUL = 0'
	cur.execute(failure_count)
	fail = cur.fetchone()[0]
	
	return total, success, fail

def error_data(path, name, compiles):
	global isEncoded
	
	# Connect to the database and initialize cursor.
	conn = sqlite3.connect(path)
	cur = conn.cursor()

	# Find the total number of errors.
	if (isEncoded == True):		  
		error_count = 'select count(MSG_TYPE) from ' + name + ' where MSG_TYPE = "RVJST1I="'
	else:
		error_count = 'select count(MSG_TYPE) from ' + name + ' where MSG_TYPE = "ERROR"'
	cur.execute(error_count)
	count = cur.fetchone()[0]

	# Get a visual summary of compiles.
	error_freq = 'select MSG_TYPE from ' + name
	cur.execute(error_freq)
	error_map = []
	
	for i in range(0, compiles):
		if (decode(cur.fetchone()[0]) == 'ERROR'):
			error_map.append('X')
		else:
			error_map.append('O')

	return count, ''.join(error_map)
	
##### MAIN #####
			
def run(path):	
	db_list = search(path)
	count = 0
	# This is the cool part.
	for f in db_list:
		name = get_name(f)
		count = count + 1
		compiles, successful, unsuccessful = compile_data(f, name)
		errors, error_map = error_data(f, name, compiles)
		print '%s\t%s\t%s\t%s\t%s\t%s' % (count, compiles, successful, unsuccessful, errors, error_map) 
	
run(sys.argv[1])	
