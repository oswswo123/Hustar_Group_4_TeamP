import pandas as pd
from postgreSQL import PostgresDB


def main():
    try:
        ainalyst = PostgresDB(host='localhost', dbname='ainalyst', user='hustar', password='1234', port='5432')
        print(f"Connection is succeed \nDatabase: \n{ainalyst}")
    except Exception as e:
        print(f"ERROR:: Failed connect to db  ({e})")
        return -1

    df = pd.read_csv('/home/piai/hustar/automation/data/ensemble_inference_data.csv')

    try:
        for idx, (company, title, article, opinion, firm, date, predictions, pred_rate) in df.iterrows():
            print(f"{idx}: {date}, {company}, {title}, {opinion}, {predictions}, {pred_rate}")
            ainalyst.execute(f"INSERT INTO home_report(create_date, company, title, article, opinion, new_opinion, firm, pred_rate)"
                             f" VALUES(%s, %s, %s, %s, %s, %s, %s, %s);", (date, company, title, article, opinion, predictions, firm, pred_rate))

    except Exception as e:
        print(f"ERROR:: Failed insert to db  ({e})")
        return -1

    print("Done")


if __name__ == '__main__':
    main()
