import sqlite3
from sqlite3 import Error
import sql_scripts
import os
import sys
import pickle


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :return: Connection object or None
    """
    db_file = r"db\pythonsqlite.db"
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str
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

def drop_tables(conn, sql_list):
    """Drops all tables in sql_list
    @param sql_list (list of sql commands)
    """
    c = conn.cursor()
    for sql in sql_list:
        c.execute(sql)

def populate_table(conn, fileName, sql, criterion):
    """
    Create a new project into the projects table
    :param conn:
    :param file (string):
    :param sql (string)
    :param criterion (list of relevant values)
    """
    fullName = os.path.join("input_data", fileName)
    file = open(fullName, 'r')
    cur = conn.cursor()
    cur.execute("begin")
    

    while True:
        line = file.readline()
        if not line:
            break

	#print(line)
        line.strip()
        row = line.split('\t')
	#print(row)

        # Try to convert to appropriate datatypes
        if fileName == "PaperAuthorAffiliations.txt":
            row = convert_PaperAuthorAffiliations_types(row, criterion)
        elif fileName == "Papers.txt":
            row = convert_papers_types(row, criterion)
        else:
            print("Error, file has not been set up yet in populate table")
            break

        if row == None:
            continue
        else:
            # Insert data into database
            cur.execute(sql, row)
    cur.execute("commit")

def convert_PaperAuthorAffiliations_types(row, papers):
    '''Given a row converts to the appropriate data types
    Refer to https://docs.microsoft.com/en-us/academic-services/graph/reference-data-schema#paper-author-affiliations
    for specifics

    Args:
        @row (list of str)
        @papers (list of interested papers)
    Returns:
        row in the appropriate data types and tuple
    '''
    try:
        row[0] = int(row[0])
        row[1] = int(row[1])
        if row[2] != '':
            row[2] = int(row[2])
        row[3] = int(row[3])
        #print("successful conversions")

        if row[0] not in papers:
            return None
        row = tuple(row)
        return row
    except ValueError:
        print("Error, incorrect types")
        return None
    
def convert_papers_types(row, papers):
    '''Given a row converts to the appropriate data types
    Refer to https://docs.microsoft.com/en-us/academic-services/graph/reference-data-schema#papers
    for specifics

    Args:
        @row (list of str)
        @papers (list of relevant papers)
    Returns:
        row in the appropriate data types and tuple
    '''
    new_row = []
    try:
        new_row.append(int(row[0]))
        new_row.append(int(row[1]))
        new_row.append(int(row[2]))
        new_row.append(row[4])
        new_row.append(int(row[7]))
        new_row.append(row[8])
        new_row.append(int(row[11]))
        new_row.append(int(row[18]))
        new_row.append(int(row[19]))
        if row[22] != '':
            new_row.append(int(row[22]))
            new_row.append(int(row[23]))
        else:
            new_row.append('')
            new_row.append('')

        if new_row[0] not in papers:
            return None
        new_row = tuple(new_row)
        return new_row
    except ValueError:
        print("Error, incorrect types")
        return None

def load_pickle_list(fileName):
    file = os.path.join("pickle_files", fileName)
    infile = open(file, "rb")
    list = pickle.loads(infile)

def main():
    '''
    For args:
        Put valid number of a table to load just one table at a time
        Put all to load everything
    '''
    input = sys.argv[1]

    #url = "https://magasuscisi.blob.core.windows.net/mag-2021-05-24/mag/PaperAuthorAffiliations.txt"
    
    # create a database connection
    conn = create_connection()
    if conn is not None:
        with conn:
            try:
                # If input is a valid number, just load one table
                i = int(input)
                criterion = load_pickle_list(sql_scripts.pickle_files[i])
                drop_tables(conn, sql_scripts.sql_delete_tables[i])
                create_table(conn, sql_scripts.sql_create_tables[i])
                populate_table(conn, sql_scripts.papers[i], sql_scripts.sql_populate_tables[i], criterion)
            except (ValueError, IndexError):

                # Can load all
                if input == "all":
                    for i in range(len(sql_scripts.papers)):
                        criterion = load_pickle_list(sql_scripts.pickle_files[i])
                        drop_tables(conn, sql_scripts.sql_delete_tables[i])
                        create_table(conn, sql_scripts.sql_create_table[i])
                        populate_table(conn, sql_scripts.papers[i], sql_scripts.sql_populate_tables[i], criterion)
                    
                else:
                    print("Invalid command")
    
    else:
        print("Error! cannot access database")
        


if __name__ == '__main__':
    main()
