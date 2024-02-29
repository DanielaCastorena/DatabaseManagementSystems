#Project Assignment 2
#Author: Daniela Castorena
#Date: 4/3/23

import os
import shlex
import subprocess

#from project assignment 1
def inputCleaner(removeWord, userQuery): 
  query = userQuery.replace(";", "")
  return query.replace(removeWord, "")

def checkDatabase(db): #database existence check
  if db in subprocess.run(['ls', '|', 'grep', db], capture_output=True, text=True).stdout:
    return 1
  else:
    return 0

def checkTable(t, workingDB): #table existence check
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
  