from peewee import PostgresqlDatabase
from configparser import ConfigParser
from pathlib import Path

def singleton(cls):
    """
    Декоратор класса для ограничения создания обьектов класса в 1 экземпляр.
    При попытке создания нового экземпляра класса, возвращает уже созданный объект класса.
    """
    instances = {}
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton

@singleton
class PGDB:
    """
    Класс создания соединения с БД Postgre
    """
    def __init__(self, *, filename:str = "db.ini", section:str = "postgresql"):
        """
        инициализация экземпляра класса, которая на вход принимает именнованные аргументы. filename - путь к конфигурационному файлу. section - в какой екции конфигурационного фала находяться данные.
        config/db.examle - содержит пример конфигурационного файла
        """
        self.__conn= None
        self.__cursor = None
        
        if not Path(filename).is_file():
            raise FileNotFoundError(f"{'-'*30}\nФайла конфигурации 'db.ini' не существует\nПоместите файл конфигурации db.ini в папку config\nСодержимое файла дожно содержать секцию {section}, которая должна содержать параметры подключения к базе данных\nнапример:\n[{section}]\nhost=localhost\nuser=user\npassword=password\n{'-'*30}")
        print(f"Получаем данные из файла {filename}\n")
        conf = self.__config(filename, section)
        self.__conn = PostgresqlDatabase(**conf)
        print("Подключаемся к базе данных")
        self.__cursor = self.__conn.cursor()
        
        
    def __del__(self):
        """
        перед удалением экземляа класса закрывает соединения с сервером
        """
        if self.__cursor:
            self.__cursor.close()
            self.__cursor = None
        if self.__conn:
            self.__conn.close()
            self.__conn = None
        print("Отключено")

    def request(self, order:str) -> list:
        """
        отправка запроса к серверу и получение список ответов
        """
        if not order : order = "SELECT version()"
        self.__cursor.execute(order)
        return self.__cursor.fetchall()

    def __commit(self):
        self.__conn.commit()

    def __rollback(self):
        self.__conn.rollback()

    @staticmethod
    def __config(fname:str ,sctn:str) -> dict:
        """
        статичный метод открытия конфигурационного файла и считывание данных из укаазнного сектора
        на вход принимает путь к файлу и название секции для чтения.
        """
        try:
            cfg = ConfigParser()
            cfg.read(fname)
            return dict(cfg.items(sctn))
        except Exception as error:
            print(f"Не удалось получить параметры конфигурации\n {error}")
            exit()
if __name__ == "__main__":
    db = PGDB(filename= "db.ini", section = "postgresql")
    inputText = ""
    while True:
        inputText = input("Пожалуйста введите запрос:\nДля выхода введите exit\n")
        if "exit" == inputText:
            break
        else:
            print(db.request(inputText))
    del db
