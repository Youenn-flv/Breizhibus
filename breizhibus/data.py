import mysql.connector as ms
import pandas as pd


def get_data(query):
    
        bdd = ms.connect(user="utilisateurbus", password="motdepasse", host="localhost", port="3307", database="breizhibus")

        cursor = bdd.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        dframe = pd.DataFrame(data, columns=cursor.column_names)
        bdd.close()
        return dframe

