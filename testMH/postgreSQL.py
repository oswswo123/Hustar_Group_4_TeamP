import psycopg2

class Databases():
    def __init__(self, host='localhost', dbname='test_ainalyst', user='postgres', password='1234', port=5432):
        self.db = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()

    def insertDB(self, schema, table, colum, data):
        sql = f" INSERT INTO {schema}.{table}({colum}) VALUES ('{data}') ;"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" insert DB err ", e)

    def readDB(self, schema, table, colum):
        sql = f" SELECT {colum} from {schema}.{table}"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            result = (" read DB err", e)

        return result

    def updateDB(self, schema, table, colum, value, condition):
        sql = f" UPDATE {schema}.{table} SET {colum}='{value}' WHERE {colum}='{condition}' "
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(" update DB err", e)

    def deleteDB(self, schema, table, condition):
        sql = f" delete from {schema}.{table} where {condition} ; "
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("delete DB err", e)


def main():
    ainalyst_db = Databases(host='localhost', dbname='ainalyst', user='postgres', password='1234', port=5432)
    ainalyst_db.insertDB(schema='myschema', table='table', colum='ID', data='유동적변경')
    print(ainalyst_db.readDB(schema='myschema', table='table', colum='ID'))
    ainalyst_db.updateDB(schema='myschema', table='table', colum='ID', value='와우', condition='유동적변경')
    ainalyst_db.deleteDB(schema='myschema', table='table', condition="id != 'd'")

    cursor = ainalyst_db.cursor()

if __name__ == '__main__':
    main()
