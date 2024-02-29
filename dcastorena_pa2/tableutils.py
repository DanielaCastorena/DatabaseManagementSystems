#Project Assignment 2 
#Author: Daniela Castorena
#Date: 4/3/23

import os
import subprocess
import dbutils

#from project assignment 1
#inserts a record into the table
def insertTuple(userQuery, workingDB):
  tInput = dbutils.inputCleaner("insert into ", userQuery)

  tName = tInput.split()[0] #table name
  tRest = tInput.replace(tName, "").replace(" values", "")
  tAttrs0 = tRest[1:] #leaves only string with attributes
  tAttrs1 = tAttrs0[:-1] #see above
  tAttrs = tAttrs1.split(",") #creates list from attributes

  if (workingDB != None):
    if dbutils.checkTable(tName, workingDB) == 1:
      filename = workingDB + '/' + tName + '.txt'
      f = open(filename, 'a')
      f.write('\n')
      f.write(" |".join(tAttrs)) #writes list to file with pipe delimiter
      f.close()
      print(f"1 new record inserted into {tName}.")
    else:
      print(f"Could not add values to {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")

#updates a record in the table
def updateTuple(userQuery, workingDB):
  tInput = dbutils.inputCleaner("update ", userQuery)

  tName = tInput.split()[0] #grabs table name
  setColumn = tInput.split()[2] 
  setRecord = tInput.split()[4]
  whereColumn = tInput.split()[6] 
  whereRecord = tInput.split()[8]

  if (workingDB != None):
    if dbutils.checkTable(tName, workingDB) == 1:
      filename = workingDB + '/' + tName + '.txt'

      #no way to modify middle of file, so we recreate it
      f = open(filename, 'r')
      tempFile = f.readlines()
      f.close()

      count = 0
      mods = 0
      setColumnNum = 0
      whereColumnNum = 0
      for line in tempFile:
        if (count == 0): #headers
          columnList = line.split()
          del columnList[1::3]
          setColumnNum = columnList.index(setColumn)
          whereColumnNum = columnList.index(whereColumn)
        if (count > 0): #values
          tupleDetails = line.split()
          if (tupleDetails[whereColumnNum] == whereRecord):
            #update data
            if ((setColumnNum+2) > len(tupleDetails)):
              tupleDetails[setColumnNum] = f'{setRecord}\n'
            else:
              tupleDetails[setColumnNum] = setRecord
            tempFile[count] = ' '.join(tupleDetails)
            mods += 1
        count += 1
      
      #overwrite file
      os.system(f'truncate -s 0 {workingDB}/{tName}.txt')

      f = open(filename, 'w')
      for line in tempFile:
        f.write(line)
      f.close()

      print(f"{mods} record(s) modified.")
    else:
      print(f"Could not update values in {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")

#removes a record from the table
def deleteTuple(userQuery, workingDB):
  tInput = dbutils.inputCleaner("delete from ", userQuery)

  tName = tInput.split()[0] # Grabs table name
  whereColumn = tInput.split()[2] # Gets "where" column
  whereRecord = tInput.split()[4]#.replace("'", "") # Gets "where" record

  operand = dbutils.getOperand(tInput.split()[3])

  if (workingDB != None):
    if dbutils.checkTable(tName, workingDB) == 1:
      filename = workingDB + '/' + tName + '.txt'
      f = open(filename, 'r')
      tempFile = f.readlines()
      f.close()

      count = 0
      mods = 0
      whereColumnNum = 0
      for line in tempFile:
        if (count == 0): #headers
          columnList = line.split()
          del columnList[1::3]
          whereColumnNum = columnList.index(whereColumn)
        if (count > 0): #values
          tupleDetails = line.split()

          #finds selected rows and deletes them
          def deleteTupleHelper(mods):
            if (operand == 0): #equality
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] == whereRecord):
                  tempFile[count] = None
                  mods += 1

              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) == float(whereRecord)):
                  tempFile[count] = None
                  mods += 1

            elif (operand == 1): # Greater than
              if (float(tupleDetails[whereColumnNum]) > float(whereRecord)):
                tempFile[count] = None
                mods += 1

            elif (operand == -1): # Less than
              if (float(tupleDetails[whereColumnNum]) < float(whereRecord)):
                tempFile[count] = None
                mods += 1

            #TODO
            # Add != action
            return mods
          mods = deleteTupleHelper(mods)
        count += 1
      
      # Overwrites the file
      os.system(f'truncate -s 0 {workingDB}/{tName}.txt')

      f = open(filename, 'w')
      for line in tempFile:
        if (line != None):
          f.write(line)
      f.close()

      print(f"{mods} record(s) deleted.")
    else:
      print(f"Could not delete values in {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")