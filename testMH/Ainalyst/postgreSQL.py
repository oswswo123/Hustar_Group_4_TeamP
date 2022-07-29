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

    def execute(self, query, args=()):  # Query 문 실행 함수
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


def main():
    try:
        ainalyst = PostgresDB(host='localhost', dbname='ainalyst', user='hustar', password='1234', port=5432)
        print("Initializing and Connecting to Database is success...")
    except Exception as e:
        print(f"ERROR:: Connection Failed... (Error code: {e})")
        return -1

    print(f"Information for database \n{ainalyst}")
    print(f"Initial DB")
    report_data = ainalyst.execute("SELECT * FROM report;")     # SELECT 문으로 report 테이블 내용 조회, 테이블 전체를 반환함
    for rd in report_data:  # [('1', datetime.date(2022, 7, 10), ...), ('3', datetime.date(2022, 7, 15), ...)] 형태로 반환
        print(rd)


if __name__ == '__main__':
    main()
