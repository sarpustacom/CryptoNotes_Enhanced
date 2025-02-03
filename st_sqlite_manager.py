import sqlite3

from crypto_note import CryptoNote

def delete_note_by_id(title):
    with sqlite3.connect('notes.db') as connection:
        cursor = connection.cursor()
        delete_query = "DELETE FROM notes WHERE title = ?"
        cursor.execute(delete_query,(title,))
        connection.commit()

def get_note_by_id(title) -> [CryptoNote]:
    with sqlite3.connect('notes.db') as connection:
        cursor = connection.cursor()
        select_query = "SELECT * FROM notes WHERE title = ?"
        cursor.execute(select_query,(title,))
        all_data = cursor.fetchall()
        return list(map(tuple_to_note, all_data))

def createNote(cryptoNote: CryptoNote):
    with sqlite3.connect("notes.db") as connection:
        cursor = connection.cursor()

        q1 = """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT
            );
        """

        cursor.execute(q1)

        q2 = """
            INSERT INTO notes (title, content) VALUES (?, ?)
        """
        data = (cryptoNote.title, cryptoNote.content)
        cursor.execute(q2, data)
        connection.commit()


def tuple_to_note(tuple):
    return CryptoNote(tuple[1],tuple[2])

def get_all_notes() -> [CryptoNote]:
    with sqlite3.connect('notes.db') as connection:
        cursor = connection.cursor()
        q1 = """
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        content TEXT
                    );
                """

        cursor.execute(q1)
        select_query = f"SELECT * FROM notes"
        cursor.execute(select_query)
        all_data = cursor.fetchall()
        return list(map(tuple_to_note, all_data))