import csv
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def search_kata(conn, katakunci):
    cur = conn.cursor()
    cur.execute("SELECT * FROM kbbi WHERE kata=?", (katakunci,))

    rows = cur.fetchall()
    return rows

def main():
    data_cocok=0
    data_tidak_cocok=0
    combine=[]
    database = "kbbi.db"
    conn = create_connection(database)
    # Read CSV
    csvfile = open('TweetBaru_clean_Final2.csv', mode='r')
    readfile = csv.reader(csvfile, delimiter=',')
    # skip header
    next(readfile)

    # Open file CSV for write data
    with open('New_OOV.csv', mode='w', newline='') as hasil:

        hasil_csv = csv.writer(hasil, delimiter=',')
        # create header CSV
        hasil_csv.writerow(["no", "kata alay"])

        # Distinct source
        source_distinc=distinct(readfile)

        # Split and Distinct
        for row in source_distinc:
            word = row[0].split(' ')
            word2 = row[1].split(' ')
            combine += word
            combine += word2
        kata=distinct(combine)

        #Check to database
        for cocok in kata:
            with conn:
                if cocok:
                    cari = search_kata(conn, cocok)
                    if len(cari) > 0:
                        data_cocok += 1
                    else:
                        data_tidak_cocok += 1
                        hasil_csv.writerow([data_tidak_cocok, cocok])
                        print(cocok)
    total=data_cocok+data_tidak_cocok
    print("-----------------------------------------")
    print("Statistik dataset |distinc   |")
    print("-----------------------------------------")
    print("total kata Dataset| "+str(total))
    print("total kata kamus  | "+str(data_cocok))
    print("total OOV         | "+str(data_tidak_cocok))

def distinct(file):
    print("distinc in progresss....")
    unique_word = []
    for row in file:
        if row not in unique_word:
            unique_word.append(row)
    unique_word.sort()
    print("distinc finish")
    return unique_word

if __name__ == '__main__':
   main()