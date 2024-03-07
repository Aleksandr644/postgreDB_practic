import psycopg2
from configparser import ConfigParser

class PGDB:
    conn = None
    cursor = None
    def __init__(self, *, filename:str = "db.ini", section:str = "postgresql"):
        try:
            PGDB.conn = psycopg2.connect(**PGDB.config(filename, section))
            print("Connection")
            PGDB.cursor = PGDB.conn.cursor()
            params = PGDB.conn.get_dsn_parameters()
            stat = PGDB.conn.get_parameter_status()
            print("information:")
            print(params)
            print(stat)
        except(Exception, psycopg2.Error) as error:
            print("Ошибка подключения к базе данных")
            exit(1)
        finally:
            PGDB.__del__()
        
    def __del__(self):
        print("Closing to connect")
        if PGDB.cursor:
            PGDB.cursor.close()
            PGDB.cursor = None
        if PGDB.conn:
            PGDB.conn.close()
            PGDB.conn = None

    def request(self, execut:str = "SELECT version()"):
        PGDB.cursor.execute(execut)
        return PGDB.cursor.fetchall()
    
    @staticmethod
    def config(filename:str ,section:str) -> dict:
        cfg = ConfigParser()
        cfg.read(filename)
        return dict(cfg.items(section))
    
if __name__ == "__main__":
    db = PGDB()
    inputText = ""
    while True:
        inputText = input("Пожалуйста введите запрос:\n")
        if "exit" == inputText:
            break
        else:
            print(db.request(inputText))
    del db
