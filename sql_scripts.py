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
                                    createdDate VARCHAR(60)
                                ); """

sql_create_paperauthoraffiliations_table = '''CREATE TABLE IF NOT EXISTS PaperAuthorAffiliations (
                            paperId long PRIMARY KEY,
                            authorId long,
                            affiliationId long,
                            authorSequenceNumber int,
                            originalAuthor varchar(60),
                            originalAffiliation varchar(60)
);'''

sql_populate_affiliations = ''' INSERT INTO Affiliations 
                                (affiliationId, rank, normalizedName, 
                                displayName, gridId, officialPage, wikiPage, 
                                paperCount, paperFamilyCount, citationCount, 
                                iso3166Code, latitude, longitude, createdDate)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?); '''

sql_populate_paperauthoraffiliations = '''INSERT INTO PaperAuthorAffiliations (
                            paperId,
                            authorId,
                            affiliationId,
                            authorSequenceNumber,
                            originalAuthor,
                            originalAffiliation)
                            VALUES (?,?,?,?,?,?);'''