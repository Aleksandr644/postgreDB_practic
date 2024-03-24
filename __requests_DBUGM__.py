import __connected_postgresql__ as connDB
from datetime import date

class RDBUGM():
    """
    Класс взаимодействия с БД Уралгипромаш
    """

    def __init__(self, *, login: str, password: str, filename:str = 'config/db.ini', section:str = "postgresql"):
        """
        Создание обьекта взаимодействия с БД возможно только при разрешенном доступе
        Для этого необходимо указать правильный логин и пароль
        """

        self.__db = connDB.PGDB(filename = filename, section = section)
        if not self.__db:
            raise ConnectionError("Не смогли подключиться к базе данных")

    def verify_login(self, login):
        """
        проверяет существует ли логин в БД
        """
        print("проверка логина")
        b = self.__db.request(f"SELECT EXISTS(SELECT 1 FROM person WHERE login='{login}');")[0][0]
        print("ответ ", b)
        return b

    def verifi_password(self, login, password):
        """
        Проверяет, соответствует ли полученный пароль хранимому в БД
        """
        print("проверка пароля")
        b = self.__db.request(f"SELECT (password=crypt('{password}', password)) AS pass_match FROM person WHERE login='{login}';")[0][0]
        print("ответ ", b)
        return b
    
    def create_person( self, full_name:str, position:str, birthday:date, login:str, password:str, role:int ) -> bool:
        """
        Создание пользователя
        """
        if not len(password) < 225: return False
        if not len(login) < 25: return False
        if not ( 0 < role < 32767 ): return False
        if not isinstance( birthday, date ): return False
        b = self.__db.request( f"INSERT INTO Person(login, password, role) VALUES( '{ login }', crypt('{password}', gen_salt( 'bf' )), { role } ) returning id;" )
        self.change_full_name(login, full_name)
        self.change_position(login, position)
        self.change_birthday(login, birthday)
        return b

    def change_full_name(self, login:str, full_name:str) -> bool:
        if self.check_len(full_name, 255):
            return self.__change_person('Person', 'full_name', full_name, login)
        return False

    def change_position(self, login:str, position:str) -> bool:
        if self.check_len(position, 255):
            return self.__change_person('Person', 'position', position, login)
        return False

    def change_birthday(self, login:str, birthday:date) -> bool:
        if isinstance(birthday, date):
            return self.__change_person('Person', 'birthday', birthday, login)
        return False

    def change_password(self, login, old_password, new_password):
        if self.verify_login(login):
            if self.verifi_password(login, old_password):
                return self.__change_person('Person', 'password', new_password, login)
        return False

    def __get_person(self, table:str, what:str, login:str) -> any:
        return self.__db.request(f"SELECT {what} FROM {table} WHERE login='{login}';")

    def __change_person(self, table:str, what:str, value:any, login: str) -> bool:
        """
        UPDATE table SET what='value' WHERE login='login'
        """
        if self.verify_login(login):
            if what.lower() != 'password':
                return self.__db.request(f"UPDATE {table} SET {what}='{value}' WHERE login='{login}';")
            elif what == 'password':
                return self.__db.request(f"UPDATE {table} SET password=crypt('{value}', gen_salt('bf')) WHERE login='{login}';")
        return False

    def __del__(self):
        """
        При удалении обьекта взаимодействия, удаляется и подключение
        """
        del self.__db
        print("запросы к базе данных Уралгипромаш закончены")

    @staticmethod
    def check_len(strk:str, val:int):
        return len(strk) < val

if __name__ == "__main__":
    inputText = ""
    while True:
        inputText = input("Пожалуйста введите запрос:\nДля выхода введите exit\n")
        if "exit" == inputText:
            break
        elif "login" == inputText:
            login = input("Пожалуйста введите ваш ЛОГИН:\n")
            password = input("Пожалуйста введите ваш ПАРОЛЬ:\n")
            test = RDBUGM(login=login, password=password)
            del test
