import sqlite3
from sqlite3 import Error
import sql_scripts
import os


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.isolation_level = None
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def populate_table(conn, fileName, sql):
    """
    Create a new project into the projects table
    :param conn:
    :param file (string):
    :param sql (string)
    """
    fullName = os.path.join("input_data", fileName)
    file = open(fullName, 'r')
    cur = conn.cursor()
    cur.execute("begin")
    

    while True:
        line = file.readline()
        if not line:
            break
	print(line)
        line.strip()
        row = line.split('\t')
	print(row)

        # Try to convert to appropriate datatypes
        if fileName == "PaperAuthorAffiliations.txt":
            row = convert_PaperAuthorAffiliations_types(row)
        else:
            print("Error, file has not been set up yet")
            break

        # Insert data into database
        cur.execute(sql, row)
    cur.execute("commit")

def convert_PaperAuthorAffiliations_types(row):
    '''Given a row converts to the appropriate data types

    Args:
        @row (list of str)
    Returns:
        row in the appropriate data types and tuple
    '''
    try:
        row[0] = int(row[0])
	row[1] = int(row[1])
        if row[2] != '':
		row[2] = int(row[2])
        row[3] = int(row[3])
	print("successful conversions")
        row = tuple(row)
        return row
    except ValueError:
        print("Error, incorrect types")
        return None
    

def main():
    database = r"db\pythonsqlite.db"
    url = "https://magasuscisi.blob.core.windows.net/mag-2021-05-24/mag/PaperAuthorAffiliations.txt"


    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        with conn:
            create_table(conn, sql_scripts.sql_create_paperauthoraffiliations_table)

            populate_table(conn, "PaperAuthorAffiliations.txt", sql_scripts.sql_populate_paperauthoraffiliations)

    else:
        print("Error! cannot access database")
        


if __name__ == '__main__':
    main()
