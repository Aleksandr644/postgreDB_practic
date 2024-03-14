import module.connected_postgresql as connDB

class RDBUGM():
    def __init__(self, *, login: str, password: str):
        try:
            self.__db = connDB.PGDB(filename = "config/db.ini", section = "postgresql")
            if not self.verify_login(login):
                self.__db.request(f"INSERT INTO person(login) values({login});")
                self.__db.request(f"UPDATE person SET password=crypt({password}, gen_salt('bf')) WHERE login={login};")
            elif self.verifi_password(login, password):
                print("Доступ разрешен")
            else:
                print("Доступ запрещен")
                raise PermissionError("Доступ запрещен")
        except PermissionError("Доступ запрещен") as error:
            print(error)
            del self.__db
            self.__del__()
    def verify_login(self, login):
        return self.__db.request(f"SELECT EXISTS(SELECT 1 FROM person WHERE login='{login}');")[0][0]

    def verifi_password(self, login, password):
        return self.__db.request(f"SELECT (password=crypt({password}, password) as pass_match FROM person WHERE login={login});")[0][0]

    def __del__(self):
        del self.__db
        print("запросы к базе данных Уралгипромаш закончены")

if __name__ == "__main__":
    db = connDB.PGDB(filename= "config/db.ini", section = "postgresql")
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
        else:
            print(db.request(inputText))
    del db
