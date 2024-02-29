import os
import dbutils

#inserts record into the table
def insertTuple(UserQuery, workingDB, isLocked, u, c):
  tInput = dbutils.inputCleaner("insert into ", UserQuery)

  tName = tInput.split()[0] #table name
  tRest = tInput.replace(tName, "").replace(" values", "")
  tAttrs0 = tRest[1:] 
  tAttrs1 = tAttrs0[:-1] 
  tAttrs = tAttrs1.split(",") #creates list from attributes
  tAttrs[0] = tAttrs[0].replace("(", "")


  def appendToFile():
    f = open(filename, 'a')
    f.write('\n')
    f.write(" | ".join(tAttrs)) # Writes list to file with pipe delimiter
    f.close()

  if (workingDB != None):
    if dbutils.tableExistenceCheck(tName, workingDB) == 1:
      if isLocked == 0:
        if u:
          os.system(f"cp {workingDB}/{tName}.txt {workingDB}/{tName}.new.txt")
          filename = workingDB + '/' + tName + '.new.txt'
          appendToFile()
          c.append(f"rm {workingDB}/{tName}.txt")
          c.append(f"mv {workingDB}/{tName}.new.txt {workingDB}/{tName}.txt")
        else:
          filename = workingDB + '/' + tName + '.txt'
          appendToFile()
        print(f"1 new record inserted into {tName}.")
      else:
        print(f"Error: Table {tName} is locked!")
    else:
      print(f"Could not add values to {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")

#updates table records
def updateTuple(UserQuery, workingDB, isLocked, u, c):
  tInput = dbutils.inputCleaner("update ", UserQuery)

  tName = tInput.split()[0] 
  setColumn = tInput.split()[2] #set column
  setRecord = tInput.split()[4] #where to place record
  whereColumn = tInput.split()[6] #location of column
  whereRecord = tInput.split()[8] #location record

  def overwriteFile():
    f = open(filename, 'w')
    for line in tempFile:
      f.write(line)
    f.close()

  if (workingDB != None):
    if dbutils.tableExistenceCheck(tName, workingDB) == 1:
      if isLocked == 0:
        filename = workingDB + '/' + tName + '.txt'

        #recreate middle file
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
              if ((setColumnNum+2) > len(tupleDetails)):
                tupleDetails[setColumnNum] = f'{setRecord}\n'
              #update data
              else:
                tupleDetails[setColumnNum] = setRecord
              tempFile[count] = ' '.join(tupleDetails)
              mods += 1
          count += 1
        
        if u:
          filename = workingDB + '/' + tName + '.new.txt'
          os.system(f"touch {filename}")
          overwriteFile()
          c.append(f"rm {workingDB}/{tName}.txt")
          c.append(f"mv {workingDB}/{tName}.new.txt {workingDB}/{tName}.txt")
        else:
          #overwrite
          os.system(f'truncate -s 0 {filename}') #{workingDB}/{tName}.txt
          overwriteFile()
        print(f"{mods} record(s) modified in {tName}.")
      else:
        print(f"Error: Table {tName} is locked!")
    else:
      print(f"Could not update values in {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")

#removes a record
def deleteTuple(UserQuery, workingDB, isLocked, u, c):
  tInput = dbutils.inputCleaner("delete from ", UserQuery)

  tName = tInput.split()[0] #table name
  whereColumn = tInput.split()[2] #location of column
  whereRecord = tInput.split()[4]#location of record

  operand = dbutils.getOperand(tInput.split()[3])

  def overwriteFileWithDeletes():
    f = open(filename, 'w')
    for line in tempFile:
      if (line != None):
        f.write(line)
    f.close()

  if (workingDB != None):
    if dbutils.tableExistenceCheck(tName, workingDB) == 1:
      if isLocked == 0:
        filename = workingDB + '/' + tName + '.txt'

        #recreate file
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
            def deleteTupleHelper(mods):
              if (operand == 0): 
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
              return mods
            mods = deleteTupleHelper(mods)
          count += 1
        
        if u:
          filename = workingDB + '/' + tName + '.new.txt'
          os.system(f"touch {filename}")
          overwriteFileWithDeletes()
          c.append(f"rm {workingDB}/{tName}.txt")
          c.append(f"mv {workingDB}/{tName}.new.txt {workingDB}/{tName}.txt")
        else:
          os.system(f'truncate -s 0 {workingDB}/{tName}.txt')
          overwriteFileWithDeletes()

        print(f"{mods} record(s) removed in {tName}.")
      else:
        print(f"Error: Table {tName} is locked!")
    else:
      print(f"Could not remove values in {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")