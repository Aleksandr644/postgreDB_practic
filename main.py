import psycopg2
from configparser import ConfigParser

def config(filename:str = "db.ini", section:str = "postgresql") -> dict:
    cfg = ConfigParser()
    cfg.read(filename)
    return dict(cfg.items(section))

print("Connection")
connection = psycopg2.connect(**config())

var_cur = connection.cursor()

print("Database version is -")
var_cur.execute("SELECT version()")

version_of_database = var_cur.fetchone()
print(version_of_database)

var_cur.close()
connection.close()
print("Database connection closed")
