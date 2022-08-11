import pandas as pd
from postgreSQL import PostgresDB


def main():
    try:
        ainalyst = PostgresDB(host='localhost', dbname='ainalyst', user='hustar', password='1234', port='5432')
        print(f"Connection is succeed \nDatabase: \n{ainalyst}")
    except Exception as e:
        print(f"Failed connect to db: ERROR code ({e})")
        return -1

    # ainalyst.execute(f"DELETE FROM home_report;")
    # datas = ainalyst.execute("SELECT * FROM home_report;")
    # print("SELECT * FROM home_report;", end='\n')
    # for d in datas:
    #     print(d)
    # print("-"*100)
    # print()

    df = pd.read_csv('./convert_inference_data.csv')

    for idx, (company, title, article, opinion, firm, date, predictions, pred_rate) in df.iterrows():
        # print(f"{idx}: {date}, {company}, {title}, {opinion}, {predictions}, {pred_rate}")
        ainalyst.execute(f"INSERT INTO home_report(create_date, company, title, article, opinion, new_opinion, firm, pred_rate)"
                         f" VALUES(%s, %s, %s, %s, %s, %s, %s, %s);", (date, company, title, article, opinion, predictions, firm, pred_rate))
        # ainalyst.execute(f"UPDATE home_report SET pred_rate='%s'"
        #                  f"WHERE create_date=%s AND company=%s AND title=%s AND article=%s AND opinion=%s AND new_opinion=%s AND firm=%s",
        #                  (pred_rate, date, company, title, article, opinion, predictions, firm))

    print("Done")


if __name__ == '__main__':
    main()
