import sqlite3
import logging
import os
from contextlib import contextmanager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseHelper:
    def __init__(self, db_path="output/asana_simulation.sqlite"):
        self.db_path = db_path
        # ---  Create the folder if it doesn't exist ---
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created directory: {db_dir}")

    @contextmanager
    def get_connection(self):
        """Context manager for handling SQLite connections safely."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    def execute_script(self, script_path):
        """Executes a .sql file to initialize the schema."""
        try:
            if not os.path.exists(script_path):
                logger.error(f"Schema file NOT FOUND at: {script_path}")
                return

            with self.get_connection() as conn:
                with open(script_path, 'r') as f:
                    script = f.read()
                conn.executescript(script)
                conn.commit()
            logger.info(f"Successfully executed schema script: {script_path}")
        except Exception as e:
            logger.error(f"Error executing script {script_path}: {e}")
            raise

    def batch_insert(self, table_name, columns, data_list):
        """High-speed batch insertion."""
        if not data_list:
            return

        placeholders = ", ".join(["?" for _ in columns])
        col_string = ", ".join(columns)
        query = f"INSERT INTO {table_name} ({col_string}) VALUES ({placeholders})"

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, data_list)
                conn.commit()
            logger.info(f"Inserted {len(data_list)} rows into {table_name}.")
        except Exception as e:
            logger.error(f"Failed to batch insert into {table_name}: {e}")
            raise
    
    def execute(self, query, params=None):
        """Execute a single query safely using the connection context."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor
        except Exception as e:
            logger.error(f"Error executing query: {query} | Error: {e}")
            raise
