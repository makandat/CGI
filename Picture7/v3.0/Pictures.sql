CREATE TABLE Pictures (
  `ID` int not null primary key auto_increment,
  `TITLE` varchar(50) not null,
  `CREATOR` varchar(50) not null,
  `PATH` varchar(500) not null,
  `MARK` varchar(10),
  `INFO` varchar(100)
) CHARACTER SET utf8;
