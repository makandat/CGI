CREATE TABLE Album (
  id int not null auto_increment,
  name varchar(50) not null,
  mark varchar(10),
  info varchar(100),
  bindata int default 0,
  primary key(id)
);


CREATE TABLE PictureAlbum (
  id int(11) not null auto_increment,
  album int not null,
  title varchar(100) not null,
  path varchar(500) not null,
  creator varchar(100) not null,
  info varchar(100),
  fav int(1) default 0,
  bindata int(11) default 0,
  primary key(id)
);