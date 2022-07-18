import psycopg2


class PostgresDB:
    def __init__(self, host='localhost', dbname='ainalyst', user='hustar', password='1234', port=5432):  # defalut = ainalyst
        self.db = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)   # postgreSQL에 접속
        self.cursor = self.db.cursor()  # cursor 선언 (query 실행 시 필요)
        self.host = host
        self.dbname = dbname
        self.user = user
        self.port = port

    def __str__(self):
        string = f"DB-Type: Postgres | host: {self.host} | DB-Name: {self.dbname} | user: {self.user} | port: {self.port}"
        return string

    def __del__(self):  # 종료시 connection을 닫아줘야함
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):  # Query 문 실행 함수
        try:
            self.cursor.execute(query, args)
            if 'select' in query.lower():   # 실행한 Query 문이 SELECT면 탐색한 데이터를 반환해줘야 함
                rows = self.cursor.fetchall()
                return rows
            self.db.commit()    # SELECT 아니면 commit으로 DB에 반영
        except Exception as e:
            print(f"ERROR:: Failed to execute SQL query... (Error code: {e})")
            return -1

    # def commit(self):
    #     self.db.commit()

    # def insertDB(self, table, columns='', values=''):
    #     sql = f" INSERT INTO {table}{columns} VALUES ({values}); "
    #     try:
    #         self.cursor.execute(sql)
    #         self.db.commit()
    #     except Exception as e:
    #         print(f"ERROR:: Failed to insert data into database ... (Error code: {e})")
    #
    # def selectDB(self, table, columns='', condition='', order=''):
    #     if columns:
    #         if condition:
    #             sql = f" SELECT {columns} FROM {table} WHERE {condition}; "
    #         else:
    #             sql = f" SELECT {columns} FROM {table}; "
    #     else:
    #         if condition:
    #             sql = f" SELECT * FROM {table} WHERE {condition}; "
    #         else:
    #             sql = f" SELECT * FROM {table}; "
    #     try:
    #         self.cursor.execute(sql)
    #         result = self.cursor.fetchall()
    #     except Exception as e:
    #         result = f"ERROR:: Failed to select data from database ... (Error code: {e})"
    #
    #     return result
    #
    # def updateDB(self, table, columns, value='', condition=''):
    #     sql = f" UPDATE {table} SET {columns}={value} WHERE {condition}; "
    #     try:
    #         self.cursor.execute(sql)
    #         self.db.commit()
    #     except Exception as e:
    #         print(f"ERROR:: Failed to update data into database ... (Error code: {e})")
    #
    # def deleteDB(self, table, condition):
    #     sql = f" DELETE FROM {table} WHERE {condition}; "
    #     try:
    #         self.cursor.execute(sql)
    #         self.db.commit()
    #     except Exception as e:
    #         print(f"ERROR:: Failed to delete data in database ... (Error code: {e})")


def main():
    try:
        ainalyst = PostgresDB(host='localhost', dbname='ainalyst', user='hustar', password='1234', port=5432)
        print("Connection is success...")
        print(f"Create database is \n{ainalyst}")
    except Exception as e:
        print(f"ERROR:: Connection Failed... (Error code: {e})")
        return -1

    print(f"Initial DB")
    report_data = ainalyst.execute("SELECT * FROM report;")
    for rd in report_data:
        print(rd)
    print()

    # take 1
    data = {'id': '4', 'create_date': '2022-07-16', 'subject': '화성 갈끄니까', 'price': '212000',
                'opinion': '매도', 'writer': '일론이', 'stock_firm': '테슬라증권'}
    # take 2
    report_id, create_date, subject, price, opinion, writer, stock_firm = \
      '5', '2022-07-17', '파란나라를 보았니', '2300', 'Sell', '지져스', '하나증권'

    ainalyst.execute(f"INSERT INTO report VALUES('{data['id']}', '{data['create_date']}', '{data['subject']}', '{data['price']}',\
                                                 '{data['opinion']}', '{data['writer']}', '{data['stock_firm']}')")
    ainalyst.execute(f"INSERT INTO report VALUES('{report_id}', '{create_date}', '{subject}', '{price}', '{opinion}', '{writer}', '{stock_firm}')")

    report_data = ainalyst.execute("SELECT * FROM report;")
    print(f"After insert data into datebase")
    for rd in report_data:
        print(rd)

    ainalyst.execute(f"UPDATE report SET (writer, stock_firm)=('정약용', '성균관증권') WHERE id='2';")
    report_data = ainalyst.execute("SELECT * FROM report;")
    print(f"After update data into datebase")
    for rd in report_data:
        print(rd)

    # ainalyst.insertDB(table='report', columns='', values="'3', '2022-07-15', '지금 사세요', '32000', 'Sell', '사실구라', 'K증권'")
    # print(f"After insert to DB \n{ainalyst.selectDB(table='Report')}")

    # ainalyst.updateDB(table='report', columns='(create_date, subject, price)', value="('2022-07-12', 'Al den te', '50000')", condition="id = '2'")
    # print(f"After update to DB \n{ainalyst.selectDB(table='Report')}")

    # ainalyst.deleteDB(table='report', condition="id = 'pdf1'")
    # print(f"After delete to DB \n{ainalyst.selectDB(table='Report')}")


if __name__ == '__main__':
    main()
