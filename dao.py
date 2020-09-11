from datetime import datetime
from random import randint
import sqlite3

import pandas as pd

def open_connection():
    global conn
    conn = sqlite3.connect('database.db')
    print ("Opened database for operation successfully\n")

def save(df):
    try:
        open_connection()
    except:
         return 'error 1'
        
    try:    
        
        for index,row in df.iterrows():
#            print(row['CIF'], row['POD'])
            conn.execute("INSERT INTO PD_TABLE (cif,pod,gambling,amazon,shopping,food,movie,cc_bill,customer_contacted,create_date) VALUES (?,?,?,?,?,?,?,?,?,?)",(int(row['CIF']),row['POD'],row['Gambling'],row['Amazon'],row['Shopping'],row['Food'],row['Movie'],row['CC_Bill'],randint(0,1),datetime.now()))
        
        conn.commit()
        conn.close()
        return 'success'
    except:
        conn.close()
        return 'error 2'

def searchCif(cif):
    try:
        open_connection()
    except:
         return 'error 1'
    try:
        conn.cursor()
#        cursor.execute("SELECT cif,pod,gambling,amazon,shopping,food,movie,cc_bill,create_date from PD_TABLE where cif = ? order by rowid desc", (cif,))
        sql = r""" SELECT cif,pod,gambling,amazon,shopping,food,movie,cc_bill,create_date from PD_TABLE where cif = {0} order by rowid desc """
        sql1 = sql.format(cif)
        print(sql1)
        df= pd.read_sql_query(sql1,conn)
        
#        records = cursor.fetchall()
        conn.close()
        return df
    except:
         conn.close()
         return 'error 2'
     
def home():
    try:
        open_connection()
    except:
         return 'error 1'
     
    try:
        cursor = conn.cursor()
        cursor.execute("with tc as ( SELECT count(*) from PD_TABLE),cc as (SELECT count(*) from PD_TABLE where customer_contacted = 1),pd as (SELECT count(*) from PD_TABLE where pod > 0.05) select * from tc,cc, pd")
        result = cursor.fetchall()[0]
        conn.close()
        
        return str(result[0]) + ',' + str((result[1]/result[0])*100) + ',' + str( (result[2]/result[0])*100 )
    except:
         conn.close()
         return 'error 2'
     
        
        
        
        
        
        
        
        
        
        
        
        