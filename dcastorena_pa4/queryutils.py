import os
import dbutils

#same code from previous project assignments
#select *
def queryAll(UserQuery, workingDB):
  selLower = dbutils.inputCleaner("SELECT * FROM ", UserQuery)
  selection = dbutils.inputCleaner("select * from ", selLower)
  if workingDB != None:
    if dbutils.tableExistenceCheck(selection, workingDB):
      f = open(f'{workingDB}/{selection}.txt', 'r')
      print(f.read())
      f.close()
    else:
      print(f"Could not query table {selection} because it does not exist.")
  else:
    print("Please specify which database to use.")
def querySpecific(UserQuery, workingDB):
  selLower = dbutils.inputCleaner("SELECT ", UserQuery)
  selection = dbutils.inputCleaner("select ", selLower)

  #gathering list of variables
  selectColumns = selection.replace(",", "").split()
  selectColumns = selectColumns[:selectColumns.index("from")]

  #table name
  tName = selection.split()[len(selectColumns)+1]

  #gathering what to filter by
  whereColumn = selection.split()[len(selectColumns)+3]
  whereRecord = selection.split()[len(selectColumns)+5]
  operand = dbutils.getOperand(selection.split()[len(selectColumns)+4])

  if workingDB != None:
    if dbutils.tableExistenceCheck(tName, workingDB):
      f = open(f'{workingDB}/{tName}.txt', 'r')
      tempFile = f.readlines()
      f.close()

      selectColumnNums = []
      columnNameString = ""
      listToReturn = []
      count = 0
      for line in tempFile:
        if (count == 0): #headers
          columnList = line.split()
          columnListWithTypes = columnList.copy()
          del columnListWithTypes[2::3]

          del columnList[1::3]
          columnCount = 0

          for word in columnList:
            if word in selectColumns:
              selectColumnNums.append(columnCount)
            if (word == whereColumn):
              whereColumnNum = columnCount
            columnCount += 1

          for index in selectColumnNums:
            columnNameString += f"{columnListWithTypes[index]} {columnListWithTypes[index+1]} | "
          queryHeader = columnNameString[:-3]
          listToReturn.append(queryHeader)

        if (count > 0): #values
          tupleDetails = line.split()
          def querySpecificHelper():

            # Creates the row output
            def queryStringMaker():
              queryString = ""
              for index in selectColumnNums:
                queryString += f"{tupleDetails[index]} | "
              queryResult = queryString[:-3]
              listToReturn.append(queryResult)

            if (operand == 0):
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] == whereRecord):
                  queryStringMaker()
              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) == float(whereRecord)):
                  queryStringMaker()

            elif (operand == 1): #greater than
              if (float(tupleDetails[whereColumnNum]) > float(whereRecord)):
                queryStringMaker()

            elif (operand == -1): #less than
              if (float(tupleDetails[whereColumnNum]) < float(whereRecord)):
                queryStringMaker()

            elif (operand == -3): #inequality
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] != whereRecord):
                  queryStringMaker()
              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) != float(whereRecord)):
                  queryStringMaker()

          querySpecificHelper()

        count += 1
      for line in listToReturn: #prints table
        print(line)

    else:
      print(f"Could not query table {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")