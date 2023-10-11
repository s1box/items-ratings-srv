import sys
import os

from flaskext.mysql import MySQL

DATABASE_NAME = 'items'

class RatingMysqlClient:

    def __init__(self, table, app):
        self.__mysql = MySQL()
        self.__table = table

        self.configure_mysql(app)


    def configure_mysql(self, app):
        _db_user = os.getenv('DB_USERNAME')
        if _db_user is None:
            print('DB_USERNAME is not set')
            sys.exit(1)
        _db_password = os.getenv('DB_PASSWORD')
        if _db_password is None:
            print('DB_PASSWORD is not set')
            sys.exit(1)
        _db_host = os.getenv('DB_HOSTNAME')
        if _db_user is None:
            print('DB_HOSTNAME is not set')
            sys.exit(1)
        _db_port = os.getenv('DB_PORT')
        if _db_user is None:
            print('DB_PORT is not set')
            sys.exit(1)

        app.config['MYSQL_DATABASE_USER'] = _db_user
        app.config['MYSQL_DATABASE_PASSWORD'] = _db_password
        app.config['MYSQL_DATABASE_HOST'] = _db_host
        app.config['MYSQL_DATABASE_PORT'] = int(_db_port)
        app.config['MYSQL_DATABASE_DB'] = DATABASE_NAME

        self.__mysql.init_app(app)


    def ping(self):
        try:
            conn = self.__mysql.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT VERSION()')
            ver = cursor.fetchone()
            return "OK"
        except Exception as e:
            print(e)
            return str(e)
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except Exception as e:
                print(e)


    def add_rating(self, item_id, item_rating):
        try:
            sql = 'INSERT INTO %s(item_id, rating) VALUES(%s, %s) ;' % (self.__table, item_id, item_rating)
            conn = self.__mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()


    def get_ratings_for_item(self, item_id):
        try:
            sql = 'SELECT rating FROM %s WHERE item_id = %s ;' % (self.__table, item_id)
            conn = self.__mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            ratings = cursor.fetchall()
            return [rating[0] for rating in ratings]
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()


    def get_average_rating_for_item(self, item_id):
        try:
            sql = 'SELECT AVG(rating) FROM %s WHERE item_id = %s ;' % (self.__table, item_id)
            conn = self.__mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            rating = cursor.fetchone()
            return rating[0]
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()


    def get_random_rating_record(self):
        try:
            sql = 'SELECT * FROM %s ORDER BY RAND() LIMIT 1 ;' % (self.__table)
            conn = self.__mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            rating = cursor.fetchone()
            return rating
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            conn.close()

