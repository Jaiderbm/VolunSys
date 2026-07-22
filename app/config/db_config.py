import os
import psycopg2
import threading
from dotenv import load_dotenv

load_dotenv()
_DATABASE_URL = os.getenv("DATABASE_URL")

class AutoReconnectConn:
    """Wraps the psycopg2 connection to auto-reconnect when Neon DB sleeps in a thread-safe way."""
    def __init__(self):
        self._local = threading.local()
        
    @property
    def connection(self):
        if not hasattr(self._local, "conn") or self._local.conn is None or self._local.conn.closed != 0:
            self._connect()
        else:
            try:
                # Rollback any aborted transaction before pinging
                if self._local.conn.info.transaction_status != 0:  # IDLE = 0
                    try:
                        self._local.conn.rollback()
                    except:
                        pass
                # Ping connection to see if it is alive
                with self._local.conn.cursor() as c:
                    c.execute("SELECT 1")
                # Rollback the implicit transaction from SELECT 1
                self._local.conn.rollback()
            except Exception:
                self._connect()
        return self._local.conn
        
    def _connect(self):
        if hasattr(self._local, "conn") and self._local.conn is not None:
            try:
                self._local.conn.close()
            except:
                pass
        self._local.conn = psycopg2.connect(_DATABASE_URL)

    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        conn = getattr(self._local, "conn", None)
        if conn is not None and conn.closed == 0:
            conn.commit()

    def rollback(self):
        conn = getattr(self._local, "conn", None)
        if conn is not None and conn.closed == 0:
            conn.rollback()

def get_connection():
    return psycopg2.connect(_DATABASE_URL)

conn = AutoReconnectConn()