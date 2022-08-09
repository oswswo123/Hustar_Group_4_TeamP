import pandas as pd
from postgreSQL import PostgresDB


def main():
    try:
        ainalyst = PostgresDB(host='localhost', dbname='ainalyst', user='hustar', password='1234', port='5432')
        print(f"Connection is succeed \nDatabase: \n{ainalyst}")
    except Exception as e:
        print(f"Failed connect to db: ERROR code ({e})")
        return -1

    ainalyst.execute(f"DELETE FROM home_report;")
    # datas = ainalyst.execute("SELECT * FROM home_report;")
    # print("SELECT * FROM home_report;")
    # print("-"*100)
    # for d in datas:
    #     print(d)
    # print("-"*100)
    # print()

    df = pd.read_csv('./report_dataset.csv')

    for idx, (_, company, title, article, opinion, firm, date) in df.iterrows():
        print(f"{idx}: {company}, {title}, {opinion}, {firm}, {date}")
        ainalyst.execute(f"INSERT INTO home_report(create_date, company, title, article, opinion, new_opinion, firm)"
                         f" VALUES(%s, %s, %s, %s, %s, %s, %s);", (date, company, title, article, opinion, None, firm))

    print("Done")

    # print()
    # datas = ainalyst.execute("SELECT * FROM home_report;")
    # print("SELECT * FROM home_report;")
    # print("-" * 100)
    # for d in datas:
    #     print(d)
    # print("-" * 100)

if __name__ == '__main__':
    main()