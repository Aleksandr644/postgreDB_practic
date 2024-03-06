import psycopg2
from configparser import ConfigParser

config = ConfigParser()
section = "postgresql"
config.read("db.ini")
params = dict(config.items(section))

print("Connection")
connection = psycopg2.connect(**params)

var_cur = connection.cursor()

print("Database version is -")
var_cur.execute("SELECT version()")

version_of_database = var_cur.fetchone()
print(version_of_database)

var_cur.close()
connection.close()
print("Database connection closed")
