show databases;
drop database dgu;
create database dgu;
use dgu;

create table Products(
	Product_ID int,
    Product_Name varchar(20),
    Price numeric(8,2),
    Stock int unsigned,
    
    primary key(Product_ID)
);
    
create table Seller(
	Seller_ID int,
    Seller_Name varchar(20),
    Address varchar(20),
    Country varchar(20),
    Contact int,
    
    primary key(Seller_ID)
);
    
create table Category(
    Category_ID int,
    Category_Name varchar(20),
    description varchar(20),
    
    primary key(Category_ID)
);

create table Orders(
	Order_ID int auto_increment,
    Order_Date int,
    Required_Date int,
    Shipped_Date int,
    
    primary key(Order_ID)
    
);

create table Customers(
	Customer_ID int auto_increment,
	Customer_Name varchar(50),
    Address varchar(50),
    Country varchar(50),
    Contact int,
    
    primary key(Customer_ID)
);

create table Shipment(
	Shipment_ID int,
	Company_Name varchar(50),
    Contact int,

    primary key(Shipment_ID)
);

create table Ship(
	Order_ID int,
    Shipment_ID int,
	Ship_Address varchar(20),
    
    primary key(Order_ID, Shipment_ID),
    foreign key(Order_ID) references Orders(Order_ID),
    foreign key(Shipment_ID) references Shipment(Shipment_ID)
);

create table Confirm(
    Order_ID int,
    Customer_ID int,
	
    primary key(Order_ID, Customer_ID),
	foreign key(Order_ID) references Orders(Order_ID),
    foreign key(Customer_ID) references Customers(Customer_ID)
);

create table Cart(
	Order_ID int,
	Product_ID int,
    Quantity int,
    
	primary key(Order_ID, Product_ID),
    foreign key(Order_ID) references Orders(Order_ID),
    foreign key(Product_ID) references Products(Product_ID)
);

create table Sell(
	Product_ID int,
    Seller_ID int,
    
    primary key(Product_ID, Seller_ID),
	foreign key (Product_ID) references Products(Product_ID),
    foreign key (Seller_ID) references Seller(Seller_ID)
);

create table Belong(
    Product_ID int,
    Category_ID int,
    
    primary key(Product_ID, Category_ID),
    foreign key (Product_ID) references Products(Product_ID),
	foreign key (Category_ID) references Category(Category_ID)
);

# Products, Orders, Customers, Confirm, Cart

# Customers
insert into Customers values(1, 'YouYunKwang', 'Seokgye' ,'Korea', 01079124032);
insert into Customers values(2, 'KimRaeYoung', 'DaeBang' ,'Korea', 01043273839);
insert into Customers values(3, 'KimSangHun', 'Omokgyo', 'Korea', 01051930493);
insert into Customers values(4, 'SonHeungMin', 'London', 'England', 01095830324);
insert into Customers values(5, 'GongSungHun', 'Sydney', 'Australia', 01084732922);

# Orders
insert into Orders values(1001, 20190504, 20190510, 20190506);
insert into Orders values(1002, 20191111, 20191116, 20191113);
insert into Orders values(1003, 20190807, 20190810, 20190810);
insert into Orders values(1004, 20190515, 20190517, 20190516);
insert into Orders values(1005, 20190704, 20190710, 20190706);

# Products
insert into Products values (11, 'PS4', 499.99, 700);
insert into Products values (12, 'iPhone11', 999.99, 1000);
insert into Products values (13, 'LG_55inch_TV', 1499.99, 400);
insert into Products values (14, 'NIKE_soccer_ball', 29.99, 100);
insert into Products values (15, 'POLO_shirts', 39.99, 1500);
insert into Products values (16, 'vacuum_cleaner', 139.99, 1500);

# Confirm
insert into Confirm values(1001, 1);
insert into Confirm values(1002, 3);
insert into Confirm values(1003, 2);
insert into Confirm values(1004, 4);
insert into Confirm values(1005, 4);

#Cart
insert into Cart values (1001, 11, 1);
insert into Cart values (1002, 12, 2);
insert into Cart values (1003, 12, 1);
insert into Cart values (1003, 13, 5);
insert into Cart values (1004, 11, 4);
insert into Cart values (1004, 14, 10);
insert into Cart values (1005, 11, 1);
insert into Cart values (1005, 13, 1);
insert into Cart values (1005, 15, 3);

delimiter &
drop procedure if exists SumOfStock_2&
create procedure SumOfStock_2(in name varchar(20))
begin
	select sum(Stock) from  Products as p where p.Product_name = name ;
end &
delimiter ;

delimiter //
create function ConfirmOrders( id int ) returns varchar(20) deterministic
begin
	declare c_name varchar(20);
	declare o_id int;
    
    set o_id = id;
    select Customer_name into c_name from Customers as C1, Confirm as C2 where C1.Customer_ID = C2.Customer_ID and C2.ORDER_ID = o_id;
    return(c_name);
end //
delimiter ;
select ConfirmOrders(1004);

DROP PROCEDURE IF EXISTS Order_info;
delimiter //
CREATE PROCEDURE Order_info(IN C_id int)
BEGIN
    select C2.Order_ID, Product_Name, Quantity, Price * Quantity as Price, Address, Country
	from Cart as C1, Confirm as C2, Customers as C3, Products as P
	where C1.Product_ID = P.Product_ID and C1.Order_ID = C2.Order_ID and C2.Customer_ID = C3.Customer_ID and C3.Customer_ID = C_id
    order by C2.Order_ID;
end //
delimiter ;