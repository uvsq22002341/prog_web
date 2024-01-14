import sqlite3
import os
from passlib.hash import scrypt


def dictionary_factory(cursor, row):
  dictionary = {}
  for index in range(len(cursor.description)):
    column_name = cursor.description[index][0]
    dictionary[column_name] = row[index]
  return dictionary


def connect(database = "database.sqlite"):
  connection = sqlite3.connect(database)
  connection.set_trace_callback(print)
  connection.execute('PRAGMA foreign_keys = 1')
  connection.row_factory = dictionary_factory
  return connection


def read_build_script():
  path = os.path.join(os.path.dirname(__file__), 'build.sql')
  file = open(path)
  script = file.read()
  file.close()
  return script


def create_database(connection):
  script = read_build_script()
  connection.executescript(script)
  connection.commit()


def fill_database(connection):
  add_user(connection, 'user@example.com', 'secret')


def hash_password(password):
  return scrypt.using(salt_size=16).hash(password)


def add_user(connection, email, password):
  sql = '''
    INSERT INTO users(email, password_hash) VALUES (:email, :password_hash);
  '''
  password_hash = hash_password(password)
  connection.execute(sql, {
    'email' : email,
    'password_hash' : password_hash
  })
  connection.commit()


def get_user(connection, email, password):
  sql = '''
    SELECT * FROM users
    WHERE email = :email;
  '''
  cursor = connection.execute(sql, {'email': email})
  users = cursor.fetchall()
  if len(users) == 0:
    raise Exception('Utilisateur inconnu')
  user = users[0]
  if not scrypt.verify(password, user['password_hash']):
    raise Exception('Utilisateur inconnu')
  return {'id' : user['id'], 'email' : user['email']}


def change_password(connection, email, old_password, new_password):
  get_user(connection, email, old_password)
  sql = '''
    UPDATE users
    SET password_hash = :password_hash
    WHERE email = :email
  '''
  password_hash = hash_password(new_password)
  connection.execute(sql, {
    'email' : email,
    'password_hash' : password_hash
  })
  connection.commit()


def change_totp(connection, email, totp_secret):
  sql = '''
    UPDATE users
    SET totp = :totp_secret
    WHERE email = :email
  '''
  connection.execute(sql, {'email' : email, 'totp_secret': totp_secret})
  connection.commit()


def get_totp(connection, user_id): 
  sql = '''
    SELECT totp FROM users
    WHERE id = :user_id
  '''
  cursor = connection.execute(sql, {'user_id' : user_id})
  users = cursor.fetchall()
  if len(users) == 0:
    raise Exception('Utilisateur inconnu')
  user = users[0]
  return user['totp']


