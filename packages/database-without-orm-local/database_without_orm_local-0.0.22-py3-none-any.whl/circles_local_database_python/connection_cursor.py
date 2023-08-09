from dotenv import load_dotenv

from logger_local.LoggerLocal import logger_local
load_dotenv()
class ConnectionCursor:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def close(self):
        try:
            self.cursor.close()
            logger_local.info("Cursor closed successfully.")
        except Exception as e:
            logger_local.warning(f"Error closing cursor: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()