import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mods (
                title TEXT NOT NULL,
                curseforge_url TEXT NOT NULL PRIMARY KEY,
                curseforge_project_id INTEGER
            );
        ''')
        self.conn.commit()

    def store(self, data):
        title = data['title']
        curseforge_url = data['curseforge_url']
        curseforge_project_id = data.get('curseforge_project_id', None)
        self.cursor.execute('''
            INSERT INTO mods (title, curseforge_url, curseforge_project_id)
            VALUES (?, ?, ?)
            ON CONFLICT(curseforge_url) DO UPDATE SET
            title = excluded.title,
            curseforge_project_id = coalesce(mods.curseforge_project_id, excluded.curseforge_project_id)
        ''', (title, curseforge_url, curseforge_project_id))
        self.conn.commit()

    def get(self, curseforge_url):
        self.cursor.execute('''
            SELECT title, curseforge_project_id
            FROM mods
            WHERE curseforge_url = ?
        ''', (curseforge_url,))
        result = self.cursor.fetchone()
        if result is not None:
            title, curseforge_project_id = result
            return {'title': title, 'curseforge_url': curseforge_url, 'curseforge_project_id': curseforge_project_id}
        else:
            return None

    def update(self, data):
        self.cursor.execute('''UPDATE mods SET curseforge_project_id = ? WHERE curseforge_url = ?''', (data['curseforge_project_id'], data['curseforge_url']))
        self.conn.commit()

    def close(self):
        self.conn.close()

class KeyValueDatabase:
    """Simple key-value store using SQLite."""
    def __init__(self, table_name, db_file="./urls.sqlite3"):
        self.table_name = table_name
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table_name} (
                            url TEXT PRIMARY KEY,
                            value INTEGER
                            )
                        """)
        self.conn.commit()

    def store(self, url, value):
        self.cursor.execute(f"INSERT OR REPLACE INTO {self.table_name} VALUES (?, ?)", (url, value))
        self.conn.commit()

    def get(self, url):
        self.cursor.execute(f"SELECT value FROM {self.table_name} WHERE url=?", (url,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    def close(self):
        self.conn.close()

