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

def divide_papers_by_journals(papers):
    """Divides journals by papers

    Args:
        papers (list of paperIds)
    Returns:
        list of affiliations
    """
    conn = database_setup.create_connection()
    community_ids = []
    for paper in papers:
        community_ids.append(get_paper_journalId(conn, paperId))

def main():
    community_ids = divide_papers_by_journals([1453551])

def __name__ == '__main__':
    main()