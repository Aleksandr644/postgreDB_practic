import psycopg2
from configparser import ConfigParser

def singleton(cls, *args, **kwargs):
    instances = {}
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton

@singleton
class PGDB:
    #conn = None
    #cursor = None
    def __init__(self, *, filename:str = "db.ini", section:str = "postgresql"):
        try:
            self.conn = psycopg2.connect(**PGDB.config(filename, section))
            print("Connection")
            self.cursor = self.conn.cursor()
            params = self.conn.get_dsn_parameters()
            print("information:")
            print(params)
        except(Exception, psycopg2.Error) as error:
            print("Ошибка подключения к базе данных", error)
            self.__del__()
            exit(1)            
        
    def __del__(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None
        print("Closing to connect")

    def request(self, order:str):
        if not order : order = "SELECT version()"
        self.cursor.execute(order)
        return self.cursor.fetchall()
    
    def request_add_product(self, article:str, name:str, description:str, volume:float, unit:str):
        pass


    
    @staticmethod
    def config(filename:str ,section:str) -> dict:
        cfg = ConfigParser()
        cfg.read(filename)
        return dict(cfg.items(section))
    
if __name__ == "__main__":
    db = PGDB()
    inputText = ""
    while True:
        inputText = input("Пожалуйста введите запрос:\nДля выхода введите exit\n")
        if "exit" == inputText:
            break
        else:
            print(PGDB.request(inputText))
    del db
