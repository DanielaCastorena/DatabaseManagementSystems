#Project Assignment 2 
#Author: Daniela Castorena
#Date: 4/3/23

import os
import subprocess
import dbutils

#select *
def queryAll(userQuery, workingDB):
  selLower = dbutils.inputCleaner("SELECT * FROM ", userQuery)
  selection = dbutils.inputCleaner("select * from ", selLower)
  if workingDB != None:
    if dbutils.checkTable(selection, workingDB):
      f = open(f'{workingDB}/{selection}.txt', 'r')
      print(f.read())
      f.close()
    else:
      print(f"Could not query table {selection} because it does not exist.")
  else:
    print("Please specify which database to use.")

def querySpecific(userQuery, workingDB):
  selLower = dbutils.inputCleaner("SELECT ", userQuery)
  selection = dbutils.inputCleaner("select ", selLower)

  #getting list of variables
  selectColumns = selection.replace(",", "").split()
  selectColumns = selectColumns[:selectColumns.index("from")]

  whereColumn = selection.split()[len(selectColumns)+3]
  whereRecord = selection.split()[len(selectColumns)+5]
  operand = dbutils.getOperand(selection.split()[len(selectColumns)+4])

  #table name
  tName = selection.split()[len(selectColumns)+1]

  if workingDB != None:
    if dbutils.checkTable(tName, workingDB):
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

          #if variable is found in table, this will record its index
          for word in columnList:
            if word in selectColumns:
              selectColumnNums.append(columnCount)
            if (word == whereColumn):
              whereColumnNum = columnCount
            columnCount += 1

          #table headers for selected columns
          for index in selectColumnNums:
            columnNameString += f"{columnListWithTypes[index]} {columnListWithTypes[index+1]} | "
          queryHeader = columnNameString[:-3]
          listToReturn.append(queryHeader)

        if (count > 0): 
          tupleDetails = line.split()
          def querySpecificHelper():

            #creates the row output
            def queryStringMaker():
              queryString = ""
              for index in selectColumnNums:
                queryString += f"{tupleDetails[index]} | "
              queryResult = queryString[:-3]
              listToReturn.append(queryResult)

            if (operand == 0): #equality
              if (type(tupleDetails[whereColumnNum]) is str):
                if (tupleDetails[whereColumnNum] == whereRecord):
                  queryStringMaker()
              elif (type(tupleDetails[whereColumnNum]) is not str):
                if (float(tupleDetails[whereColumnNum]) == float(whereRecord)):
                  queryStringMaker()

            elif (operand == 1): #greater than, >
              if (float(tupleDetails[whereColumnNum]) > float(whereRecord)):
                queryStringMaker()

            elif (operand == -1): #less than, <
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
      for line in listToReturn: 
        print(line) #prints table

    else:
      print(f"Could not query table {tName} because it does not exist.")
  else:
    print("Please specify which database to use.")