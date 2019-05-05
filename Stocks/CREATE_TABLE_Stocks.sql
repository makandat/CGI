-- 証券管理
CREATE TABLE Stocks(
  id int not null auto_increment,
  `date` char(10) not null,
  stock_code int not null,
  amount int not null,
  current_price decimal(10) not null,
  purchased_price decimal(10),
  purchased_date char(10),
  sec_company varchar(20),
  info varchar(100),
  PRIMARY KEY(id)
) CHARACTER SET='UTF8';
