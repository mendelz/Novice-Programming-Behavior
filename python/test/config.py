#########################################
# ONLY MODIFY THESE VARIABLES
#########################################
# You should only need to modify these 
# variables for the collection of data.

# Choose the IP address of the server that
# is hosting this script. "localhost" will 
# prevent machines elsewhere on the 
# network from logging data.
serverAddress = 'aldenv187.allegheny.edu'

# Choose the port that you wish to run the 
# server on. Anything over 1024 should be fine.
serverPort = 12345

# Remote operation password
# If you want to be able to start and stop the server 
# remotely, then you'll need to set this
# "password"
controlPassword = 'changeme'

# Time between tests.
sleepTime = 0

# Number of Test Clients (Number of databases to test)
testCount = 50

# Number of submissions per client (Number of database inserts to commit)
submitCount = 500

# Name of client (or possibly user) that is creating and populating the databases
clientName = 'Zach'
