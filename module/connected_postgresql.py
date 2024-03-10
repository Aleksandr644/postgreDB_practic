import psycopg2
from configparser import ConfigParser

def singleton(cls):
    instances = {}
    def _singleton(*args, **kwargs):
        print(args)
        print(kwargs)
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton

@singleton
class PGDB:
    def __init__(self, *, filename:str = "../config/db.ini", section:str = "postgresql"):
        self.conn= None
        self.cursor = None
        try:
            self.conn = psycopg2.connect(**PGDB.config(filename, section))
            print("Connection")
            self.cursor = self.conn.cursor()
            params = self.conn.get_dsn_parameters()
            print("information:")
            print(params)
        except(Exception, psycopg2.Error) as error:
            print("Ошибка подключения к базе данных", error)
            exit()            
        
    def __del__(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None
        print("Closing to connect")

    def request(self, order:str) -> str:
        if not order : order = "SELECT version()"
        self.cursor.execute(order)
        return self.cursor.fetchall()
    
    @staticmethod
    def config(filename:str ,section:str) -> dict:
        cfg = ConfigParser()
        cfg.read(filename)
        return dict(cfg.items(section))
  
if __name__ == "__main__":
    db = PGDB(filename= "../config/db.ini", section = "postgresql")
    inputText = ""
    while True:
        inputText = input("Пожалуйста введите запрос:\nДля выхода введите exit\n")
        if "exit" == inputText:
            break
        else:
            print(PGDB.request(inputText))
    del db
