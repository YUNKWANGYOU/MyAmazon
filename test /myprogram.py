import os
import datetime
from datetime import timedelta


class MyProgram:
    cart = {}
    c_id = 0

    def __init__(self, conn):
        self.conn = conn

    def start(self):
        while True:
            os.system('clear')
            print("+----------------------------------+")
            print("|           1.  Login              |")
            print("|           2.  Sign up            |")
            print("|           3.  Exit               |")
            print("+----------------------------------+")

            var = input("Press the button. [1~3] \n>>> ")
            if var == '1':
                login = self.login()
                if login is True:
                    return True
            elif var == '2':
                sign_up = self.sign_up()
                if sign_up is True:
                    return True
            elif var == '3':
                return False

    def login(self):
        while True:
            os.system('clear')
            try:
                print("+----------------------------------+")
                print("|              Login               |")
                print("+----------------------------------+")
                self.c_id = int(input("ID: "))
                break
            except ValueError:
                input("Please enter a number.")
                return

        curs = self.conn.cursor()
        sql_command = "select Customer_ID from Customers"
        curs.execute(sql_command)

        result = curs.fetchall()
        for row in result:
            if self.c_id == row[0]:
                sql_command = "select Customer_Name from Customers where Customer_ID = %s"
                curs.execute(sql_command, self.c_id)

                result2 = curs.fetchone()
                print("+----------------------------------+")
                print("|        welcome,%12s      |" % result2[0])
                print("+----------------------------------+")
                curs.close()
                input("( Please press the Enter button )")
                return True

        print("+---------------------------------+")
        print("|           No ID exists          |")
        print("+---------------------------------+")
        curs.close()
        input("( Please press the Enter button )")

    def sign_up(self):
        while True:
            os.system('clear')
            print("+----------------------------------+")
            print("|             Sign up              |")
            print("+----------------------------------+")
            name = input("Name: ")
            address = input("Address: ")
            country = input("Country: ")
            try:
                contact = int(input("Contact: "))
            except ValueError:
                contact = None
            if name != '' and address != '' and country != '' and contact is not None:
                break
            else:
                input("Cannot make an ID.")
                return
        while True:
            confirm = input("Confirm [y/n]: ")
            if confirm == 'y':
                curs = self.conn.cursor()
                sql_command = "insert into Customers (Customer_Name, Address, Country, Contact)" \
                              "values (%s, %s, %s, %s);"
                curs.execute(sql_command, (name, address, country, contact))
                self.conn.commit()
                sql_command = "select Customer_ID from Customers;"
                curs.execute(sql_command)
                result = curs.fetchall()

                self.c_id = int(result[-1][0])
                print("your id is %s." % result[-1][0])
                curs.close()
                input("( Please press the Enter button )")
                return True
            elif confirm == 'n':
                input("Canceled.\n( Please press the Enter button )")
                break

    def menu(self):
        while True:
            os.system('clear')
            print("+----------------------------------+")
            print("|          Amazon services         |")
            print("|        1. Shop products          |")
            print("|        2. Check your cart        |")
            print("|        3. Your orders            |")
            print("|        4. Your account info      |")
            print("|        5. Logout                 |")
            print("|        6. Exit program           |")
            print("+----------------------------------+")

            var = input("Press the button [1~6] \n>>> ")
            if var == '1':
                self.shop_product()
            elif var == '2':
                self.check_cart()
            elif var == '3':
                self.your_orders()
            elif var == '4':
                self.account_info()
            elif var == '5':
                self.execute()
                break
            elif var == '6':
                break

    def shop_product(self):
        while True:
            os.system('clear')
            print("+--------------------------------------------+")
            print("| # |         Product        |     Price     |")
            print("+--------------------------------------------+")
            print("| 1 |    PS4                 |     499.99    |")
            print("| 2 |    iPhone11            |     999.99    |")
            print("| 3 |    LG 55 inch TV       |    1499.99    |")
            print("| 4 |    NIKE soccer ball    |      29.99    |")
            print("| 5 |    POLO shirts         |      39.99    |")
            print("| 6 |    Vacuum cleaner      |     139.99    |")
            print("|                                            |")
            print("| 0 |   Cancel                               |")
            print("+--------------------------------------------+")
            try:
                prod = int(input("Select product: "))
            except ValueError:
                input("Please select a product by number.\n( Please press the Enter button )")
                continue
            if prod == 0:
                input("Canceled.\n( Please press the Enter button )")
                return
            elif 1 <= prod <= 6:
                try:
                    qty = int(input("Quantity: "))
                except ValueError:
                    input("Please type a number.\n( Please press the Enter button )")
                    return
                while True:
                    confirm = input("Add to cart? [y/n]: ")
                    if confirm == 'y':
                        p_id = 0
                        if prod == 1:
                            p_id = 11
                        elif prod == 2:
                            p_id = 12
                        elif prod == 3:
                            p_id = 13
                        elif prod == 4:
                            p_id = 14
                        elif prod == 5:
                            p_id = 15
                        elif prod == 6:
                            p_id = 16
                        if p_id in self.cart:
                            self.cart[p_id] += qty
                        else:
                            self.cart[p_id] = qty
                        input("Item added to cart.\n( Please press the Enter button )")
                        while True:
                            var = input("Do you want to add more item? [y/n]: ")
                            if var == 'y':
                                break
                            elif var == 'n':
                                return
                        break
                    elif confirm == 'n':
                        input("Canceled.\n( Please press the Enter button )")
                        return
            else:
                input("Please type a number that is valid.\n( Please press the Enter button )")

    def print_cart(self):
        curs = self.conn.cursor()
        sql_command = "select Product_Name, Price from Products where Product_ID = %s;"
        tot_price = 0
        print("+--------------------------------------------+")
        print("| # |         Product         |   Quantity   |")
        print("+--------------------------------------------+")
        for p_id in self.cart.keys():
            qty = self.cart.get(p_id)
            curs.execute(sql_command, p_id)
            result = curs.fetchone()
            print("|%2s |%24s |%13s |" % (list(self.cart.keys()).index(p_id) + 1, result[0], qty))
            tot_price = tot_price + result[1] * qty
        print("|                                            |")
        print("|                     Total Price: %9s |" % tot_price)
        print("+--------------------------------------------+")
        curs.close()

    def check_cart(self):
        while True:
            os.system('clear')
            self.print_cart()

            print("+----------------------------------+")
            print("|         1. Place Order           |")
            print("|         2. Delete item           |")
            print("|         3. Clear cart            |")
            print("|         4. Return to menu        |")
            print("+----------------------------------+")

            var = input("Press the button [1~4] \n>>> ")
            if var == '1':
                place_order = self.place_order()
                if place_order is True:
                    break
            elif var == '2':
                self.delete_item()
            elif var == '3':
                self.clear_cart()
            elif var == '4':
                break

    def place_order(self):
        os.system('clear')
        print("+--------------------------------------------+")
        print("|               Shipping Address             |")
        print("+--------------------------------------------+")
        curs = self.conn.cursor()
        sql_command = "select Customer_Name, Address, Country, Contact from Customers where Customer_ID = %s"
        curs.execute(sql_command, self.c_id)
        result = curs.fetchone()
        print("|   Name:\t\t%s\t     |" % result[0])
        print("|   Address:\t\t%s\t\t     |" % result[1])
        print("|   Country:\t\t%s\t\t     |" % result[2])
        print("|   Contact:\t\t0%s\t     |" % result[3])
        if len(list(self.cart.keys())) == 0:
            self.print_cart()
            input("Cart is empty.\n( Please press the Enter button )")
            return False
        self.print_cart()
        today = datetime.date.today()
        td1 = timedelta(days=5)
        td2 = timedelta(days=2)

        today_int = int(today.isoformat().replace('-', ''))
        """
        print("|                   Date                     |")
        print("+--------------------------------------------+")
        print("|   Order date : %11s\t\t     |" % today)
        print("|   Estimated delivery date : %11s    |" % (today + td1))
        print("|   Shipped date : %11s\t\t     |" % (today + td2))
        print("+--------------------------------------------+")
        """
        print("|                   Date                     |")
        print("+--------------------------------------------+")
        print("|   Order date : \t\t%11s  |" % today)
        print("|   Estimated delivery date :   %11s  |" % (today + td1))
        print("|   Shipped date : \t\t%11s  |" % (today + td2))
        print("+--------------------------------------------+")
        while True:
            confirm = input("Confirm? [y/n]: ")
            if confirm == 'y':
                curs = self.conn.cursor()
                sql_command = "insert into Orders (Order_Date, Required_Date, Shipped_Date) values (%s, %s, %s);"
                curs.execute(sql_command, (today_int, today_int + 2, today_int + 5))
                sql_command = "select Order_ID from Orders;"
                curs.execute(sql_command)
                result = curs.fetchall()
                o_id = int(result[-1][0])
                for p_id in self.cart.keys():
                    qty = self.cart.get(p_id)
                    sql_command = "insert into Cart values (%s, %s, %s)"
                    curs.execute(sql_command, (o_id, p_id, qty))
                    sql_command = "Update Products set Stock = Stock - %s where Product_ID = %s"
                    curs.execute(sql_command, (qty, p_id))
                    self.conn.commit()
                sql_command = "insert into Confirm values (%s, %s)"
                curs.execute(sql_command, (o_id, self.c_id))
                self.conn.commit()
                curs.close()
                self.cart.clear()
                input("Successfully ordered.\n( Please press the Enter button )")
                break
            elif confirm == 'n':
                curs.close()
                input("Canceled.\n( Please press the Enter button )")
                break

    def delete_item(self):
        os.system('clear')
        self.print_cart()
        try:
            var = int(input("Select item number: "))
        except ValueError:
            input("Please type a number.\n( Please press the Enter button )")
            return
        try:
            key = list(self.cart.keys())[var - 1]
        except IndexError:
            input("Item does not exist for this number.\n( Please press the Enter button )")
            return

        while True:
            confirm = input("Confirm? [y/n]: ")
            if confirm == 'y':
                del self.cart[key]
                break
            elif confirm == 'n':
                input("Canceled.\n( Please press the Enter button )")
                break

    def clear_cart(self):
        os.system('clear')
        self.print_cart()
        while True:
            confirm = input("Confirm? [y/n]: ")
            if confirm == 'y':
                self.cart.clear()
                input("Cart is cleared.\n( Please press the Enter button )")
                break
            elif confirm == 'n':
                input("Canceled.\n( Please press the Enter button )")
                break

    def your_orders(self):
        os.system('clear')
        curs = self.conn.cursor()
        sql_command = "call Order_info(%s)"
        curs.execute(sql_command, self.c_id)
        result = curs.fetchall()
        tot_price = 0
        temp = ''
        print("+-----------------------------------------------------------------------------------------------+")
        print("|  Order_ID  |           Product         | Quantity |   Price   |    Address    |    Country    |")
        print("+-----------------------------------------------------------------------------------------------+")
        for row in result:
            if temp != row[0] and result[0] != row:
                print("|                                                                                        "
                      "       |")
                print("|                                                                        Total price: %9s |"
                      % tot_price)
                print("+----------------------------------------------------------------------------------------"
                      "-------+")
                tot_price = 0
            print("|%11s |%26s |%9s |%10s |%14s |%14s |" % (row[0], row[1].replace('_', ' '), row[2], row[3],
                                                            row[4], row[5]))
            temp = row[0]
            tot_price = tot_price + row[3]
            if result[-1] == row:
                print("|                                                                                        "
                      "       |")
                print("|                                                                        Total price: %9s |"
                      % tot_price)
                print("+----------------------------------------------------------------------------------------"
                      "-------+")
        input("( Please press the Enter Button )")

    def account_info(self):
        while True:
            os.system('clear')
            curs = self.conn.cursor()
            sql_command = "select * from Customers where Customer_ID = %s"
            curs.execute(sql_command, self.c_id)
            result = curs.fetchone()
            contact = str(result[4])
            print("+--------------------------------+")
            print("|      Account Information       |")
            print("+--------------------------------+")
            print("|  Name :       %s\t |" % result[1])
            print("|  Address :    %s\t\t |" % result[2])
            print("|  Country :    %s\t\t |" % result[3])
            print("|  Contact :    0%s-%s-%s    |" % (contact[0:2], contact[2:6], contact[6:]))
            print("+--------------------------------+\n")
            print("+--------------------------------+")
            print("|        1. Change Info          |")
            print("|        2. Return to menu       |")
            print("+--------------------------------+")
            curs.close()
            var = input("Press the button [1~2] \n>>> ")
            if var == '1':
                change_info = self.change_info()
                if change_info is True:
                    break
            elif var == '2':
                break

    def change_info(self):
        while True:
            os.system('clear')
            print("+--------------------------------+")
            print("|      Account Information       |")
            print("+--------------------------------+")
            name = input("Name: ")
            address = input("Address: ")
            country = input("Country: ")
            try:
                contact = int(input("Contact: "))
            except ValueError:
                contact = None
            if name != '' and address != '' and country != '' and contact is not None:
                break
            else:
                input("Cannot change information.\n( Please press the Enter button )")
                return False
        while True:
            confirm = input("Confirm? [y/n]: ")
            if confirm == 'y':
                curs = self.conn.cursor()
                sql_command = "update Customers set Customer_Name = %s, Address = %s, Country = %s," \
                              "Contact = %s where Customer_ID = %s;"
                curs.execute(sql_command, (name, address, country, contact, self.c_id))
                self.conn.commit()
                curs.close()
                return True
            elif confirm == 'n':
                input("Canceled.\n( Please press the Enter button )")
                break

    def execute(self):
        start = self.start()
        if start is True:
            self.menu()