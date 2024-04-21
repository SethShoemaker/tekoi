from .protocol import SessionStorageProtocol as _SessionStorageProtocol
from mysql.connector import MySQLConnection as _MySQLConnection
import secrets as _secrets
import json as _json
import typing as _typing

class MySqlSessionStorage(_SessionStorageProtocol):

    def __init__(self, user: str, host: str, database: str, table_name_prefix = "tekoi_sessions_", password: str|None = None):
        self.user = user
        self.host = host
        self.database = database
        self.table_name_prefix = table_name_prefix
        self.password = password
        
        self.session_table_name = self.table_name_prefix + "session"

        self.create_tables_if_not_exists()

    def _create_connection(self) -> _MySQLConnection:
        return _MySQLConnection(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )

    def create_tables_if_not_exists(self) -> None:
        cnx = self._create_connection()
        cur = cnx.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS `{self.session_table_name}` 
            (
                id VARCHAR(100) NOT NULL PRIMARY KEY,
                data TEXT NOT NULL
            ) ENGINE=InnoDB;
        """)

    def create_session(self, session_data: dict[str, _typing.Any]) -> str:

        session_id = _secrets.token_urlsafe()
        insert_sql = f'INSERT INTO `{self.session_table_name}` (id, data) VALUES (%s , %s)'

        cnx = self._create_connection()
        cur = cnx.cursor()
        res = cur.execute(insert_sql, (session_id, _json.dumps(session_data,))) #type: ignore
        cnx.commit()

        return session_id
    
    def get_session_data(self, session_id: str) -> dict[str, _typing.Any]|None:
        
        cnx = self._create_connection()
        query_sql = f'SELECT data FROM `{self.session_table_name}` WHERE id=%s' 
        cur = cnx.cursor()
        res = cur.execute(query_sql, (session_id,))
        row = cur.fetchone()

        return _json.loads(str(row[0])) if row else None

    def invalidate_session(self, session_id: str):
        
        delete_sql = f'DELETE FROM `{self.session_table_name}` WHERE `id`=%s'
        cnx = self._create_connection()
        cur = cnx.cursor()
        cur.execute(delete_sql, (session_id))
