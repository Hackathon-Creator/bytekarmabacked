import sqlite3
#import json

#conn = sqlite3.connect('database.db')
#print ("Opened database successfully...")
#conn.execute('DROP TABLE PD_TABLE')
#conn.execute('CREATE TABLE PD_TABLE (cif INT, pod FLOAT, gambling FLOAT, amazon FLOAT, shopping FLOAT, food FLOAT, movie FLOAT, cc_bill FLOAT,customer_contacted INT, create_date DATETIME)')
#print ("New table created successfully...")
#conn.close()

conn = sqlite3.connect('database.db')
print ("Opened database successfully...")
conn.execute('DROP TABLE PD_TABLE')
conn.execute('CREATE TABLE PD_TABLE (cif INT, pod FLOAT, gambling FLOAT, amazon FLOAT, shopping FLOAT, food FLOAT, movie FLOAT, cc_bill FLOAT,customer_contacted INT ,create_date DATETIME )')
print ("New table created successfully...")
conn.close()

#sqlite_select_query = """"

#cursor = conn.cursor()
#
#cursor.execute("with tc as ( SELECT count(*) from PD_TABLE),cc as (SELECT count(*) from PD_TABLE where customer_contacted = 1),pd as (SELECT count(*) from PD_TABLE where pod > 0.05) select * from tc,cc, pd")
#
#records = cursor.fetchall()

#cursor.execute("SELECT count(*) from PD_TABLE where customer_contacted = 1")
#
#cc = cursor.fetchall()[0][0]

#for row in records:
#    print(type(row))
#    print(row.)

#print(records[0])
