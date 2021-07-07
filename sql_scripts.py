papers = ['']
sql_delete_tables = ['']
sql_create_tables = ['']
sql_populate_tables = ['']
pickle_files = ['']


papers.append("PaperAuthorAffiliations.txt")
pickle_files.append('PaperAuthorAffiliations')
sql_create_tables.append('''CREATE TABLE IF NOT EXISTS PaperAuthorAffiliations (
                            paperId long,
                            authorId long,
                            affiliationId long,
                            authorSequenceNumber int,
                            originalAuthor varchar(60),
                            originalAffiliation varchar(60),
                            PRIMARY KEY (paperId, authorId, affiliationId)
);''')
sql_delete_tables.append("DROP TABLE IF EXISTS PaperAuthorAffiliations;")


sql_populate_tables.append('''INSERT INTO PaperAuthorAffiliations (
                            paperId,
                            authorId,
                            affiliationId,
                            authorSequenceNumber,
                            originalAuthor,
                            originalAffiliation)
                            VALUES (?,?,?,?,?,?);'''
)
papers.append("Papers.txt")
pickle_files.append('Papers')
sql_create_tables.append(""" CREATE TABLE IF NOT EXISTS Papers (
                            paperId long int PRIMARY KEY,
                            rank integer,
                            doi VARCHAR(60),
                            paperTitle VARCHAR(60),
                            year YEAR,
                            date DATETIME,
                            journalId long int,
                            referenceCount long int,
                            citationCount long int,
                            familyId long int,
                            familyRank int
                        );""")
sql_delete_tables.append("DROP TABLE IF EXISTS Papers;")

sql_populate_tables.append("""INSERT INTO Papers (
                        paperId,
                        rank,
                        doi,
                        paperTitle,
                        year,
                        date,
                        journalId,
                        referenceCount,
                        citationCount,
                        familyId,
                        familyRank)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)
);""")

sql_create_affiliations_table = """ CREATE TABLE IF NOT EXISTS Affiliations (
                                    affiliationId integer PRIMARY KEY,
                                    rank integer,
                                    normalizedName VARCHAR(60),
                                    displayName VARCHAR(60),
                                    gridId VARCHAR(60),
                                    officialPage VARCHAR(60),
                                    wikiPage VARCHAR(60),
                                    paperCount long int,
                                    paperFamilyCount long int,
                                    citationCount long int,
                                    iso3166Code Char(2),
                                    latitude float,
                                    longitude float,
                                    createdDate DATETIME
                                ); """
sql_delete_tables.append("DROP TABLE IF EXISTS Affiliations;")

sql_populate_affiliations = ''' INSERT INTO Affiliations 
                                (affiliationId, rank, normalizedName, 
                                displayName, gridId, officialPage, wikiPage, 
                                paperCount, paperFamilyCount, citationCount, 
                                iso3166Code, latitude, longitude, createdDate)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?); '''
