#Daniela Castorena
#CS 457
#Main driver file
#same code from previous project assignments

import os
import sys

import dbutils
import tableutils
import queryutils
import joinutils

workingDB = None
UserQuery = ""
TableList = [None]
CommandsToExecuteOnCommit = []
BreakFlag = 0
isLocked = 1
userMadeLock = 0

def commandProcessing():
  global workingDB
  global userMadeLock
  global isLocked
  #global CommandsToExecuteOnCommit

  if (';' not in UserQuery and UserQuery.upper() != ".EXIT"): # Invalid command
    print("Commands must end with ';'")
  
  # Creates database
  elif ("CREATE DATABASE" in UserQuery.upper()):
    dbName = dbutils.inputCleaner("CREATE DATABASE ", UserQuery)
    if dbutils.databaseExistenceCheck(dbName) == 0:
      os.system(f'mkdir {dbName}')
      print(f"Database {dbName} created.")
    else:
      print(f"Could not create database {dbName} because it already exists.")
  
  # Deletes database
  elif ("DROP DATABASE" in UserQuery.upper()):
    dbName = dbutils.inputCleaner("DROP DATABASE ", UserQuery)
    if dbutils.databaseExistenceCheck(dbName):
      os.system(f'rm -r {dbName}')
      print(f"Removed database {dbName}.")
    else:
      print(f"Could not remove database {dbName} because it does not exist.")
  
  # Sets currently active database
  elif ("USE" in UserQuery.upper()):
    workingDB = dbutils.inputCleaner("USE ", UserQuery)
    #os.system('cd ' + workingDB)
    if dbutils.databaseExistenceCheck(workingDB):
      print(f"Using database {workingDB}.")
    else:
      print(f"Could not use database {workingDB} because it does not exist.")

  # Creates a table with specified name and attributes
  elif ("CREATE TABLE" in UserQuery.upper()):
    # Splits input into separate strings
    tInput = dbutils.inputCleaner("CREATE TABLE ", UserQuery).replace("create table ", "")
    tName = tInput.split()[0] # Grabs table name
    tRest = tInput.replace(tName, "")
    tAttrs0 = tRest[2:] # Leaves only string with attributes
    tAttrs1 = tAttrs0[:-1] # See above
    tAttrs = tAttrs1.split(",") # Creates list from attributes

    if (workingDB != None):
      if dbutils.tableExistenceCheck(tName, workingDB) == 0:
        os.system(f'touch {workingDB}/{tName}.txt')
        filename = workingDB + '/' + tName + '.txt'
        f = open(filename, 'w')
        f.write(" |".join(tAttrs)) # Writes list to file with pipe delimiter
        f.close()
        print(f"Table {tName} created.")
      else:
        print(f"Could not create table {tName} because it already exists.")
    else:
      print("Please specify which database to use.")

  #delete
  elif ("DROP TABLE" in UserQuery.upper()):
    tName = dbutils.inputCleaner("DROP TABLE ", UserQuery)
    if (workingDB != None):
      if dbutils.tableExistenceCheck(tName, workingDB):
        if isLocked == 0:
          if userMadeLock:
            CommandsToExecuteOnCommit.append(f'rm {workingDB}/{tName}.txt')
          else:
            os.system(f'rm {workingDB}/{tName}.txt')
          print(f"Removed table {tName} from database {workingDB}.")
        else:
          print(f"Error: Table {tName} is locked!")
      else:
        print(f"Could not remove table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  elif ("SELECT" in UserQuery.upper()):
    if ("SELECT *" in UserQuery.upper()):
      if ("." in UserQuery.upper()):
        joinutils.joinTableOpener(UserQuery, workingDB)
      else:
        queryutils.queryAll(UserQuery, workingDB)
    else:
      queryutils.querySpecific(UserQuery, workingDB)

  elif ("ALTER TABLE" in UserQuery.upper()):
    alter = dbutils.inputCleaner("ALTER TABLE ", UserQuery)
    tName = alter.split()[0] 
    alterCmd = alter.split()[1] 
    alterRest1 = alter.replace(tName, "")
    alterRest2 = alterRest1.replace(alterCmd, "") 
    newAttr = alterRest2[2:] 

    if workingDB != None:
      if dbutils.tableExistenceCheck(tName, workingDB):
        if isLocked == 0:
          f = open(f'{workingDB}/{tName}.txt', 'a')
          f.write(f" | {newAttr}") #sppends attribute to file with pipe delimiter
          f.close()
          print(f"Modified table {tName}.")
        else:
          print(f"Error: Table {tName} is locked!")
      else:
        print(f"Could not modify table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  elif ("INSERT INTO" in UserQuery.upper()):
    tableutils.insertTuple(UserQuery, workingDB, isLocked, userMadeLock, CommandsToExecuteOnCommit)
  
  elif ("UPDATE" in UserQuery.upper()):
    tableutils.updateTuple(UserQuery, workingDB, isLocked, userMadeLock, CommandsToExecuteOnCommit)
  
  elif ("DELETE FROM" in UserQuery.upper()):
    tableutils.deleteTuple(UserQuery, workingDB, isLocked, userMadeLock, CommandsToExecuteOnCommit)
  
  elif ("BEGIN TRANSACTION" in UserQuery.upper()):
    userMadeLock = dbutils.makeLock(workingDB)
    print("Transaction starts.")
  
  elif ("COMMIT" in UserQuery.upper()):
    if userMadeLock:
      dbutils.releaseLock(workingDB, CommandsToExecuteOnCommit)
      print("Transaction committed.")
    else:
      print("Transaction abort.")
    userMadeLock = 0

  elif ("DEL" in UserQuery):
    os.system('rm -r CS457_PA4')
  
  elif (".EXIT" != UserQuery.upper()):
    print("I don't know what you want me to do.")

try:
  inputFile = open(sys.argv[1])
  for cmd in inputFile:
    if (BreakFlag == 1):
      inputFile.close()
      quit()
    elif ("--" not in cmd):
      if (".EXIT" not in cmd.upper()):
        if userMadeLock == 0:
          isLocked = dbutils.checkLock(workingDB) if (workingDB != None) else 1
        UserQuery = cmd.rstrip('\n')
        commandProcessing()
      else:
        BreakFlag = 1
except IndexError:
  while (UserQuery.upper() != ".EXIT"):
    if userMadeLock == 0:
      isLocked = dbutils.checkLock(workingDB) if (workingDB != None) else 1
    UserQuery = input("danielaQL> ")
    commandProcessing()

quit()