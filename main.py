import module.connected_postgresql as connDB

if __name__ == "__main__":
    db = connDB.PGDB(filename= "config/db.ini", section = "postgresql")
    inputText = ""
    while True:
        inputText = input("Пожалуйста введите запрос:\nДля выхода введите exit\n")
        if "exit" == inputText:
            break
        else:
            print(db.request(inputText))
    del db
