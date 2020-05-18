import pymysql

conn = pymysql.connect("localhost", user="root", password="dgu1234!", db="dgu")

curs = conn.cursor()
country = 'Korea'
sql_command = """
select Customer_id from Customers where Country = %s;
"""
curs.execute(sql_command, country)
#1번예
result = curs.fetchall()
print("#1")
print("+-------------------+")
print("|    Customer_ID    |")
print("+-------------------+")
for row in result:
    print("|         %s         |" % row[0])
print("+-------------------+")

curs.close()

curs = conn.cursor()
p_id1 = 11
p_id2 = 13
sql_command = """
(select Order_ID from Cart where Product_ID = %s) union (select Order_ID from Cart where Product_ID = %s);
"""
curs.execute(sql_command, (p_id1, p_id2))

result = curs.fetchall()
print("#2")
print("+-------------------+")
print("|      Order_ID     |")
print("+-------------------+")
for row in result:
    print("|        %s       |" % row[0])
print("+-------------------+")

curs.close()

curs = conn.cursor()
price = 29.99
sql_command3 = """
select Product_ID, Quantity
from Cart as C
where exists(select Product_ID 
            from Products as P 
            where price = %s and C.Product_ID = P.Product_ID);
"""
curs.execute(sql_command3, price)

result3 = curs.fetchall()
print("#3")
print("+---------------------------+")
print("|   ID           Quantity   |")
print("+---------------------------+")
for row in result3:
    print("|  %03s\t\t%10s      |" % (row[0], row[1]))
print("+---------------------------+")

curs.close()


curs = conn.cursor()
cnt = 1
sql_command4 = """
select Customer_ID, cnt
from (select Customer_ID, count(*) as cnt
        from Confirm group by Customer_ID) as count 
where cnt > %s;
"""
curs.execute(sql_command4, cnt)

result4 = curs.fetchall()
print("#4")
print("+---------------------------+")
print("|   ID              cnt     |")
print("+---------------------------+")
for row in result4:
    print("|  %03s\t\t%10s      |" % (row[0], row[1]))
print("+---------------------------+")

curs.close()
#2번예제

curs = conn.cursor()
p_name = "LG_55inch_TV"
sql_command = """
    call SumOfStock(%s);
"""
curs.execute(sql_command, p_name)
result5 = curs.fetchall()
for row in result5:
    print("+---------------------------+")
    print("|          sum(Stock)       |")
    print("+---------------------------+")
    print("|            %3s            |" % (row[0]))
    print("+---------------------------+")
curs.close()


curs = conn.cursor()
o_id = '1004'
sql_command = """
     select ConfirmOrders(%s);
"""
curs.execute(sql_command, o_id)
result6 = curs.fetchall()

for row in result6:
    print("+---------------------------+")
    print("|      ConfirmOrders(%s)  |"%o_id)
    print("+---------------------------+")
    print("|%20s       |" % (row[0]))
    print("+---------------------------+")

curs.close()


