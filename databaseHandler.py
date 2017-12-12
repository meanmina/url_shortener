import sqlite3
from sqlite3 import OperationalError

class DatabaseHandler:
  # use an sqlite database since it's easy to work with
  #   and I have SQL experience
  def checkDbs(self):
    # check that table was created and create if not

    # simple CREATE TABLE command
    #   ID  for URL (to be later encoded)
    #   URL to be stored
    command = """
              CREATE TABLE WEBURL(
                ID INTEGER PRIMARY KEY  AUTOINCREMENT,
                URL TEXT  NOT NULL
              );
              """
    # connect to database
    with sqlite3.connect('urls.db') as connection:
      cursor = connection.cursor()

      try:
        cursor.execute(command)
      except OperationalError:
        pass
      except Exception as exc:
        print exc


  def addToDbs(self, inpt):
    # add item to URL table

    # simple insert command
    command = """
              INSERT INTO WEBURL (URL) VALUES ('%s')
              """ % (inpt)
    # connect to database
    with sqlite3.connect('urls.db') as connection:
      cursor = connection.cursor()

      try:
        result = cursor.execute(command)

        if result:
          return result.lastrowid
      except Exception as exc:
        print exc

    return None

  def getFromDbs(self, inpt):
    # get item from URL table

    # simple SELECT command
    command = """
              SELECT URL FROM WEBURL WHERE ID=%s
              """ % (inpt)
    # connect to database
    with sqlite3.connect('urls.db') as connection:
      cursor = connection.cursor()

      try:
        result = cursor.execute(command)
        if result:
          return result.fetchone()[0]
      except Exception as exc:
        print exc

    return None