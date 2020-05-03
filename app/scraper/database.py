import sqlite3
#from scraper import sqliteConnection

import sqlite3, os, uuid

def convertToBinaryData(filepath):
    # convert digital data to Blob
    with open(filepath, 'rb') as file:
        blobData = file.read()

    return blobData


def addToNews(country: str, title: str, body: str):
    try:
        PATH_TO_DB = os.path.join(os.getcwd(), 'app', 'database', 'newsfeed.db')
        sqliteConnection = sqlite3.connect(PATH_TO_DB)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        insert_news_query = """INSERT INTO news
                            (public_id, country, title, body) VALUES (?, ?, ?, ?)"""

        data_tuple = (str(uuid.uuid4()), country, title, body)

        cursor.execute(insert_news_query, data_tuple)

        sqliteConnection.commit()

        cursor.close()

        return 200
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            return 400
        return 404
