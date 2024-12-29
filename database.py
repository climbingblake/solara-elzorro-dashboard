import sqlite3
from config import Config

class DatabaseManager:

    def __init__(self):
        self.db_file = Config.DB_CONFIG['FILE']

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def update_setting(self, key, value):
        """Update a setting in the database with proper error handling"""
        try:
            with self as cursor:
                cursor.execute("""
                    INSERT INTO settings (key, value, timestamp)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(key) DO UPDATE SET
                        value = excluded.value,
                        timestamp = CURRENT_TIMESTAMP
                """, (key, value))
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    @staticmethod
    def initialize_db():
        """Initialize the database with required tables"""
        try:
            with DatabaseManager() as cursor:
                for table_sql in Config.DB_CONFIG['TABLES'].values():
                    cursor.execute(table_sql)
                    print("-------------------created database------------------------- ")
            return True
        except sqlite3.Error as e:
            print(f"Failed to initialize database: {e}")
            return False

    def fetch_records(self, table_name):

        try:
            with self as cursor:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                cursor.execute(f"SELECT * FROM {table_name} ORDER BY timestamp ASC")
                records = cursor.fetchall()
            return records, columns
        except sqlite3.Error as e:
            print(f"Failed to fetch records: {e}")
            return [], []
    def fetch_snapshot_count(self):
        try:
            with self as cursor:
                cursor.execute("SELECT COUNT(*) FROM snapshots")
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Failed to fetch snapshot count: {e}")
            return 0