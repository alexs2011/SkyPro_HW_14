import sqlite3


class NetflixDAO:

    def __init__(self, path: str) -> None:
        """
        При создании экземпляра NetflixDAO указывается путь к базе данных.
        """
        self.path = path

    def execute_query(self, sqlite_query: str) -> list:
        """
        Подключается к базе данных и выполняет запрос sqlite_query.
        """
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(sqlite_query)
            executed_query = cur.fetchall()
        return executed_query
