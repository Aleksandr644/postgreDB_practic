import psycopg2
from configparser import ConfigParser



class PGDB:
    conn = None
    cursor = None
    def __init__(self, *, filename:str = "db.ini", section:str = "postgresql"):
        PGDB.conn = psycopg2.connect(**PGDB.config(filename, section))
        print("connection")
        PGDB.cursor = PGDB.conn.cursor()
        
    def __del__(self):
        print("Closing to connect")
        if PGDB.cursor:
            PGDB.cursor.close()
            PGDB.cursor = None
        if PGDB.conn:
            PGDB.conn.close()
            PGDB.conn = None
    def request(execut:str = None):
        if execut:
            PGDB.cursor.execute(execut)
        else:
            PGDB.cursor.execut("SELECT version()")
        return PGDB.cursor.fetchall()
    @staticmethod
    def config(filename:str ,section:str) -> dict:
        cfg = ConfigParser()
        cfg.read(filename)
        return dict(cfg.items(section))
if __name__ == "__main__":
    db = PGDB()
    print(db.request())
    del db