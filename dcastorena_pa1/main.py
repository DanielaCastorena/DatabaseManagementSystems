#Daniela Castorena
#CS 457
#PA1

import os
import subprocess
import shlex

userQuery = None
workingDataBase = None
tableList = [None]

def inputCleaner(removeWord): #removes ; and command
  query = userQuery.replace(";", "")
  return query.replace(removeWord, "")

def checkTable(table): #checks for an existing table
  if table in subprocess.run(['ls', workingDataBase,  '|', 'grep', table], output=True, text=True).stdout:
    return 1
  else:
    return 0
  
def databaseCheck(database): #checks for an existing database 
 if database in subprocess.run(['ls', '|', 'grep', database], output=True, text=True).stdout:
    return 1
 else:
    return 0
  
while (userQuery != ".EXIT"):
  userQuery = input("danielaQL> ")
  if (';' not in userQuery and userQuery != ".EXIT"): 
    print("Commands must end with ';'") #invalid command, return solution
  
  #create database
  elif ("CREATE DATABASE" in userQuery):
    databaseName = inputCleaner("CREATE DATABASE ")
    if databaseCheck(databaseName) == 0:
      os.system(f'mkdir {databaseName}')
      print(f"Created database {databaseName}.")
    else:
      print(f"Could not create database {databaseName} because it already exists.")
  
  #delete database
  elif ("DROP DATABASE" in userQuery):
    databaseName = inputCleaner("DROP DATABASE ")
    if databaseCheck(databaseName):
      os.system(f'rm -r {databaseName}')
      print(f"Database {databaseName} has been removed.")
    else:
      print(f"Unable to remove database {databaseName} because it doesn't exist.")
  
  #sets database
  elif ("USE" in userQuery):
    workingDataBase = inputCleaner("USE ")
    #os.system('cd ' + workingDataBase)
    if databaseCheck(workingDataBase):
      print(f"Using database {workingDataBase}.")
    else:
      print(f"Could not use database {workingDataBase} because it does not exist.")

  #creates a table 
  elif ("CREATE TABLE" in userQuery):
    #splits input into separate strings
    tableInput = inputCleaner("CREATE TABLE ")
    tableName = tableInput.split()[0] #table name
    tableRest = tableInput.replace(tableName, "")
    tAttributes1 = tableRest[2:] #leaves only string with attributes
    tAttributes2 = tAttributes1[:-1] 
    tAttrs = tAttributes2.split(",") #creates list from attributes

    if (workingDataBase != None):
      if checkTable(tableName) == 0:
        os.system(f'touch {workingDataBase}/{tableName}.txt')
        filename = workingDataBase + '/' + tableName + '.txt'
        f = open(filename, 'w')
        f.write(" |".join(tAttrs)) #writes list to file with pipe delimiter
        f.close()
        print(f"Table {tableName} has been created.")
      else:
        print(f"Failed to create table {tableName} because it already exists.")
    else:
      print("Please specify which database to use.")

  #deletes table
  elif ("DROP TABLE" in userQuery):
    tableName = inputCleaner("DROP TABLE ")
    if (workingDataBase != None):
      if checkTable(tableName):
        os.system(f'rm {workingDataBase}/{tableName}.txt')
        print(f"Removed table {tableName} from database {workingDataBase}.")
      else:
        print(f"Failed remove table {tableName} because it doesn't exist.")
    else:
      print("Please specify which database to use.")
  
  #TODO
  #returns table elements as specified
  elif ("SELECT *" in userQuery):
    selection = inputCleaner("SELECT * FROM ")
    if workingDataBase != None:
      if checkTable(selection):
        f = open(f'{workingDataBase}/{selection}.txt', 'r')
        print(f.read())
        f.close()
      else:
        print(f"Failed to query table {selection} because it doesn't exist.")
    else:
      print("Please specify which database to use.")

  #TODO
  #modifies table by adding attribute
  elif ("ALTER TABLE" in userQuery):
    alter = inputCleaner("ALTER TABLE ")
    tableName = alter.split()[0] #table name
    alterCommand = alter.split()[1] #command (ADD, etc)
    alter1 = alter.replace(tableName, "")
    alter2 = alter1.replace(alterCommand, "") #left with attributes, currently only supports one
    newAttributes = alter2[2:] 

    if workingDataBase != None:
      if checkTable(tableName):
        f = open(f'{workingDataBase}/{tableName}.txt', 'a')
        f.write(f" | {newAttributes}") #appends attribute to file with pipe delimiter
        f.close()
        print(f"Table {tableName} has been modified.")
      else:
        print(f"Could not modify table {tableName} because it doesn't exist.")
    else:
      print("Please specify which database to use.")

quit()
