import os

import dbutils
import tableutils
import queryutils
import joinutils

userQuery = None
workingDB = None
tableList = [None]

while (userQuery != ".exit"):
  userQuery = input("danielaQL> ")
  if (';' not in userQuery and userQuery != ".exit"): 
    print("Commands must end with ';'")
  
  #create a database
  elif ("CREATE DATABASE" in userQuery.upper()):
    dbName = dbutils.inputCleaner("CREATE DATABASE ", userQuery)
    if dbutils.databaseExistenceCheck(dbName) == 0:
      os.system(f'mkdir {dbName}')
      print(f"Database {dbName} created.")
    else:
      print(f"Could not create database {dbName} because it already exists.")

  #delete a database
  elif ("DROP DATABASE" in userQuery.upper()):
    dbName = dbutils.inputCleaner("DROP DATABASE ", userQuery)
    if dbutils.databaseExistenceCheck(dbName):
      os.system(f'rm -r {dbName}')
      print(f"Removed database {dbName}.")
    else:
      print(f"Could not remove database {dbName} because it does not exist.")
  
  #sets currently active database
  elif ("USE" in userQuery.upper()):
    workingDB = dbutils.inputCleaner("USE ", userQuery)
    #os.system('cd ' + workingDB)
    if dbutils.databaseExistenceCheck(workingDB):
      print(f"Using database {workingDB}.")
    else:
      print(f"Could not use database {workingDB} because it does not exist.")

  #creates a table with specified name and attributes
  elif ("CREATE TABLE" in userQuery.upper()):
    #splits input into separate strings
    tInput = dbutils.inputCleaner("CREATE TABLE ", userQuery).replace("create table ", "")
    tName = tInput.split()[0] #table name
    tRest = tInput.replace(tName, "")
    tAttrs0 = tRest[2:] 
    tAttrs1 = tAttrs0[:-1] 
    tAttrs = tAttrs1.split(",") 

    if (workingDB != None):
      if dbutils.tableExistenceCheck(tName, workingDB) == 0:
        os.system(f'touch {workingDB}/{tName}.txt')
        filename = workingDB + '/' + tName + '.txt'
        f = open(filename, 'w')
        f.write(" |".join(tAttrs)) #writes list to file with pipe delimiter
        f.close()
        print(f"Table {tName} created.")
      else:
        print(f"Could not create table {tName} because it already exists.")
    else:
      print("Please specify which database to use.")

  #delete a table
  elif ("DROP TABLE" in userQuery.upper()):
    tName = dbutils.inputCleaner("DROP TABLE ", userQuery)
    if (workingDB != None):
      if dbutils.tableExistenceCheck(tName, workingDB):
        os.system(f'rm {workingDB}/{tName}.txt')
        print(f"Removed table {tName} from database {workingDB}.")
      else:
        print(f"Could not remove table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  #returns table elements as specified
  elif ("SELECT" in userQuery.upper()):
    if ("SELECT *" in userQuery.upper()):
      if ("." in userQuery.upper()):
        joinutils.joinTableOpener(userQuery, workingDB)
      else:
        queryutils.queryAll(userQuery, workingDB)
    else:
      queryutils.querySpecific(userQuery, workingDB)

  #modifies table
  elif ("ALTER TABLE" in userQuery.upper()):
    alter = dbutils.inputCleaner("ALTER TABLE ", userQuery)
    tName = alter.split()[0] #table name
    alterCmd = alter.split()[1] #grabs commands
    alterRest1 = alter.replace(tName, "")
    alterRest2 = alterRest1.replace(alterCmd, "")
    newAttr = alterRest2[2:] 
    
    if workingDB != None:
      if dbutils.tableExistenceCheck(tName, workingDB):
        f = open(f'{workingDB}/{tName}.txt', 'a')
        f.write(f" | {newAttr}") #appends attribute to file with pipe delimiter
        f.close()
        print(f"Modified table {tName}.")
      else:
        print(f"Could not modify table {tName} because it does not exist.")
    else:
      print("Please specify which database to use.")
  
  elif ("INSERT INTO" in userQuery.upper()):
    tableutils.insertTuple(userQuery, workingDB)
  
  elif ("UPDATE" in userQuery.upper()):
    tableutils.updateTuple(userQuery, workingDB)
  
  elif ("DELETE FROM" in userQuery.upper()):
    tableutils.deleteTuple(userQuery, workingDB)

  #deletes databases to start fresh
  elif ("DEL" in userQuery):
    os.system('rm -r CS457_PA3')
  
  elif (".exit" != userQuery):
    print("I don't know what you want me to do.")

quit()