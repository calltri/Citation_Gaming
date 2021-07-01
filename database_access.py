import sqlite3
from sqlite3 import Error
import sql_scripts
import database_setup

def get_paper_journalId(conn, paperId):
    sql = """SELECT journalId 
            FROM Papers
            WHERE Papers.paperId == ?"""
    c = conn.cursor()
    return c.execute(sql, paperId)

