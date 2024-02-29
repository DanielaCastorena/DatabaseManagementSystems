class Table:
  
  def __init__(self, name, attributes, database):
    self.name = None #table name
    self.attributes = None #table attributes
    self.database = None #table database
  
#get statements
  def getName(self):
    return self.name
  
  def getAttributes(self):
    return self.attributes 
  
  def getDatabase(self):
    return self.database

#set statements
  def setAttributes(self, input):
    return self.attributes
  
  def printTable(self):
    return 0