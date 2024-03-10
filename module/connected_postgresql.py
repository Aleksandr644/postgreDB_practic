import psycopg2
from pathlib import Path
from configparser import ConfigParser

def singleton(cls):
    instances = {}
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton
@singleton
class PGDB:
    def __init__(self, *, filename:str = "config/db.ini", section:str = "postgresql"):
        self.conn= None
        self.cursor = None
        try:
            if not Path(filename).is_file():
                raise FileNotFoundError(f"{'-'*30}\nФайла конфигурации './config/db.ini' не существует\nПоместите файл конфигурации db.ini в папку config\nСодержимое файла дожно содержать секцию {section}, которая должна содержать параметры подключения к базе данных\nнапример:\n[{section}]\nhost=localhost\nuser=user\npassword=password\n{'-'*30}")
            print(f"Получаем данные из файла {filename}\n")
            conf = self.config(filename, section)
            self.conn = psycopg2.connect(**conf)
            print("Подключаемся к базе данных")
            self.cursor = self.conn.cursor()
            params = self.conn.get_dsn_parameters()
            print("Информация о подключении:")
            print(params)
        except Exception as error:
            print("Ошибка подключения к базе данных\n", error)
            exit()            
        
    def __del__(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None
        print("Отключено")

    def request(self, order:str) -> str:
        try:
            if not order : order = "SELECT version()"
            self.cursor.execute(order)
            return self.cursor.fetchall()
        except psycopg2.Error as error:
            print("Что то пошло не так...\n", error)
    
    @staticmethod
    def config(fname:str ,sctn:str) -> dict:
        try:
            cfg = ConfigParser()
            cfg.read(fname)
            return dict(cfg.items(sctn))
        except Exception as error:
            print(f"Не удалось получить параметры конфигурации\n {error}")
            exit()
    
if __name__ == "__main__":
    db = PGDB(filename= "config/db.ini", section = "postgresql")
    inputText = ""
    while True:
        inputText = input("Пожалуйста введите запрос:\nДля выхода введите exit\n")
        if "exit" == inputText:
            break
        else:
            print(PGDB.request(inputText))
    del db
