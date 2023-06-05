from django.db import connection

my_cursor = None
class my_db():

    def conn(self):
        cursor = connection.cursor()
        cursor.execute("SET timezone TO 'Asia/Tbilisi';")
        return cursor


    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]