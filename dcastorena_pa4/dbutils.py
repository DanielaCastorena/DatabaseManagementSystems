import os
import shlex
import subprocess
#same code from previous project assignments

def inputCleaner(wordToRemove, UserQuery): #removes ; and command
  query = UserQuery.replace(";", "")
  return query.replace(wordToRemove, "")

def databaseExistenceCheck(db): #checks if database exists
  if db in subprocess.run(['ls', '|', 'grep', db], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

def tableExistenceCheck(t, workingDB): #checks if table exists
  if t in subprocess.run(['ls', workingDB,  '|', 'grep', t], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

#determines operand and assigns value
def getOperand(o):
  operand = None
  if (o == '='):
    operand = 0
  elif (o == '<'):
    operand = -1
  elif (o == '>'):
    operand = 1
  elif (o == '!='):
    operand = -3
  return operand

#PA4 NEW CODE
#creates a lock if one does not exist already
def makeLock(workingDB):
  if checkLock(workingDB):
    return 0
  else:
    tablesToLock = subprocess.run(['ls', workingDB, '|', 'grep ".txt"'], capture_output=True, text=True).stdout.split()
    tablesToLock.pop(0)
    for name in tablesToLock:
      os.system(f"touch {workingDB}/{name}.lock")
    return 1

#code to check for exixting lock
def checkLock(workingDB):
  if ".lock" in subprocess.run(['ls', workingDB, '|', 'grep ".lock"'], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

#code to remove lock
def releaseLock(workingDB, c):
  for cmd in c:
    os.system(cmd)
  os.system(f"rm {workingDB}/*.lock")